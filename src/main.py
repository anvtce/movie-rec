import os
import shutil
import kagglehub
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS, ALSModel
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.functions import col, explode, avg, udf
from pyspark.sql.types import FloatType, ArrayType
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.linalg import Vectors, Vector
import numpy as np

def init_spark():
    # Khởi tạo Spark với cấu hình phù hợp
    return SparkSession.builder \
        .appName("MovieLens20M_Recommendation") \
        .config("spark.driver.memory", "8g") \
        .config("spark.executor.memory", "8g") \
        .config("spark.sql.shuffle.partitions", "200") \
        .getOrCreate()

def get_data_and_prepare_paths():
    # 1. Xác định thư mục hiện tại (nơi chứa main.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(os.path.dirname(current_dir), "movielens_20m_data")

    # 2. Tải dataset từ Kaggle
    print("--- Đang tải bộ dữ liệu từ Kaggle... ---")
    tmp_download_path = kagglehub.dataset_download("grouplens/movielens-20m-dataset")

    # 3. Di chuyển file từ thư mục tạm của kagglehub về thư mục project nếu chưa có
    if not os.path.exists(dataset_dir):
        shutil.copytree(tmp_download_path, dataset_dir)
        print(f"--- Đã lưu dữ liệu tại: {dataset_dir} ---")
    else:
        print(f"--- Dữ liệu đã tồn tại tại: {dataset_dir} ---")

    rating_path = os.path.join(dataset_dir, "rating.csv")
    movie_path = os.path.join(dataset_dir, "movie.csv")
    genome_path = os.path.join(dataset_dir, "genome_scores.csv")
    return rating_path, movie_path, genome_path

def train_and_save(spark, rating_path, model_path):
    print(f"--- Đang nạp dữ liệu từ: {rating_path} ---")
    df = spark.read.csv(rating_path, header=True, inferSchema=True)
    
    data = df.select(
        col("userId").cast("int"),
        col("movieId").cast("int"),
        col("rating").cast("float")
    ).dropna()

    (training, test) = data.randomSplit([0.8, 0.2], seed=42)

    als = ALS(
        maxIter=10, 
        regParam=0.05, 
        rank=20,
        userCol="userId", 
        itemCol="movieId", 
        ratingCol="rating",
        coldStartStrategy="drop",
        nonnegative=True
    )

    print("--- Đang huấn luyện mô hình ALS... ---")
    model = als.fit(training)

    # Đánh giá nhanh
    predictions = model.transform(test)
    evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")
    rmse = evaluator.evaluate(predictions)
    print(f"--- Chỉ số RMSE: {rmse:.4f} ---")

    # Lưu model
    if os.path.exists(model_path):
        shutil.rmtree(model_path)
    model.save(model_path)
    return model

class ContentBasedRecommender:
    def __init__(self, spark, genome_path):
        self.spark = spark
        self.genome_path = genome_path
        self.movie_profiles = None

    def build_profiles(self):
        print("--- Đang xây dựng Movie Profiles từ Genome data... ---")
        # Đọc genome_scores.csv: movieId, tagId, relevance
        genome_df = self.spark.read.csv(self.genome_path, header=True, inferSchema=True)
        
        # Pivot dữ liệu để mỗi movie là một vector đặc điểm (tagId -> relevance)
        # Vì số lượng tag rất lớn, ta chỉ lấy các tag có relevance cao hoặc dùng VectorAssembler
        # Để đơn giản và hiệu quả trong Spark, ta sẽ group by movieId và thu thập các đặc điểm
        
        # Lấy top tags cho mỗi movie để giảm chiều dữ liệu nếu cần, 
        # nhưng ở đây ta sẽ dùng phương pháp tạo vector từ các tag có relevance > 0.5
        filtered_genome = genome_df.filter(col("relevance") > 0.5)
        
        # Tạo vector đặc điểm cho mỗi phim
        # Lưu ý: Trong thực tế với 20M data, ta nên dùng một ma trận thưa (Sparse Matrix)
        # Ở đây ta sẽ lưu trữ dưới dạng DataFrame để join sau này
        self.movie_profiles = filtered_genome.select("movieId", "tagId", "relevance")
        print("--- Đã xây dựng xong Movie Profiles ---")

    def get_similar_movies(self, movie_id, top_n=10):
        if self.movie_profiles is None:
            raise ValueError("Hãy gọi build_profiles() trước khi gợi ý.")
        
        # Tìm các phim có cùng các tag với movie_id
        target_tags = self.movie_profiles.filter(col("movieId") == movie_id).select("tagId").collect()
        target_tag_ids = [row.tagId for row in target_tags]
        
        if not target_tag_ids:
            return self.spark.createDataFrame([], "movieId int, score float")

        # Tính điểm tương đồng đơn giản: tổng relevance của các tag chung
        similar_movies = self.movie_profiles.filter(col("tagId").isin(target_tag_ids)) \
            .groupBy("movieId") \
            .agg(avg("relevance").alias("score")) \
            .filter(col("movieId") != movie_id) \
            .orderBy(col("score").desc()) \
            .limit(top_n)
            
        return similar_movies


def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    model_save_path = os.path.join(root_dir, "models", "als_movie_model")
    
    spark = init_spark()
    
    try:
        # Bước 1: Tải dữ liệu về thư mục project
        rating_path, movie_path, genome_path = get_data_and_prepare_paths()
        
        # Bước 2: Huấn luyện hoặc Load model ALS
        if not os.path.exists(model_save_path):
            model = train_and_save(spark, rating_path, model_save_path)
        else:
            print("--- Đang tải mô hình đã có sẵn... ---")
            model = ALSModel.load(model_save_path)

        # Bước 3: Khởi tạo Content-Based Recommender
        cb_recommender = ContentBasedRecommender(spark, genome_path)
        cb_recommender.build_profiles()

        # Bước 4: Dự đoán và Gợi ý Hybrid
        movies_df = spark.read.csv(movie_path, header=True, inferSchema=True)

        print("\n--- Tiến hành gợi ý Hybrid cho 3 người dùng (ID: 1, 2, 3) ---")
        user_ids = [1, 2, 3]
        
        for user_id in user_ids:
            print(f"\n>>> Gợi ý cho User {user_id}:")
            
            # 1. Lấy gợi ý từ ALS (Collaborative)
            users_df = spark.createDataFrame([(user_id,)], ["userId"])
            als_recs = model.recommendForUserSubset(users_df, 10)
            
            # Phẳng hóa kết quả ALS
            flat_als = als_recs.withColumn("rec", explode("recommendations")) \
                .select(col("rec.movieId").alias("movieId"), col("rec.rating").alias("als_score"))
            
            # 2. Lấy gợi ý từ Content-Based (Dựa trên phim user thích nhất)
            # Tìm phim user đánh giá cao nhất (>= 4.0)
            user_ratings = spark.read.csv(rating_path, header=True, inferSchema=True) \
                .filter((col("userId") == user_id) & (col("rating") >= 4.0)) \
                .orderBy(col("rating").desc())
            
            top_movie = user_ratings.select("movieId").first()
            
            if top_movie:
                movie_id = top_movie.movieId
                cb_recs = cb_recommender.get_similar_movies(movie_id, top_n=10)
                # Join ALS và CBF
                final_recs = flat_als.join(cb_recs, on="movieId", how="outer") \
                    .fillna(0, subset=["als_score", "score"]) \
                    .withColumn("hybrid_score", col("als_score") * 0.7 + col("score") * 0.3) \
                    .orderBy(col("hybrid_score").desc()) \
                    .limit(10)
            else:
                # Nếu user chưa có phim thích, dùng thuần ALS
                final_recs = flat_als.withColumn("hybrid_score", col("als_score")) \
                    .orderBy(col("hybrid_score").desc()) \
                    .limit(10)

            # Join với movie metadata để hiển thị
            result = final_recs.join(movies_df, on="movieId") \
                .select("title", "genres", "hybrid_score")
            
            result.show(n=10, truncate=False)

    except Exception as e:
        print(f"Lỗi: {e}")
        import traceback
        traceback.print_exc()
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
import os
import shutil
import kagglehub
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS, ALSModel
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.functions import col, explode

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
    dataset_dir = os.path.join(current_dir, "movielens_20m_data")

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
    return rating_path, movie_path

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
    print(f"--- Đã lưu mô hình tại: {model_path} ---")
    return model

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    model_save_path = os.path.join(root_dir, "models", "als_movie_model")
    
    spark = init_spark()
    
    try:
        # Bước 1: Tải dữ liệu về thư mục project
        rating_path, movie_path = get_data_and_prepare_paths()
        
        # Bước 2: Huấn luyện hoặc Load model
        if not os.path.exists(model_save_path):
            model = train_and_save(spark, rating_path, model_save_path)
        else:
            print("--- Đang tải mô hình đã có sẵn... ---")
            model = ALSModel.load(model_save_path)

        # Bước 3: Dự đoán và Gợi ý
        # Nạp thêm file movie.csv để biết tên phim
        movies_df = spark.read.csv(movie_path, header=True, inferSchema=True)

        print("\n--- Tiến hành gợi ý 10 phim cho 3 người dùng (ID: 1, 2, 3) ---")
        user_ids = [1, 2, 3]
        users_df = spark.createDataFrame([(i,) for i in user_ids], ["userId"])
        
        # Tạo gợi ý
        recommendations = model.recommendForUserSubset(users_df, 10)

        # Xử lý kết quả để hiển thị đẹp hơn
        # Explode danh sách gợi ý thành các dòng riêng biệt
        flat_recs = recommendations.withColumn("rec", explode("recommendations")) \
            .select("userId", col("rec.movieId"), col("rec.rating"))

        # Join với movies_df để lấy tiêu đề phim
        final_output = flat_recs.join(movies_df, on="movieId") \
            .select("userId", "title", "rating") \
            .orderBy("userId", col("rating").desc())

        final_output.show(n=30, truncate=False)

    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
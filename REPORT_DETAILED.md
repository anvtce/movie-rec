# BÁO CÁO CHI TIẾT ĐỒ ÁN: HỆ THỐNG GỢI Ý PHIM HYBRID TRÊN NỀN TẢNG BIG DATA

## 1. Xác định vấn đề (Problem Statement)
**Câu hỏi nghiên cứu:** Làm thế nào để xây dựng một hệ thống gợi ý phim cá nhân hóa cho hàng triệu người dùng với tập dữ liệu lớn, đảm bảo tính chính xác và giải quyết được vấn đề "Cold Start" (người dùng mới/phim mới)?

**Ý nghĩa thực tiễn:** 
- Giúp người dùng tìm thấy nội dung phù hợp trong kho dữ liệu khổng lồ.
- Tăng trải nghiệm người dùng và thời gian lưu trú trên nền tảng.
- Tối ưu hóa việc phân phối nội dung phim.

## 2. Thiết kế dữ liệu (Data Design)
### 2.1. Nguồn dữ liệu
- **Tên tập dữ liệu:** MovieLens 20M.
- **Định dạng:** CSV.
- **Các file chính:**
    - `rating.csv`: Lịch sử đánh giá (userId, movieId, rating, timestamp).
    - `movie.csv`: Thông tin phim (movieId, title, genres).
    - `genome_scores.csv`: Đặc điểm chi tiết của phim (movieId, tagId, relevance).
    - `genome_tags.csv`: Danh mục các thẻ đặc điểm (tagId, tag).

### 2.2. Đặc trưng Big Data (3Vs)
- **Volume (Khối lượng):** Hơn 20 triệu bản ghi đánh giá, yêu cầu khả năng xử lý phân tán.
- **Variety (Đa dạng):** Kết hợp dữ liệu định lượng (điểm rating) và định tính (thể loại, thẻ genome).
- **Velocity (Tốc độ):** Khả năng tính toán ma trận tương đồng trên quy mô lớn trong thời gian ngắn nhờ Spark.

## 3. Tiền xử lý dữ liệu (Data Preprocessing)
**Luồng biến đổi dữ liệu:**
`Raw CSV` $\rightarrow$ `Spark DataFrame` $\rightarrow$ `Cleaning/Casting` $\rightarrow$ `Feature Engineering` $\rightarrow$ `Model Input`

**Các bước thực hiện:**
1. **Chuẩn hóa:** Ép kiểu `userId`, `movieId` sang Integer và `rating` sang Float.
2. **Lọc nhiễu:** Loại bỏ các giá trị null (dropna).
3. **Phân tách:** Chia dữ liệu theo tỷ lệ 80% huấn luyện (training) và 20% kiểm thử (test).
4. **Xây dựng Profile:** Pivot dữ liệu từ `genome_scores.csv` để tạo vector đặc điểm cho mỗi bộ phim (chỉ lấy các tag có relevance > 0.5).

## 4. Phân tích và Xử lý dữ liệu (Data Analysis)
Hệ thống áp dụng mô hình **Hybrid Recommendation** kết hợp hai phương pháp:

### 4.1. Collaborative Filtering (ALS)
- **Thuật toán:** Alternating Least Squares (ALS).
- **Cơ chế:** Phân rã ma trận User-Item thành hai ma trận đặc trưng (Latent Factors).
- **Mục tiêu:** Dự đoán điểm rating mà người dùng có thể sẽ cho một bộ phim dựa trên hành vi của những người dùng tương tự.

### 4.2. Content-Based Filtering (Genome-based)
- **Thuật toán:** Cosine Similarity / Relevance Sum.
- **Cơ chế:** Tính toán độ tương đồng giữa vector đặc điểm (Genome) của phim người dùng thích nhất với tất cả các phim khác.
- **Mục tiêu:** Gợi ý những phim có "DNA" tương đồng về nội dung.

### 4.3. Chiến lược Hybrid
Kết hợp điểm số theo trọng số:
$$Score_{final} = 0.7 \times Score_{ALS} + 0.3 \times Score_{CBF}$$
*Chiến lược này giúp cân bằng giữa sự bất ngờ (từ ALS) và sự chính xác về nội dung (từ CBF).*

## 5. Kết quả và Demo
- **Kết quả:** Hệ thống trả về Top-10 phim gợi ý cho mỗi người dùng.
- **Minh chứng:** 
    - User 1: Gợi ý các phim hành động/viễn tưởng dựa trên lịch sử xem.
    - User mới: Hệ thống tự động chuyển sang chế độ ALS hoặc gợi ý phim phổ biến.
- **Công cụ sử dụng:** PySpark (SparkSession, MLlib), Python, KaggleHub.

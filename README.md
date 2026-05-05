# Movie Recommendation System

## Mục đích
Dự án này là một hệ thống gợi ý phim (movie recommendation system) dùng dữ liệu MovieLens 20M.
Nó xây dựng mô hình hybrid kết hợp giữa:
- Collaborative Filtering (ALS) trên `rating.csv`
- Content-Based Recommendation trên `genome_scores.csv`

## Dữ liệu sử dụng
Thư mục dữ liệu nằm ở `movielens_20m_data/` và bao gồm:
- `rating.csv`: dữ liệu user đánh giá phim (`userId`, `movieId`, `rating`)
- `movie.csv`: metadata phim như `title`, `genres`
- `genome_scores.csv`: tag và độ liên quan (`relevance`) từng movie với mỗi tag

## Khởi tạo môi trường
Dự án có thể chạy trong môi trường ảo Python (`venv`) hoặc với `uv` nếu đã cài.

### 1. Tạo và kích hoạt `venv`
```bash
cd /Users/ilongggg/zzz/pet/movie_rec_system
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Cài dependencies
```bash
python -m pip install --upgrade pip
python -m pip install numpy pyspark kagglehub
```

## Chạy chương trình

### Cách 1: Dùng `uv`
Nếu đã cài `uv`, chạy:
```bash
uv run src/main.py
```

### Cách 2: Dùng `python`
Nếu dùng Python trực tiếp, chạy:
```bash
python src/main.py
```

## Lưu ý
- `src/main.py` sẽ tự tải dữ liệu MovieLens 20M từ Kaggle bằng `kagglehub`.
- Dữ liệu sẽ được lưu vào thư mục `movielens_20m_data/` nếu chưa tồn tại.
- Mô hình ALS sẽ được lưu tại `src/models/als_movie_model/`.
- Nếu muốn chạy lại từ đầu, xóa thư mục `src/models/als_movie_model/` rồi chạy lại.

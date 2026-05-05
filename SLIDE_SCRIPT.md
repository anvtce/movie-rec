# KỊCH BẢN SLIDE: HỆ THỐNG GỢI Ý PHIM HYBRID (BIG DATA)

*Hướng dẫn: Copy nội dung này vào các công cụ AI tạo slide (như Gamma.app, Tome.app, hoặc ChatGPT với plugin Slide)*

---

## Slide 1: Tiêu đề
- **Tiêu đề chính:** Xây dựng Hệ thống Gợi ý Phim Hybrid trên nền tảng Big Data
- **Phụ đề:** Giải pháp cá nhân hóa trải nghiệm người dùng với PySpark và MovieLens 20M
- **Thông tin:** [Tên của bạn] - Đồ án cuối khóa Dữ liệu lớn

## Slide 2: Đặt vấn đề & Mục tiêu
- **Vấn đề:** Sự quá tải thông tin (Information Overload). Người dùng khó tìm thấy phim đúng gu trong hàng triệu lựa chọn.
- **Thách thức:** Vấn đề "Cold Start" (Người dùng mới không có lịch sử xem).
- **Mục tiêu:** Xây dựng hệ thống gợi ý kết hợp (Hybrid) để tăng độ chính xác và tính đa dạng.

## Slide 3: Tổng quan Dữ liệu (The 3Vs of Big Data)
- **Volume:** 20 triệu lượt đánh giá $\rightarrow$ Yêu cầu xử lý phân tán.
- **Variety:** Kết hợp Rating (Số), Genres (Chuỗi), Genome Scores (Vector đặc điểm).
- **Velocity:** Tốc độ xử lý ma trận lớn bằng Apache Spark.
- **Nguồn:** Dataset MovieLens 20M từ Kaggle.

## Slide 4: Kiến trúc Hệ thống (System Architecture)
- **Sơ đồ luồng:** 
    `Dữ liệu thô` $\rightarrow$ `Tiền xử lý (Spark)` $\rightarrow$ `Mô hình Hybrid` $\rightarrow$ `Kết quả gợi ý`.
- **Công cụ:** Python, PySpark, MLlib.

## Slide 5: Phương pháp 1 - Collaborative Filtering (ALS)
- **Khái niệm:** Gợi ý dựa trên hành vi cộng đồng.
- **Thuật toán:** Alternating Least Squares (ALS).
- **Điểm mạnh:** Tìm ra những phim "bất ngờ" nhưng phù hợp.
- **Hình ảnh minh họa:** Ma trận User-Item.

## Slide 6: Phương pháp 2 - Content-Based Filtering (Genome)
- **Khái niệm:** Gợi ý dựa trên "DNA" của phim.
- **Thuật toán:** Tính tương đồng vector đặc điểm (Genome Scores).
- **Điểm mạnh:** Giải quyết Cold Start, hiểu sâu nội dung phim.
- **Hình ảnh minh họa:** Vector đặc điểm phim.

## Slide 7: Mô hình Hybrid - Sự kết hợp hoàn hảo
- **Công thức:** $Score = 0.7 \times ALS + 0.3 \times CBF$.
- **Tại sao lại là Hybrid?** 
    - Tăng độ chính xác.
    - Giảm thiểu nhược điểm của từng phương pháp đơn lẻ.
    - Tối ưu hóa trải nghiệm người dùng.

## Slide 8: Demo & Kết quả
- **Kịch bản demo:** Gợi ý cho User ID 1, 2, 3.
- **Kết quả:** Danh sách Top-10 phim kèm thể loại và điểm số.
- **Minh chứng:** Sự khác biệt giữa gợi ý thuần ALS và gợi ý Hybrid.

## Slide 9: Kết luận & Hướng phát triển
- **Kết luận:** Hệ thống đáp ứng tốt yêu cầu xử lý dữ liệu lớn và gợi ý chính xác.
- **Hướng phát triển:** 
    - Tích hợp API IMDb/TMDb để lấy poster.
    - Triển khai lên Cloud (AWS/Azure).
    - Áp dụng Deep Learning (Neural Collaborative Filtering).

## Slide 10: Q&A
- Cảm ơn thầy và các bạn đã lắng nghe.
- Sẵn sàng trả lời câu hỏi.

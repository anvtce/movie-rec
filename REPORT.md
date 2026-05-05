# Báo Cáo Dự Án: Hệ Thống Gợi Ý Phim Thông Minh (Movie Recommendation System)

## 🌟 Giới thiệu chung
Bạn đã bao giờ tự hỏi tại sao Netflix hay YouTube lại biết chính xác bạn muốn xem gì tiếp theo? Dự án này xây dựng một "bộ não" tương tự cho kho phim MovieLens 20M, giúp người dùng tìm thấy những bộ phim yêu thích một cách tự động và chính xác.

## 🎯 Mục tiêu của dự án
Thay vì để người dùng tự bơi trong hàng ngàn bộ phim, hệ thống này đóng vai trò như một "chuyên gia tư vấn phim" ảo, đưa ra danh sách 10 bộ phim phù hợp nhất cho mỗi cá nhân dựa trên sở thích riêng của họ.

## 🛠 Cách hệ thống "tư duy" (Giải thích đơn giản)
Để gợi ý phim chính xác, tôi không chỉ dùng một cách mà kết hợp **hai phương pháp tư duy** khác nhau (gọi là mô hình **Hybrid - Lai**):

### 1. Tư duy theo "Đám đông" (Collaborative Filtering)
*   **Cách hoạt động:** "Nếu bạn thích phim A, và một người khác cũng thích phim A và phim B, thì có khả năng cao là bạn cũng sẽ thích phim B."
*   **Ưu điểm:** Tìm ra những bộ phim bất ngờ mà bạn chưa từng biết nhưng những người có gu giống bạn đều thích.
*   **Nhược điểm:** Gặp khó khăn với những người dùng mới (chưa xem phim nào) hoặc phim mới ra mắt (chưa ai đánh giá).

### 2. Tư duy theo "Đặc điểm" (Content-Based Filtering)
*   **Cách hoạt động:** "Bạn thích phim *Inception* vì nó có đặc điểm là 'hack não', 'giấc mơ' và 'hành động'. Tôi sẽ tìm cho bạn những phim khác cũng có các đặc điểm tương tự."
*   **Ưu điểm:** Hiểu sâu về nội dung phim thông qua dữ liệu "Genome" (mã gene của phim) — bao gồm các thẻ mô tả chi tiết về phong cách, chủ đề.
*   **Nhược điểm:** Có xu hướng gợi ý những phim quá giống nhau, thiếu sự bất ngờ.

### 🚀 Sự kết hợp hoàn hảo (Hybrid Model)
Hệ thống hiện tại kết hợp cả hai: **70% dựa trên hành vi đám đông** và **30% dựa trên đặc điểm nội dung**. Điều này giúp gợi ý vừa chính xác, vừa đa dạng, đồng thời giải quyết được vấn đề "người dùng mới".

## 📊 Quy trình xử lý dữ liệu
1.  **Thu thập:** Tải dữ liệu từ Kaggle (hàng triệu lượt đánh giá, thông tin phim, thẻ mô tả).
2.  **Phân tích:** Sử dụng công nghệ **Apache Spark** để xử lý khối lượng dữ liệu khổng lồ một cách nhanh chóng.
3.  **Huấn luyện:** Dạy cho máy tính hiểu mối quan hệ giữa Người dùng $\leftrightarrow$ Bộ phim $\leftrightarrow$ Đặc điểm nội dung.
4.  **Gợi ý:** Xuất ra danh sách phim kèm theo thể loại và điểm số tin cậy.

## 📈 Kết quả mong đợi
*   **Cá nhân hóa:** Mỗi người dùng nhận được một danh sách phim khác nhau.
*   **Độ chính xác cao:** Giảm thiểu việc gợi ý những phim không đúng gu.
*   **Khám phá:** Giúp người dùng tìm thấy những "viên ngọc quý" ẩn trong kho dữ liệu lớn.

---
*Dự án được phát triển bằng ngôn ngữ Python và công nghệ xử lý dữ liệu lớn PySpark.*

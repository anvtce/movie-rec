# HỆ THỐNG GỢI Ý PHIM HYBRID

**Trên nền tảng Big Data — Apache Spark & MovieLens 20M**

MSB10CT_BDA501

GV: NGÔ BÁ HÙNG

- Nguyễn Trần Nhân Trí (Nhóm trưởng)
- Bùi Ngọc Minh Tâm
- Võ Thành An

---

## ĐẶT VẤN ĐỀ

| Quá tải lựa chọn | Cold Start | Cá nhân hóa kém |
|---|---|---|
| Người dùng mất nhiều thời gian tìm nội dung phù hợp giữa hàng triệu phim. | Hệ thống truyền thống không gợi ý được cho người dùng hoặc phim mới. | Chỉ dựa xu hướng phổ biến, thiếu gợi ý theo sở thích cá nhân sâu. |

---

## MỤC TIÊU

1. **Hybrid Recommender** — Kết hợp Collaborative Filtering và Content-Based để gợi ý phim chính xác hơn.
2. **Xử lý Big Data** — Sử dụng PySpark để xử lý khối lượng dữ liệu lớn hiệu quả.
3. **Cá nhân hóa** — Tăng độ chính xác và khả năng cá nhân hóa gợi ý cho từng người dùng.

---

## CÔNG NGHỆ & DỮ LIỆU SỬ DỤNG

- **Apache Spark / PySpark** — Framework xử lý phân tán cho dữ liệu lớn.
- **MovieLens 20M** — Bộ dữ liệu 20 triệu đánh giá phim thực tế.
- **ALS (Alternating Least Squares)** — Thuật toán Collaborative Filtering tối ưu cho dữ liệu thưa.
- **Content-Based Filtering** — Phân tích đặc trưng phim để gợi ý theo sở thích.

---

## PHƯƠNG PHÁP HYBRID

Hệ thống kết hợp hai phương pháp để bù trừ điểm yếu của nhau.

1. **ALS Collaborative** — Phân tích hành vi người dùng.
2. **Content-Based** — Phân tích đặc trưng phim.
3. **Kết hợp Kết quả** — Gộp đề xuất tăng hiệu quả.

> Mô hình Hybrid cân bằng giữa xu hướng cộng đồng và sở thích cá nhân.

---

## QUY TRÌNH XỬ LÝ DỮ LIỆU

1. **Thu thập** — Tải dữ liệu MovieLens 20M.
2. **Tiền xử lý** — Làm sạch dữ liệu bằng Spark DataFrame.
3. **Huấn luyện ALS** — Xây dựng mô hình Collaborative Filtering.
4. **Kết hợp** — Tích hợp Content-Based Filtering.
5. **Đánh giá** — Kiểm tra và lưu mô hình.

---

## DEMO

---

## KẾT QUẢ ĐẠT ĐƯỢC

| Xử lý hiệu quả | Gợi ý phù hợp | Giảm Cold Start |
|---|---|---|
| Hệ thống xử lý dữ liệu lớn hiệu quả với Apache Spark. | Đề xuất phim phù hợp với sở thích cá nhân người dùng. | Giảm vấn đề Cold Start nhờ mô hình Hybrid kết hợp. |

---

## HẠN CHẾ HIỆN TẠI

**Dữ liệu thưa (Sparse Data)**

Hệ thống vẫn gặp khó khăn khi dữ liệu đánh giá quá thưa — nhiều người dùng chưa đánh giá đủ phim để tạo gợi ý chính xác.

> Đây là thách thức phổ biến của hệ thống gợi ý dựa trên Collaborative Filtering.

---

## HƯỚNG PHÁT TRIỂN TƯƠNG LAI

- **Deep Learning** — Tích hợp mô hình học sâu để nâng cao chất lượng gợi ý.
- **Real-time Streaming** — Xử lý dữ liệu thời gian thực để cập nhật gợi ý ngay lập tức.

---

## CẢM ƠN MỌI NGƯỜI ĐÃ LẮNG NGHE <3

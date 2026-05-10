# NỘI DUNG THUYẾT TRÌNH — HỆ THỐNG CẢNH BÁO SỚM AN NINH MẠNG

> Slides 1–3 | Mục tiêu: ~2 phút

---

## SLIDE 1 — TRANG TIÊU ĐỀ (~15 giây)

Xin chào thầy và các bạn. Nhóm em xin trình bày đề tài **Xây dựng hệ thống cảnh báo sớm rủi ro an ninh mạng bằng Apache Spark ML**. Em xin phép bắt đầu.

---

## SLIDE 2 — XÁC ĐỊNH VẤN ĐỀ (~1 phút)

UBND xã Mỹ An Hưng đang chuyển đổi số, toàn bộ dữ liệu công dân lưu trên máy chủ tập trung — điều này kéo theo rủi ro bị tấn công mạng ngày càng cao.

Vấn đề là: mỗi ngày hệ thống sinh ra **hàng chục nghìn dòng Log** — không ai có thể đọc hết để phát hiện bất thường kịp thời.

Nhóm em giải quyết bằng cách xây dựng một **"người gác cổng" tự động bằng AI** — tự học từ dữ liệu lịch sử và cảnh báo ngay khi phát hiện hành vi xâm nhập.

---

## SLIDE 3 — THIẾT KẾ YÊU CẦU DỮ LIỆU (~45 giây)

Để AI nhận diện được tấn công, nhóm thu thập **5 thông số** từ Log máy chủ:

- **Thời gian kết nối** — kéo dài bất thường có thể là dấu hiệu tải dữ liệu ngầm.
- **Số lần đăng nhập sai** — dấu hiệu rõ nhất của tấn công dò mật khẩu.
- **Dung lượng dữ liệu truyền tải** — quá lớn trong một phiên → nghi ngờ đánh cắp.
- **Tải trọng CPU** — tấn công thường làm hệ thống quá tải đột ngột.
- **Trạng thái VPN** — truy cập có đang ẩn danh không.

Mỗi dòng Log được gán nhãn **0 (bình thường)** hoặc **1 (nguy hiểm)** để huấn luyện AI.

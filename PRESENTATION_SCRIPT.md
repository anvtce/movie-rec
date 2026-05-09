# NỘI DUNG THUYẾT TRÌNH — HỆ THỐNG GỢI Ý PHIM HYBRID

> Slides 1–6 | Người thuyết trình: bạn gái | Mục tiêu: ~8 phút

---

## SLIDE 1 — TRANG TIÊU ĐỀ (~30 giây)

Xin chào thầy và các bạn. Nhóm 1 chúng em xin trình bày đồ án với chủ đề **Hệ thống gợi ý phim Hybrid trên nền tảng Big Data**.

Nhóm em gồm ba thành viên: Nhân Trí, Minh Tâm và Thành An. Em xin phép bắt đầu.

---

## SLIDE 2 — ĐẶT VẤN ĐỀ (~1.5 phút)

Chắc hẳn nhiều người trong chúng ta đã từng mở Netflix hay YouTube lên, nhìn hàng trăm bộ phim mà không biết xem gì — rồi cuối cùng mất cả chục phút chỉ để chọn phim. Đó chính là vấn đề **quá tải lựa chọn**.

Không chỉ vậy, với người mới đăng ký, hệ thống chưa biết gì về sở thích của họ, nên không thể gợi ý được gì phù hợp — đây gọi là vấn đề **Cold Start**, tức là "khởi động lạnh".

Và vấn đề thứ ba: nhiều hệ thống chỉ gợi ý những phim đang hot, phổ biến với đại đa số — nhưng mỗi người có sở thích khác nhau, nên cách đó không thực sự **cá nhân hóa** được.

Ba vấn đề này là lý do nhóm em thực hiện đề tài này — xây dựng một hệ thống gợi ý thông minh hơn, cá nhân hơn.

---

## SLIDE 3 — MỤC TIÊU (~1 phút)

Từ những vấn đề đó, nhóm em đặt ra ba mục tiêu chính.

**Một là**, xây dựng hệ thống gợi ý kết hợp — Hybrid — để phát huy điểm mạnh của từng phương pháp và bù đắp điểm yếu cho nhau.

**Hai là**, xử lý được bộ dữ liệu lớn — hơn 20 triệu lượt đánh giá phim — bằng công nghệ Apache Spark, vì các công cụ thông thường không đáp ứng được quy mô này.

**Ba là**, đảm bảo mỗi người dùng nhận được danh sách phim gợi ý riêng, phù hợp với sở thích cá nhân của họ.

---

## SLIDE 4 — CÔNG NGHỆ & DỮ LIỆU SỬ DỤNG (~1.5 phút)

Về công nghệ, nhóm em dùng **Apache Spark** — đây là nền tảng xử lý dữ liệu lớn phổ biến nhất hiện nay, cho phép chia nhỏ công việc và xử lý song song, nên rất nhanh dù dữ liệu khổng lồ.

Về dữ liệu, nhóm sử dụng **MovieLens 20M** — một bộ dữ liệu thực tế gồm hơn 20 triệu lượt người dùng đánh giá phim. Bộ dữ liệu này đủ lớn và đủ đa dạng để thể hiện ba đặc trưng của Big Data mà môn học đề cập: **khối lượng lớn**, **đa dạng định dạng**, và **cần xử lý nhanh**.

Về thuật toán, nhóm dùng hai phương pháp chính sẽ được giải thích ở slide tiếp theo — một phương pháp dựa trên **hành vi người dùng**, một phương pháp dựa trên **nội dung bộ phim**.

---

## SLIDE 5 — PHƯƠNG PHÁP HYBRID (~2 phút)

Đây là phần cốt lõi của hệ thống.

**Phương pháp thứ nhất** là Collaborative Filtering — hay còn gọi là "lọc cộng tác". Ý tưởng đơn giản: nếu bạn và một người khác có cùng sở thích xem phim trong quá khứ, thì phim mà họ thích nhưng bạn chưa xem — nhiều khả năng bạn cũng sẽ thích. Hệ thống phân tích toàn bộ lịch sử đánh giá của hàng triệu người dùng để tìm ra những mẫu như vậy.

**Phương pháp thứ hai** là Content-Based Filtering — lọc theo nội dung. Thay vì nhìn vào hành vi người dùng, phương pháp này nhìn vào bản thân bộ phim: thể loại, chủ đề, không khí... Nếu bạn từng thích một bộ phim nào đó, hệ thống sẽ tìm những phim có nội dung tương tự.

**Hai phương pháp được kết hợp lại** theo tỉ lệ 70% từ hành vi người dùng và 30% từ nội dung phim. Cách kết hợp này giúp hệ thống vừa gợi ý được những phim bất ngờ mà cộng đồng yêu thích, vừa đảm bảo phù hợp với sở thích cá nhân.

Đặc biệt, nếu người dùng hoàn toàn mới, chưa có lịch sử xem phim, hệ thống tự động chỉ dùng phương pháp thứ nhất — đảm bảo vẫn có kết quả gợi ý, không bị "tắt máy".

---

## SLIDE 6 — QUY TRÌNH XỬ LÝ DỮ LIỆU (~1.5 phút)

Toàn bộ quy trình hoạt động qua 5 bước.

**Bước 1 — Thu thập:** Dữ liệu MovieLens 20M được tải tự động về máy khi chạy hệ thống lần đầu.

**Bước 2 — Làm sạch:** Dữ liệu thô được lọc bỏ các giá trị thiếu, chuẩn hóa định dạng, rồi chia thành 80% để huấn luyện và 20% để kiểm tra độ chính xác.

**Bước 3 — Huấn luyện:** Mô hình học từ 80% dữ liệu đó. Kết quả được lưu lại, nên những lần chạy sau không cần học lại từ đầu — tiết kiệm thời gian đáng kể.

**Bước 4 — Kết hợp:** Hệ thống xây dựng thêm phần phân tích nội dung phim, kết hợp với mô hình vừa học được để tạo ra gợi ý Hybrid.

**Bước 5 — Cho kết quả:** Hệ thống xuất ra danh sách Top 10 phim gợi ý cho mỗi người dùng, kèm tên phim và thể loại.

Tiếp theo, nhóm em sẽ demo trực tiếp để thầy thấy hệ thống hoạt động như thế nào.

---

*→ Tiếp theo: **DEMO** hệ thống thực tế.*

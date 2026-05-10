# FAQ — CÂU HỎI THƯỜNG GẶP KHI THUYẾT TRÌNH

> Dành cho toàn bộ nhóm tham khảo trước khi thuyết trình

---

## NHÓM 1 — Câu hỏi về Vấn đề & Ý nghĩa

---

**Q: Tại sao nhóm chọn đề tài này? Thực tế nó có ứng dụng không?**

> Hệ thống gợi ý là một trong những thành phần cốt lõi của các nền tảng lớn như Netflix, Spotify, YouTube — ước tính 80% nội dung được xem trên Netflix đến từ hệ thống gợi ý. Nhóm chọn đề tài này vì nó vừa gắn với thực tiễn, vừa là bài toán điển hình của Big Data: dữ liệu lớn, cần xử lý nhanh, và yêu cầu thuật toán phức tạp.

---

**Q: Cold Start là gì? Nhóm giải quyết nó như thế nào?**

> Cold Start xảy ra khi hệ thống không có đủ thông tin về người dùng hoặc bộ phim để đưa ra gợi ý. Với người dùng mới chưa có lịch sử xem phim, nhóm xử lý bằng cách: nếu không tìm được phim yêu thích để làm cơ sở cho Content-Based, hệ thống tự động chuyển sang chỉ dùng ALS — lúc này ALS dựa vào hành vi trung bình của cộng đồng để gợi ý. Đây là cách giải quyết thực dụng, đảm bảo hệ thống luôn có output.

---

## NHÓM 2 — Câu hỏi về Dữ liệu

---

**Q: Tại sao chọn MovieLens 20M mà không dùng bộ dữ liệu khác?**

> MovieLens 20M là bộ dữ liệu chuẩn mực trong nghiên cứu hệ thống gợi ý, được cung cấp bởi GroupLens Research (Đại học Minnesota). Nó có đủ quy mô để thể hiện thách thức Big Data thực sự (20 triệu bản ghi), có cấu trúc rõ ràng, và có bộ Genome Data — thông tin đặc trưng nội dung phim — rất phù hợp để xây dựng phần Content-Based Filtering.

---

**Q: 3V của Big Data là gì? Bộ dữ liệu này thể hiện 3V như thế nào?**

> Ba đặc trưng của Big Data: **Volume** (khối lượng) — hơn 20 triệu bản ghi rating, vượt ngưỡng xử lý thông thường; **Variety** (đa dạng) — kết hợp dữ liệu số (điểm đánh giá), văn bản (thể loại phim), và ma trận đặc trưng (genome); **Velocity** (tốc độ) — cần công cụ xử lý song song như Spark thay vì chạy tuần tự.

---

**Q: Dữ liệu có được làm sạch không? Làm sạch như thế nào?**

> Có. Nhóm thực hiện ba bước: lọc bỏ các dòng có giá trị thiếu, chuẩn hóa kiểu dữ liệu cho các cột ID và rating, và với genome data thì chỉ giữ lại các đặc trưng có độ liên quan cao — để giảm nhiễu và tăng tốc độ tính toán.

---

## NHÓM 3 — Câu hỏi về Thuật toán & Phương pháp

---

**Q: ALS là gì? Tại sao chọn ALS mà không dùng thuật toán khác?**

> ALS — Alternating Least Squares — là thuật toán Collaborative Filtering được tối ưu đặc biệt cho dữ liệu thưa (sparse data), tức là ma trận mà phần lớn các ô còn trống vì người dùng chỉ đánh giá một phần nhỏ số phim. ALS phân rã ma trận này thành hai ma trận nhỏ hơn đại diện cho đặc trưng ẩn của người dùng và bộ phim, từ đó dự đoán các ô còn thiếu. Lý do chọn ALS: được tích hợp sẵn trong Spark MLlib, tối ưu cho xử lý phân tán, và phù hợp với đặc điểm thưa của dữ liệu MovieLens.

---

**Q: Tại sao chọn tỉ lệ 70% ALS và 30% Content-Based? Có cơ sở nào không?**

> Tỉ lệ này được chọn dựa trên nguyên tắc: ALS khai thác hành vi tập thể của hàng triệu người dùng nên tín hiệu mạnh hơn, trong khi Content-Based chỉ dựa vào một bộ phim yêu thích của cá nhân nên tín hiệu yếu hơn và có thể bị nhiễu. Trọng số 70/30 đảm bảo ưu tiên tín hiệu xã hội đồng thời không bỏ qua đặc điểm nội dung. Trong thực tế, tỉ lệ tối ưu cần được xác định bằng thực nghiệm (cross-validation), đây là một hướng cải thiện của nhóm.

---

**Q: Collaborative Filtering và Content-Based khác nhau như thế nào? Ưu nhược điểm?**

> **Collaborative Filtering** nhìn vào *người dùng*: "những người giống bạn thích gì". Ưu điểm: khám phá được phim bất ngờ, không cần biết nội dung phim. Nhược điểm: bị Cold Start với người dùng mới, cần nhiều dữ liệu.
>
> **Content-Based** nhìn vào *bộ phim*: "phim nào giống phim bạn đã thích". Ưu điểm: không bị Cold Start với phim mới, giải thích được lý do gợi ý. Nhược điểm: dễ bị "bẫy bong bóng" — chỉ gợi ý những gì đã quen, ít khám phá mới.
>
> Kết hợp hai phương pháp giúp bù trừ nhược điểm cho nhau.

---

**Q: Tại sao chia dữ liệu theo tỉ lệ 80% huấn luyện và 20% kiểm tra? Không phải 70/30 hay 90/10?**

> Đây là tỉ lệ phổ biến và được chấp nhận rộng rãi trong Machine Learning vì lý do thực tế: **80% đủ lớn** để mô hình học được các mẫu phức tạp trong dữ liệu — nếu train ít hơn (ví dụ 70%), mô hình dễ bị underfitting; **20% đủ đại diện** để đánh giá khách quan — nếu test quá ít (ví dụ 10%), kết quả đánh giá dễ bị may rủi, không phản ánh đúng hiệu năng thực tế. Với bộ dữ liệu 20 triệu bản ghi, 20% tương đương 4 triệu bản ghi kiểm tra — con số rất lớn, đảm bảo độ tin cậy thống kê cao.

---

**Q: Hệ thống đánh giá độ chính xác bằng cách nào?**

> Nhóm dùng chỉ số **RMSE** (Root Mean Squared Error — căn bậc hai của sai số bình phương trung bình). Mô hình được huấn luyện trên 80% dữ liệu, sau đó dự đoán trên 20% còn lại và so sánh với điểm đánh giá thực tế. RMSE càng nhỏ thì mô hình dự đoán càng chính xác.

---

## NHÓM 4 — Câu hỏi về Công nghệ

---

**Q: Tại sao cần Apache Spark? Dùng Python thông thường không được sao?**

> Python thông thường (pandas, numpy) xử lý dữ liệu trên một máy và bị giới hạn bởi RAM. Với 20 triệu bản ghi, dữ liệu có thể chiếm hàng chục GB RAM — vượt khả năng của máy tính thông thường. Spark cho phép chia nhỏ dữ liệu và xử lý song song trên nhiều lõi (hoặc nhiều máy), đồng thời có thư viện MLlib tích hợp sẵn các thuật toán machine learning tối ưu cho dữ liệu lớn như ALS.

---

**Q: Hệ thống có thể mở rộng lên dữ liệu lớn hơn (hàng tỉ bản ghi) không?**

> Về lý thuyết, kiến trúc Spark cho phép mở rộng ngang (scale-out) bằng cách thêm máy chủ vào cluster mà không cần thay đổi code. Tuy nhiên, với phiên bản hiện tại chạy local trên một máy, giới hạn là tài nguyên phần cứng. Để triển khai thực tế ở quy mô lớn hơn, cần chuyển sang môi trường Spark cluster (AWS EMR, Google Dataproc...).

---

## NHÓM 5 — Câu hỏi về Hạn chế & Hướng phát triển

---

**Q: Hạn chế lớn nhất của hệ thống hiện tại là gì?**

> Hai hạn chế chính: **Thứ nhất**, vấn đề Sparse Data — nhiều người dùng chỉ đánh giá rất ít phim, khiến mô hình khó học được đặc trưng chính xác của họ. **Thứ hai**, phần Content-Based hiện tính độ tương đồng theo cách đơn giản (tổng relevance các tag chung), chưa dùng phép tính tinh tế hơn như Cosine Similarity trên toàn vector — đây là điểm có thể cải thiện về sau.

---

**Q: Hướng phát triển tiếp theo của nhóm là gì?**

> Nhóm đề xuất hai hướng chính: **Deep Learning** — thay ALS bằng các mô hình mạng nơ-ron như Neural Collaborative Filtering (NCF) hoặc Transformer-based để nắm bắt mối quan hệ phi tuyến phức tạp hơn; và **Real-time Streaming** — tích hợp Spark Streaming hoặc Kafka để cập nhật gợi ý ngay khi người dùng vừa xem xong một bộ phim, thay vì gợi ý theo batch như hiện tại.

---

**Q: So với Netflix thực tế thì hệ thống của nhóm còn thiếu gì?**

> Khá nhiều. Netflix sử dụng hàng trăm tín hiệu: thời điểm xem, thiết bị, thời gian dừng xem, xem lại bao nhiêu lần, thậm chí tốc độ cuộn tay trong menu... Hệ thống của nhóm chỉ dùng điểm đánh giá (rating) và đặc trưng nội dung (genome). Ngoài ra, Netflix cũng cá nhân hóa đến cả thumbnail hiển thị cho từng người dùng — đây là mức độ mà một đồ án sinh viên chưa thể đạt tới.

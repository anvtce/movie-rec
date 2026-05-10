# FAQ — CÂU HỎI THƯỜNG GẶP KHI THUYẾT TRÌNH

> An ninh mạng — Hệ thống cảnh báo sớm Log truy cập

---

## NHÓM 1 — Câu hỏi về Vấn đề & Ý nghĩa

---

**Q: Tại sao lại chọn bối cảnh UBND xã? Quy mô nhỏ như vậy có cần đến AI không?**

> Đây là lý do thực tế: các cơ quan hành chính cấp xã thường không có đội ngũ IT chuyên trách đủ lớn để giám sát hệ thống 24/7. Chính vì vậy, một hệ thống tự động hóa việc phát hiện tấn công lại càng cần thiết hơn ở quy mô nhỏ — nơi con người không thể ngồi đọc Log liên tục. Ngoài ra, dữ liệu công dân ở cấp xã cũng là dữ liệu nhạy cảm cần được bảo vệ nghiêm túc.

---

**Q: Tấn công Brute-force là gì? Nguy hiểm như thế nào?**

> Brute-force là kiểu tấn công dò mật khẩu bằng cách thử hàng loạt tổ hợp liên tục cho đến khi đúng. Nguy hiểm ở chỗ nó không cần kỹ năng cao — chỉ cần phần mềm tự động chạy liên tục. Nếu không có hệ thống phát hiện, kẻ tấn công có thể thử hàng nghìn lần mà quản trị viên không hay biết cho đến khi tài khoản đã bị chiếm.

---

## NHÓM 2 — Câu hỏi về Dữ liệu

---

**Q: Dữ liệu Log lấy từ đâu? Có phải dữ liệu thật không?**

> Dữ liệu sử dụng trong đề tài là dữ liệu mô phỏng (synthetic data) được tạo ra dựa trên đặc điểm của Log hệ thống thực tế. Trong triển khai thực tế, dữ liệu sẽ được thu thập trực tiếp từ Log máy chủ của đơn vị — ví dụ như Log SSH, Log web server, hoặc Log hệ thống Windows/Linux.

---

**Q: Tại sao chỉ chọn 5 thông số đó? Có thiếu thông tin không?**

> 5 thông số được chọn vì đây là những tín hiệu rõ ràng và đo lường được nhất từ Log hệ thống, đồng thời bao phủ được các hình thức tấn công phổ biến nhất: dò mật khẩu (Failed_Logins), đánh cắp dữ liệu (Data_Size), chiếm dụng tài nguyên (Sys_Load), kết nối ẩn danh (Is_VPN) và kết nối kéo dài bất thường (Duration). Trong thực tế có thể bổ sung thêm địa chỉ IP, múi giờ truy cập, hay tần suất yêu cầu — đây là hướng mở rộng của đề tài.

---

**Q: Nhãn 0 và 1 được gán như thế nào? Có chính xác không?**

> Trong bộ dữ liệu mô phỏng, nhãn được gán theo quy tắc rõ ràng: các bản ghi có số lần đăng nhập sai cao, dung lượng truyền tải bất thường hoặc CPU quá tải được gán nhãn 1 (nguy hiểm), còn lại là 0 (bình thường). Trong môi trường thực tế, việc gán nhãn cần được thực hiện bởi chuyên gia bảo mật dựa trên các sự cố đã xảy ra — đây là bước quan trọng nhất quyết định chất lượng mô hình.

---

## NHÓM 3 — Câu hỏi về Thuật toán & Phương pháp

---

**Q: Tại sao chọn Logistic Regression mà không dùng thuật toán khác như Random Forest hay SVM?**

> Logistic Regression được chọn vì phù hợp với bài toán phân loại nhị phân (0/1), dễ giải thích kết quả, và huấn luyện nhanh ngay cả khi dữ liệu lớn. Với bộ dữ liệu Log có 5 đặc trưng rõ ràng và ranh giới phân tách tương đối rõ giữa hai lớp, Logistic Regression đã cho kết quả tốt (AUC = 1.0). Trong thực tế dữ liệu phức tạp hơn, có thể cân nhắc Random Forest để xử lý các mối quan hệ phi tuyến.

---

**Q: AUC = 1.0 có nghĩa là gì? Tại sao lại đạt tuyệt đối như vậy?**

> AUC (Area Under the ROC Curve) đo khả năng phân biệt giữa hai lớp của mô hình, với giá trị từ 0.5 (ngẫu nhiên) đến 1.0 (hoàn hảo). Kết quả AUC = 1.0 đạt được vì dữ liệu mô phỏng có ranh giới phân tách rất rõ ràng giữa truy cập bình thường và tấn công — chẳng hạn, 10 lần đăng nhập sai và CPU 99% là tín hiệu quá rõ. Trong dữ liệu thực tế nhiễu hơn, AUC sẽ thấp hơn và đó mới là thách thức thực sự.

---

**Q: Cross-Validation là gì? Tại sao cần dùng?**

> Cross-Validation (xác thực chéo) là kỹ thuật đánh giá mô hình khách quan hơn bằng cách chia dữ liệu thành nhiều phần, luân phiên dùng từng phần làm tập kiểm tra. Nhóm dùng 3-fold cross-validation — nghĩa là dữ liệu được chia làm 3 phần, mô hình được huấn luyện và kiểm tra 3 lần với các phần khác nhau, sau đó lấy kết quả trung bình. Mục đích là tránh mô hình "học vẹt" một tập dữ liệu cố định, đảm bảo hiệu năng thực sự tổng quát hơn.

---

**Q: StandardScaler là gì? Tại sao phải chuẩn hóa dữ liệu?**

> Các thông số trong Log có đơn vị và thang đo rất khác nhau: Duration tính bằng giây (vài chục đến vài trăm), Data_Size tính bằng MB (có thể hàng nghìn), còn Failed_Logins chỉ là số nguyên nhỏ. Nếu không chuẩn hóa, thuật toán sẽ bị "lóa mắt" bởi những con số lớn và bỏ qua các thông số nhỏ nhưng quan trọng. StandardScaler đưa tất cả về cùng thang đo (trung bình = 0, độ lệch chuẩn = 1) để mô hình học đồng đều từ tất cả các đặc trưng.

---

**Q: Tại sao chia dữ liệu theo tỉ lệ 80% huấn luyện và 20% kiểm tra?**

> Đây là tỉ lệ phổ biến và được chấp nhận rộng rãi trong Machine Learning: 80% đủ để mô hình học được các mẫu phức tạp, tránh underfitting; 20% đủ đại diện để đánh giá khách quan, tránh kết quả may rủi. Trong thực tế, tỉ lệ tối ưu nên được xác định qua thực nghiệm — nhưng 80/20 là baseline tin cậy để bắt đầu.

---

## NHÓM 4 — Câu hỏi về Công nghệ

---

**Q: Tại sao dùng Apache Spark thay vì Python thông thường?**

> Python thông thường xử lý dữ liệu trên một luồng, trên một máy. Với Log hệ thống thực tế có thể lên đến hàng triệu dòng mỗi ngày, giải pháp đơn lẻ sẽ không đáp ứng được tốc độ cần thiết. Spark cho phép xử lý song song trên nhiều lõi CPU, đồng thời có thư viện MLlib tích hợp các thuật toán ML tối ưu cho dữ liệu lớn — bao gồm Logistic Regression, Pipeline, và CrossValidator mà nhóm đã sử dụng.

---

**Q: Pipeline trong Spark là gì?**

> Pipeline là cách tổ chức các bước xử lý thành một dây chuyền liên kết: đầu vào của bước sau là đầu ra của bước trước. Trong đề tài này, Pipeline gồm 3 bước nối tiếp: gom đặc trưng (VectorAssembler) → chuẩn hóa (StandardScaler) → huấn luyện (Logistic Regression). Ưu điểm: khi có dữ liệu mới cần dự đoán, chỉ cần chạy qua Pipeline một lần duy nhất thay vì thực hiện từng bước thủ công.

---

## NHÓM 5 — Câu hỏi về Hạn chế & Hướng phát triển

---

**Q: Hạn chế lớn nhất của hệ thống hiện tại là gì?**

> Hai hạn chế chính: **Thứ nhất**, dữ liệu mô phỏng quá "sạch" — trong thực tế, ranh giới giữa truy cập bình thường và tấn công mờ nhạt hơn nhiều, AUC sẽ không đạt 1.0 và cần cải thiện liên tục. **Thứ hai**, hệ thống hiện phân tích theo batch — nghĩa là phân tích trên tập dữ liệu đã thu thập, chưa phân tích được theo thời gian thực khi Log mới phát sinh.

---

**Q: Hướng phát triển tiếp theo là gì?**

> Hai hướng chính: **Real-time detection** — tích hợp Spark Streaming hoặc Kafka để phân tích Log ngay khi phát sinh, thay vì xử lý theo batch; và **mở rộng đặc trưng** — bổ sung thêm thông tin như địa chỉ IP, múi giờ, tần suất yêu cầu, đồng thời thử các thuật toán phức tạp hơn như Random Forest hay Isolation Forest cho dữ liệu thực tế nhiễu hơn.

---

**Q: Hệ thống này sau khi triển khai thì ai sẽ vận hành?**

> Đây là điểm mạnh của hệ thống: sau khi triển khai, việc vận hành hàng ngày gần như tự động — hệ thống tự phân tích Log và đưa ra cảnh báo. Quản trị viên chỉ cần xem báo cáo và xử lý các cảnh báo được đánh dấu. Không cần chuyên gia AI để vận hành, chỉ cần định kỳ cập nhật lại mô hình khi xuất hiện các kiểu tấn công mới.

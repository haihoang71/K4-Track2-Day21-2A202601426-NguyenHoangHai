# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

<!--
HƯỚNG DẪN - đọc rồi XÓA TOÀN BỘ các khối chú thích này sau khi điền xong:

  - Giới hạn: KHÔNG QUÁ 1 TRANG A4, tương đương khoảng 450 - 550 từ nội dung.
  - Chỉ điền vào các chỗ ___ và các ô trong bảng. Không thêm mục mới.
  - Viết bằng câu hoàn chỉnh, không gạch đầu dòng cụt lủn.
  - Kiểm tra độ dài sau khi đã xóa hết chú thích:
        wc -w nop-bai/bao-cao.md
    và xem trước bản in bằng cách mở file trên GitHub rồi Ctrl+P / Cmd+P.
-->

| | |
|---|---|
| Họ và tên | Nguyễn Hoàng Hải |
| MSSV | 2A202601426 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/haihoang71/K4-Track2-Day21-2A202601426-NguyenHoangHai |
| Ngày nộp | 21/08/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do


| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 200 | 0.1 | 5 | 0.7149 | 0.874 |
| 2 | 100 | 0.1 | 3 | 0.7109 | 0.878 |
| 3 | 50 | 0.5 | 2 | 0.7048 | 0.876 |
| 4 | 200 | 0.2 | 10 | 0.7009 | 0.860 |
| 5 | 50 | 0.5 | 10 | 0.6463 | 0.838 |

**Bộ siêu tham số đã chọn:** `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`.

**Lý do:** 
* **So sánh theo F1-score:** Bộ siêu tham số này đạt chỉ số `f1_score` cao nhất (0.7149) trong tất cả các lần chạy. Điểm F1 cao vượt trội cho thấy mô hình đạt được sự cân bằng tối ưu giữa Precision (độ chính xác) và Recall (độ phủ), đặc biệt hiệu quả nếu tập dữ liệu có sự mất cân bằng giữa các lớp (class imbalance) — điều mà chỉ số `accuracy` đơn thuần không phản ánh hết được.
* **Mối quan hệ giữa Accuracy và F1-score:** Lần chạy có `accuracy` cao nhất là lần 2 (`accuracy` = 0.878), **không trùng** với lần chạy có `f1_score` cao nhất là lần 1 (`accuracy` = 0.874). Điều này chỉ ra rằng dữ liệu có hiện tượng lệch lớp (imbalanced data). Lần chạy 2 đạt `accuracy` cao hơn có thể do mô hình dự đoán tốt ở lớp đa số, nhưng xét về khả năng nhận diện lớp thiểu số/lớp mục tiêu thì lần chạy 1 mới là mô hình toàn diện và hữu ích hơn.
* **Sự đánh đổi (trade-off) giữa `n_estimators` và `learning_rate`:** Qua quan sát các lần chạy, khi sử dụng `learning_rate` nhỏ (0.1) kết hợp với `n_estimators` đủ lớn (100–200), mô hình học từng bước cẩn thận và đạt hiệu năng tối ưu nhất. Ngược lại, khi tăng `learning_rate` lên cao (0.5) nhưng giảm `n_estimators` xuống (50) ở lần 3 và 5, mô hình tiến tới nghiệm quá nhanh dẫn đến giảm cả `f1_score` lẫn `accuracy`, đặc biệt tồi tệ khi kết hợp với `max_depth` lớn (lần 5 gây overfit nghiêm trọng).

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Tập dữ liệu dự đoán thu nhập bị lệch lớp nghiêm trọng (imbalanced dataset), khi nhóm có thu nhập cao (>50K) chỉ chiếm khoảng 24%, còn nhóm thu nhập thấp (<=50K) chiếm tới 76%. Nếu xây dựng một mô hình ngây thơ (naive model) luôn luôn dự đoán mọi mẫu là "thu nhập thấp", mô hình này vẫn đạt độ chính xác (Accuracy) lên tới 76%. Con số này gây hiểu nhầm lớn vì mô hình hoàn toàn thất bại trong việc phát hiện nhóm thu nhập cao.

Chỉ số F1-Score của lớp dương (lớp >50K) khắc phục điều này bằng cách dung hòa giữa Precision (độ chính xác khi dự đoán lớp >50K) và Recall (khả năng không bỏ sót người có thu nhập cao). Chúng ta không dùng average="macro" hay average="weighted" vì các cách tính này sẽ kéo chỉ số F1 lên cao nhờ trọng số của lớp đa số (<=50K), làm che khuất hiệu năng thực tế trên lớp mục tiêu.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| Pipeline báo lỗi kết nối S3 ở bước DVC Pull | Runner thiếu AWS Credentials do secret chưa được truyền hoặc parse chưa đúng dạng JSON | Tách secret thành 2 biến `AWS_ACCESS_KEY_ID` và `AWS_SECRET_ACCESS_KEY` riêng biệt trong Repository Secrets |
| Mất kết nối (timeout/refused) khi `curl` API từ máy local | AWS Security Group của EC2 mặc định chặn các port không phải SSH (port 22) | Thêm Inbound Rule cho Custom TCP trên port `8000` với source `0.0.0.0/0` |
| Lỗi `ModuleNotFoundError: No module named 'boto3'` ở bước upload model | Môi trường runner GitHub Actions chưa được cài đặt thư viện `boto3` | Bổ sung `boto3` vào câu lệnh `pip install` ở bước `Install dependencies` trong file YAML |
---

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | **0.714** | **0.874** |
| Bước 3 (thêm `train_batch2`) | **0.735** | **0.882** |

**Nhận xét:** Khi bổ sung thêm `train_batch2` (tăng gấp đôi dữ liệu lên 44.722 mẫu), F1-score tăng nhẹ từ 0.714 lên 0.735 và Accuracy tăng từ 0.874 lên 0.882. Sự cải thiện nhỏ này cho thấy hai tập dữ liệu được chia ngẫu nhiên từ cùng một phân phối gốc nên không mang thêm nhiều thông tin đột biến, tuy nhiên lượng dữ liệu lớn hơn vẫn giúp mô hình tối ưu hóa ranh giới phân loại tốt hơn một chút. Quan trọng nhất, Bước 3 đã chứng minh quy trình MLOps CI/CD hoạt động hoàn toàn tự động và tin cậy: từ lúc commit dữ liệu mới đến khi mô hình được huấn luyện và deploy lên EC2 mà không cần thao tác thủ công.

---

## 5. Phần Bonus Đã Thực Hiện (nếu có)


- [ ] Bonus 1 - Tracking MLflow từ xa với DagsHub: ___
- [ ] Bonus 2 - Điều chỉnh ngưỡng quyết định: ___
- [ ] Bonus 3 - Báo cáo precision / recall tự động: ___
- [ ] Bonus 4 - Hoàn trả về phiên bản trước: ___
- [ ] Bonus 5 - Cảnh báo lệch lạc dữ liệu: ___

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

<!-- Khoảng 120 - 150 từ. -->

___

<!--
Cần nêu được:
  - Phân bố lớp của tập dữ liệu (tỷ lệ lớp thu nhập > 50K) và hệ quả của nó.
  - Accuracy của một mô hình luôn trả lời "thu nhập thấp" là bao nhiêu, vì sao con số
    đó gây hiểu nhầm.
  - F1 của lớp dương đo điều gì mà accuracy không đo được.
  - Vì sao KHÔNG dùng average="weighted" hay average="macro" khi gọi f1_score.
-->

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

<!-- Nêu 2 - 3 khó khăn thật, mỗi ô một câu ngắn. -->

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| ___ | ___ | ___ |
| ___ | ___ | ___ |
| ___ | ___ | ___ |

---

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)

<!-- Lấy số liệu từ bảng ở mục 3.6 của tasks/buoc-3.md. -->

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | ___ | ___ |
| Bước 3 (thêm `train_batch2`) | ___ | ___ |

**Nhận xét:** ___

<!--
Một câu trả lời trung thực kiểu "f1 giảm 0,01 vì dữ liệu mới cùng phân phối, không mang
thêm thông tin mới" được đánh giá cao hơn kết luận sai rằng thêm dữ liệu luôn tốt hơn.
-->

---

## 5. Phần Bonus Đã Thực Hiện (nếu có)

<!-- Xóa cả mục 5 nếu không làm bonus. Mỗi bonus tối đa 1 dòng. -->

- [ ] Bonus 1 - Tracking MLflow từ xa với DagsHub: ___
- [ ] Bonus 2 - Điều chỉnh ngưỡng quyết định: ___
- [ ] Bonus 3 - Báo cáo precision / recall tự động: ___
- [ ] Bonus 4 - Hoàn trả về phiên bản trước: ___
- [ ] Bonus 5 - Cảnh báo lệch lạc dữ liệu: ___

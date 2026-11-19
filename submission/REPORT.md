# Báo cáo nhóm 98

## 1. Số liệu luyện tập
- Phụ trách P1: NGUYỄN KHOA MINH và VŨ THỊ NHUNG. Tổng hợp báo cáo: NGUYỄN ANH THƯ.
- Kết quả cuối ngày 2026-11-19: seed 98007 có 17 lỗi đã chốt; F1 rule ≈ 1,0, cross_check ≈ 0,7, overall ≈ 0,8.
- Seed kiểm tra độc lập 98008 có 11 lỗi luật, F1 rule ≈ 1,0, cross_check chưa triển khai, overall ≈ 0,8.
- Các F1 là số làm tròn một chữ số từ score_findings.py chế độ học viên; chưa kết luận kết quả đề ẩn.
- Lô sạch seed 5 gồm 50 ảnh: 0 lỗi luật; P2 sau hiệu chỉnh có 0 ứng viên.
- P2: CAO THỊ THÚY HIỀN phụ trách đối chiếu; NGUYỄN XUÂN ANH phụ trách công cụ xem ảnh. Bản đầu của seed 98007 có 19 ứng viên trên 18 ảnh (12 instance_merge, 4 bất đồng lớp, 2 missing_box, 1 bbox_drift). Sau sửa thuật toán và review, hồ sơ cuối có 18 dòng review: 7 confirmed và 11 rejected; ca `000000014831` được giữ riêng ở trạng thái chưa chắc chắn, không đưa vào `errors.json`.
- Hiệu chỉnh trên lô sạch: bản đầu sinh 52 ứng viên instance_merge do box lân cận chạm mask đã được box khác phủ hết. Bổ sung mỗi box phủ 20–80%, hợp phủ ≥ 75%, pixel chung ≤ 10%; còn 0 ứng viên. Ngưỡng và giới hạn tại [validator/README.md](../validator/README.md).
- Ngưỡng P1: biên box dung sai 1e-6 cho làm tròn YOLO; duplicate_box cùng lớp, lệch kích thước tối đa 0,01 pixel, lệch tâm tối đa 2,01 pixel mỗi trục. Căn cứ mô tả box lặp 1–2 pixel và cùng kích thước trong GUIDE; không dùng đáp án riêng hoặc dò điểm từng ảnh.
- Cập nhật ngày 2026-11-19: người dùng xác nhận CAO THỊ THÚY HIỀN và NGUYỄN XUÂN ANH đã trực tiếp xem ảnh, kiểm tra và xác nhận kết quả P2 theo phân công. Ca uncertain vẫn chưa chốt. Bản v2 đã được tạo ở trạng thái Hold, chưa được phê duyệt để train. Mỗi thành viên vẫn cần giải thích được phần việc khi vấn đáp.

## 2. Vì sao báo hết ứng viên làm F1 giảm?
Bản đầu tạo 52 ứng viên trên lô sạch dù không có lỗi gài. Báo hết sẽ tạo false positive, giảm precision và có thể giảm F1. Sau hiệu chỉnh còn 0 ứng viên lô sạch nhưng không chứng minh không bỏ sót. Sau review, kết quả tự đo cross-check làm tròn ≈ 0,7 và overall ≈ 0,8; đây chỉ là số tự đo trên seed luyện tập.

## 3. Quyết định và lineage
Phụ trách: HỒ XUÂN HÙNG. Ngày 2026-11-19, ghi quyết định **HOLD** cho v1 `lab250_05fa3dd27dd4`.

- Quyết định HOLD ban đầu được ghi khi có 10 lỗi luật / 250 ảnh = **4%**, đã vượt ngưỡng 2%. Áp dụng quy ước đề: mỗi scene_leak tính một ảnh lỗi.
- Sau review, `errors.json` có 17 lỗi đã chốt / 250 ảnh = **6,8%** gồm 10 lỗi luật và 7 lỗi gán nhãn. Ca chưa chắc chắn không được cộng vào tỷ lệ.
- Training run `R-021` đã sử dụng v1, nên cần review_or_retrain. Thay dataset không thay đổi trọng số mô hình đã học; team AI phải đánh giá run và quyết định kiểm tra/train lại.
- Lineage giữ quyết định HOLD ban đầu và đã ghi sự kiện release v2 với parent là v1; v2 vẫn ở trạng thái Hold.

## 4. Hash chứng minh gì, không chứng minh gì?
SHA-256 giúp kiểm tra bytes của file có khớp bản kê hay không và hỗ trợ truy vết thay đổi. Hash khớp không chứng minh nhãn đúng, ảnh phù hợp guideline hoặc dataset không rò split. Sai hash cần kiểm tra file thực tế trước khi quyết định chỉ sửa manifest hay đưa ảnh vào rework.

## 5. Truy vết
Phụ trách và trực tiếp hoàn thành theo xác nhận người dùng: **NGUYỄN ANH THƯ**.

- Lớp đổi quy tắc là `cup` (class id 41). Chỉ xét ảnh thuộc job dùng guideline cũ v1.2 và thực sự có ít nhất một box detection lớp cup.
- `tier_a` gồm 4 ảnh trong hai cảnh team AI báo (`scene_237`, `scene_878`): `000000002592`, `000000002685`, `000000003845`, `000000003934`.
- `tier_b` gồm 3 ảnh khác cùng điều kiện nhưng chưa được báo: `000000002157`, `000000002431`, `000000003661`.
- Hai job liên quan yêu cầu thông báo người gán `A02` và người kiểm `Q02`.
- Dùng guideline của job trong `jobs.csv`, không dùng guideline từng ảnh, vì trường metadata ảnh có thể chính là lỗi guideline_mismatch.
- Kết quả tự đo: tier_a ≈ 1,0, tier_b ≈ 1,0, notify ≈ 1,0.

## 6. Bàn giao v2 và bảo mật

- **NGUYỄN XUÂN ANH** trực tiếp hoàn thành bản v2 theo xác nhận người dùng; **HỒ XUÂN HÙNG** hoàn thành QC và lineage.
- V2 có 242 ảnh và 1.708 nhãn; 8 ảnh lỗi detection chuyển sang rework đúng người. Ảnh chỉ lỗi panoptic vẫn ở lại sản phẩm detection và được ghi chú cho team panoptic.
- Manifest có 484 file ảnh/nhãn với SHA-256; label summary, truy vết, README, rework queue và gói tái lập đã được kiểm tra.
- Ảnh sai hash `000000002532` mở được và đúng nội dung; v2 tính lại hash từ bytes, không sửa v1.
- V2 giữ trạng thái Hold vì ca `000000014831` vẫn chưa đủ căn cứ để chốt và ca khuôn mặt yêu cầu Hold + báo người phụ trách.
- **NGUYỄN ANH THƯ** trực tiếp hoàn thành `security.md` theo xác nhận người dùng.
- `check_handover.py`: **17 PASS, 0 FAIL**. PASS xác nhận định dạng và tính nhất quán, không chứng minh mọi nhãn đều đúng.

## 7. Bug hoặc điểm chưa rõ trong lab (nếu có)
Chưa xác nhận bug trong script đề. Hai lỗi trong công cụ nhóm đã sửa sau đối chiếu ảnh:

- Gợi ý instance_merge do chọn hai box lân cận dù có box đúng khớp segment. Đã bổ sung điều kiện loại trừ box khớp tốt.
- Gợi ý missing_box giả do bỏ dòng có class 80 nhưng box vẫn tồn tại. Đã giữ hình học và để P1 báo invalid_class.

Sau sửa: seed 98007 còn 8 ứng viên trên 8 ảnh; lô sạch vẫn 0 ứng viên, kết quả 10 lỗi luật P1 không đổi. 8 kiểm thử P2 đạt. Số 19 ứng viên ở phần trên là kết quả trước sửa, được lưu để truy vết.

Phân tích đủ 19 ca ban đầu và một ca bổ sung: 7 ca có bằng chứng lỗi, 12 gợi ý ban đầu bị loại, 1 ca chưa chắc chắn. Xem [P2_REVIEW.md](P2_REVIEW.md) để biết nguồn phân tích và bằng chứng từng ca. Người dùng đã xác nhận Hiền/Xuân Anh trực tiếp hoàn thành phần kiểm tra P2; 7 dòng confirmed đã được gộp vào `errors.json` và kết quả tự đo P2 làm tròn ≈ 0,7. Ca chưa chắc chắn không được chuyển thành confirmed.

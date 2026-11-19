# Validator của nhóm

Phụ trách: **NGUYỄN KHOA MINH** (file, detection, CLI) và **VŨ THỊ NHUNG** (metadata, panoptic, kiểm thử).

Đã triển khai P1 trong [validate.py](validate.py): chín lỗi luật. Chạy từ gốc repo:

```
py -X utf8 validator/validate.py runs/r98007/delivery --out runs/r98007/rules.json
py -X utf8 -m unittest discover -s tests -p test_validator_rules.py -v
```

Chỉ đọc thư mục delivery được truyền vào; chỉ thư viện chuẩn; không mạng. Xem [GUIDE.md](../GUIDE.md) Pha 1–2 và [RULES.md](../RULES.md).

## Phạm vi và lựa chọn kiểm tra

- Tính SHA-256 của ảnh, nhãn và mask theo manifest. Thiếu ảnh báo missing_image, không đồng thời báo wrong_hash do thiếu file.
- Kiểm class theo classes.txt; box phải hữu hạn, kích thước dương và nằm trong ảnh. Dung sai 1e-6 theo tọa độ chuẩn hóa chỉ nhằm tránh nhiễu làm tròn.
- Box lặp: cùng lớp, chênh kích thước tối đa 0,01 pixel và chênh tâm tối đa 2,01 pixel mỗi trục; dựa vào mô tả trong GUIDE, không dò điểm để chọn ngưỡng.
- Guideline theo jobs.csv; scene xuất hiện nhiều split báo target là scene_id.
- Category theo panoptic.json; segment thing có area lớn hơn số pixel thực trong mask báo thing_overlap; bỏ id nền 0.
- Đường dẫn dữ liệu phải nằm trong delivery; đầu ra phải nằm ngoài delivery để bảo vệ v1. Thiếu nhãn/mask hoặc schema không đọc được sẽ dừng với thông báo thay vì báo PASS giả.
- `--candidates` sinh bất đồng để review P2; không tự gộp vào lỗi luật.

## Kết quả P1 ngày 2026-11-19

- Seed 98007: 10 lỗi luật, F1 lỗi luật ≈ 1,0; F1 tổng ≈ 0,6.
- Seed 98008: 11 lỗi luật, F1 lỗi luật ≈ 1,0; F1 tổng ≈ 0,8.
- Lô sạch seed 5: 50 ảnh, 0 lỗi luật, 0 ứng viên P2 sau hiệu chỉnh.
- F1 do score_findings.py chế độ học viên làm tròn một chữ số; không coi đây là độ chính xác tuyệt đối.
- `errors.json` cuối gồm lỗi luật và lỗi gán nhãn đã confirmed; `rules.json` được giữ riêng trong thư mục chạy để có thể tái lập bước merge review.
- Minh/Nhung đã được ghi nhận phụ trách P1; mỗi người cần giải thích được các hàm thuộc phần mình khi vấn đáp.

## P2 — Hiền phụ trách đối chiếu, Xuân Anh phụ trách công cụ review

```powershell
py -X utf8 validator/validate.py runs/r98007/delivery --out runs/r98007/rules.json --candidates runs/r98007/candidates.json
py -X utf8 validator/build_review.py runs/r98007/delivery --candidates runs/r98007/candidates.json --out runs/r98007/review.html
py -X utf8 -m unittest discover -s tests -p test_cross_check.py -v
```

Mở review.html bằng trình duyệt. Trang nhúng ảnh và mask, chạy offline, không cần Pillow hoặc máy chủ. Lọc tên người được giao. Hàng đợi ban đầu 19 ca/18 ảnh đã được lưu riêng; sau sửa lỗi báo thừa còn 8 ca/8 ảnh, được phân công lại theo ảnh. Segment hồng, box liên quan xanh, các box còn lại vàng. Có thể tắt overlay và phóng to.

1. Chọn tên người thực sự xem. Với class_disagreement, nhìn ảnh để chọn class_swap hoặc category_swap theo nguồn sai.
2. Chọn confirmed/rejected, ghi bằng chứng cụ thể ít nhất 20 ký tự, lưu trước khi chuyển ca.
3. Xuất CSV thường xuyên. Các máy không tự đồng bộ; gửi CSV cho Hùng gộp đúng schema image,type,verdict,note, giữ một header và xử lý mâu thuẫn cùng ảnh/loại.
4. Đặt kết quả chung tại `runs/r98007/review_log.csv`, sau đó chạy merge_review và đo F1:

```powershell
py -X utf8 scripts/merge_review.py --rules runs/r98007/rules.json --review runs/r98007/review_log.csv --out runs/r98007/errors.json
py -X utf8 scripts/score_findings.py --run runs/r98007
```

Ngưỡng trong [cross_check.py](cross_check.py): ghép theo tên lớp; bỏ crowd và segment nhỏ hơn max(200 pixel, 0,1% ảnh). Bất đồng lớp cần IoU ≥ 0,65 và phủ mask ≥ 0,85; drift cần IoU ≥ 0,3 nhưng phủ < 0,8; thiếu box khi mọi IoU < 0,1 và phủ < 0,2. Gộp instance cần hai box cùng lớp mỗi box phủ 20–80%, hợp phủ ≥ 75%, pixel chung ≤ 10% và IoU hai box < 0,25.

Lần đầu lô sạch có 52 ứng viên gộp giả do box lân cận chạm segment đã được một box phủ hết. Sau bổ sung giới hạn độ phủ và pixel chung còn 0 ứng viên. Không dùng điểm để dò từng ảnh. Hàng đợi ban đầu của lô chính có 12 instance_merge, 4 class_disagreement, 2 missing_box, 1 bbox_drift; đây là số trước sửa và review. Ngưỡng có thể bỏ sót vật nhỏ hoặc box lệch lớn; 0 ứng viên lô sạch không đảm bảo recall.

### Cập nhật sau xem ảnh hỗ trợ

Hồ sơ phân tích và kết quả review nằm trong [P2_REVIEW.md](../submission/P2_REVIEW.md). Hai sửa lỗi có kiểm thử hồi quy: không gợi ý merge nếu có box cùng lớp khớp IoU ≥ 0,85, phủ ≥ 0,9; giữ hình học box invalid_class để không báo thiếu box giả.

Hàng đợi mới: 2 instance_merge, 4 class_disagreement, 1 bbox_drift và 1 missing_box. Lô sạch vẫn 0 ứng viên. Riêng ca zebra được gợi ý bbox_drift cần kiểm lại đề xuất missing_box trong hồ sơ hỗ trợ. Chưa tự đổi loại theo từng tên ảnh trong validator.

Để hiển thị bằng chứng hỗ trợ trong trang review mà không tự điền kết luận:

```powershell
py -X utf8 validator/build_review.py runs/r98007/delivery --candidates runs/r98007/candidates.json --out runs/r98007/review.html --advisory runs/r98007/p2_advisory.json
```

Kết luận/ghi chú chỉ được lưu sau khi người thực sự xem chủ động nhập. Tài liệu hỗ trợ và ảnh không được chuyển thành lịch sử review mang tên thành viên nếu họ chưa xác nhận.

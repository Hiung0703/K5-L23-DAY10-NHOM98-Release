Release: lab250_05fa3dd27dd4_v2
Parent: lab250_05fa3dd27dd4
Số ảnh: 242
Số nhãn: 1708
Guideline: J01: v1.2; J02: v1.2; J03: v1.2; J04: v1.3; J05: v1.3; J06: v1.3; J07: v1.3; J08: v1.3; J09: v1.3; J10: v1.3
QC v1: 17/250 = 6.80%
Kết luận v1: Hold — theo ngưỡng 2%
Kết luận v2: Hold — bản bàn giao đã chuẩn bị; chờ hoàn tất kiểm tra và xử lý ca chưa chắc chắn trước khi dùng train
Ghi chú: Xuân Anh thực hiện bàn giao; Hùng phụ trách QC/lineage, theo xác nhận người dùng. Nhãn và ảnh giữ nguyên bytes; loại ảnh lỗi detection vào rework_queue đúng job. Guideline lấy jobs.csv; split lấy đa số toàn cảnh v1 (hòa chọn thứ tự tên split). Hash tính lại từ bytes; ảnh wrong_hash đã mở kiểm: 000000002532.
Lỗi panoptic giữ ảnh trong v2 detection, báo team panoptic: [{"type": "category_swap", "target": "000000023126"}, {"type": "instance_merge", "target": "000000017115"}, {"type": "instance_merge", "target": "000000022935"}, {"type": "invalid_category_id", "target": "000000002587"}, {"type": "invalid_category_id", "target": "000000006818"}, {"type": "thing_overlap", "target": "000000006763"}]
Ca chưa chắc chắn giữ nguyên và yêu cầu kiểm lại trước train: 000000014831
Bản đóng gói không phải phê duyệt train. PASS kiểm định dạng không chứng minh nhãn đúng.

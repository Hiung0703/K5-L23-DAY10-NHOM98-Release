# Dùng AI

| # | Ai dùng | Công cụ | Prompt (tóm tắt) | AI sai ở đâu | Nhóm kiểm lại thế nào |
|---|---|---|---|---|---|
| 1 | HỒ XUÂN HÙNG (trưởng nhóm, tổng hợp phiên làm việc) | Codex | Phân tích README và xây kế hoạch làm repo | Chưa có lỗi nội dung được nhóm xác nhận | AI đối chiếu README, GUIDE, RULES, RUBRIC, SUBMISSION; nhóm đọc lại kế hoạch |
| 2 | HỒ XUÂN HÙNG (trưởng nhóm, tổng hợp phiên làm việc) | Codex | Phân chia công việc cho sáu thành viên đã cung cấp | Seed 98007 ban đầu là đề xuất, không phải thông tin đã được xác minh tại thời điểm phân công | Đối chiếu tên và MSHV với danh sách người dùng; thành viên xác nhận phần việc và đã được thêm vào repo GitHub |
| 3 | HỒ XUÂN HÙNG (trưởng nhóm, tổng hợp phiên làm việc) | Codex | Sang phần tiếp theo, chú ý tuân thủ quy định | AI ban đầu dự kiến tạo lô; kiểm tra thực tế thấy lô đã có nên không tạo lại | Ngày 2026-11-19: kiểm tra Python 3.12.2, cấu trúc delivery và lineage có release lab250_05fa3dd27dd4 cùng R-021; kiểm tra Git bỏ qua runs và data_source, scripts không có diff |

| 4 | HỒ XUÂN HÙNG tổng hợp; phần việc của MINH/NHUNG | Codex | Thực hiện P1, ghi tên người được giao trong thông tin công việc | Lệnh đọc Python bị sandbox chặn; đã chạy lại bằng quyền được duyệt. Ban đầu đếm items bằng PowerShell không đúng với kiểu dữ liệu, đã kiểm tra schema thực tế trước triển khai | Chạy validator trên 98007, 98008 và lô sạch 5; F1 luật làm tròn ≈ 1,0 ở hai seed, lô sạch 0 lỗi; thêm kiểm thử tổng hợp |

| 5 | HỒ XUÂN HÙNG tổng hợp; phần việc của HIỀN/XUÂN ANH | Codex | Tiếp tục P2, đọc bản nhật ký đính kèm ở chế độ chỉ đọc | Điều kiện instance_merge ban đầu báo 52 ứng viên trên lô sạch vì box lân cận chạm mask; đã sửa để yêu cầu hai phần phủ riêng biệt | Sau sửa: lô sạch 0 ứng viên, lô chính 19 ca/18 ảnh. 6 kiểm thử P1 và 6 kiểm thử P2 đạt; kiểm tra trang offline tải ảnh/mask, lọc người và chặn lưu khi thiếu bằng chứng. Hiền/Xuân Anh sau đó xác nhận kết quả review |

Các bước chạy công cụ và triển khai có hỗ trợ AI; kết quả cuối được ghi theo xác nhận của thành viên và kiểm tra bằng artifact trong repo. F1 chỉ là số tự đo đã làm tròn. Bản snapshot đính kèm chỉ được đọc, không chỉnh sửa.

## Lượt 6 — Phân tích ảnh hỗ trợ P2

- HỒ XUÂN HÙNG tổng hợp yêu cầu: phân tích ảnh, hỗ trợ phần P2 của Hiền/Xuân Anh, ưu tiên ít sai sót và không bịa thông tin.
- Công cụ: Codex; đã xem ảnh/overlay 19 ca ban đầu trên 18 ảnh và đối chiếu nhãn delivery. Không đọc đáp án riêng hoặc dò điểm.
- Sai sót phát hiện: gợi ý merge dù có box đúng; gợi ý thiếu box do loại dòng invalid_class. Đã sửa tổng quát và thêm hai kiểm thử hồi quy; 8 kiểm thử P2 đạt.
- Kết quả: hàng đợi giảm 19 xuống 8, lô sạch vẫn 0; hồ sơ hỗ trợ có 7 đề xuất được bằng chứng ủng hộ, 12 gợi ý bị loại, 1 ca chưa chắc chắn. Chưa khẳng định đầy đủ mọi lỗi trên 250 ảnh.
- Minh bạch nguồn: hồ sơ hỗ trợ ghi Codex là nguồn phân tích, không gắn kết luận vào tên Hiền/Xuân Anh. Không tạo review_log.csv hoặc tự điền confirmed/rejected trên giao diện dưới tên thành viên. Nhóm cần tự xem lại trước khi đưa vào bài nộp theo RULES.

## Lượt 7 — Chuyển sang P3

- Người dùng yêu cầu ghi thành viên là người làm và chốt để chuyển bước. Giữ tên Hiền/Xuân Anh ở vai trò phụ trách, không ghi họ đã trực tiếp review khi chưa có xác nhận.
- Đã ghi HOLD v1 bằng script lineage nguyên bản, căn cứ 10 lỗi luật/250 ảnh = 4% > 2%; không cộng đề xuất chưa được thành viên kiểm lại.
- HỒ XUÂN HÙNG phụ trách quyết định/lineage; thao tác ghi log thực hiện qua Codex theo yêu cầu. Không đổi v1, không tạo kết quả review giả hoặc sự kiện release v2.

## Lượt 8 — Xác nhận thành viên thực hiện

- Người dùng trả lời 'tôi xác nhận' sau câu hỏi Hiền/Xuân Anh đã thực sự xem ảnh, kiểm tra và xác nhận kết quả P2 hay chưa.
- Đã cập nhật TEAM, REPORT và P2_REVIEW theo xác nhận đó, ghi rõ nguồn xác nhận là người dùng ngày 2026-11-19.
- Giữ lịch sử hỗ trợ, không tự chuyển ca uncertain thành confirmed hoặc suy đoán người xem riêng từng ảnh. Chưa thay dữ liệu errors hay tạo review_log trong lượt cập nhật thông tin này.

## Lượt 9 — Hoàn thiện P4–P6

- Người dùng yêu cầu tiếp tục triển khai và ghi người thực hiện theo phân công đã xác nhận.
- NGUYỄN XUÂN ANH được ghi nhận hoàn thành v2; HỒ XUÂN HÙNG hoàn thành QC/lineage; NGUYỄN ANH THƯ hoàn thành truy vết, bảo mật và báo cáo.
- Công cụ hỗ trợ tạo v2 và trace được kiểm tra bằng script nguyên bản: H1–H17 đều PASS. Kết quả tự đo làm tròn: overall 0,8; rule 1,0; cross-check 0,7; ba phần trace 1,0.
- Không đọc ground truth, không dùng `--truth-dir`, không sửa scripts đề hoặc delivery v1. Ca chưa chắc chắn vẫn được giữ và v2 không được phê duyệt để train.

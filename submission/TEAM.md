# Nhóm 98

- Trưởng nhóm: HỒ XUÂN HÙNG.
- Seed luyện tập: `98007` (nhóm 98 × 1000 + 7). Đã có lô tại `runs/r98007/delivery`; kiểm tra ngày 2026-11-19.
- Release v1: `lab250_05fa3dd27dd4`; lineage đã có sự kiện inject và training run `R-021`. Không chạy lại bước tạo lô chính.
- Trạng thái P3: đã ghi HOLD v1 ngày 2026-11-19 trên cơ sở 10 lỗi luật/250 ảnh = 4%; HỒ XUÂN HÙNG phụ trách.
- Xác nhận P2 ngày 2026-11-19: theo xác nhận của người dùng trong phiên làm việc, **CAO THỊ THÚY HIỀN và NGUYỄN XUÂN ANH đã trực tiếp xem ảnh, kiểm tra và xác nhận kết quả phần việc P2**. Hiền hoàn thành phần đối chiếu; Xuân Anh hoàn thành phần công cụ review và kiểm tra ảnh theo phân công. Ca còn chưa chắc chắn được giữ nguyên; xác nhận này không tự biến ca đó thành lỗi đã xác nhận.
- Xác nhận P4–P6 ngày 2026-11-19: **NGUYỄN XUÂN ANH trực tiếp hoàn thành bàn giao v2**, **HỒ XUÂN HÙNG trực tiếp hoàn thành QC/lineage**, và **NGUYỄN ANH THƯ trực tiếp hoàn thành truy vết, bảo mật và tổng hợp báo cáo**, theo xác nhận của người dùng. Bộ kiểm cuối đạt 17 PASS, 0 FAIL.
- Repo: https://github.com/Hiung0703/K5-L23-Day10-Nhom98-Dataset-Release-Handover
- Email/tài khoản liên hệ đã được người dùng cung cấp ngày 2026-11-19. Ngày 2026-11-19, trưởng nhóm xác nhận cả sáu thành viên đã được thêm vào repository GitHub. Tên đăng nhập GitHub không được suy đoán từ địa chỉ email.

## Thành viên và phần việc chính

| Họ và tên | MSHV | Email/tài khoản liên hệ | Tài khoản GitHub | Phần chính |
|---|---|---|---|---|
| NGUYỄN KHOA MINH | 2A202603160 | ngyenkhoaminh0104@gmail.com | Đã xác nhận tham gia repo | Validator lỗi file và detection; giao diện chạy validator |
| VŨ THỊ NHUNG | 2A202603156 | vuthinhung061005@gmail.com | Đã xác nhận tham gia repo | Validator metadata và panoptic; kiểm thử lô sạch |
| CAO THỊ THÚY HIỀN | 2A202603193 | hiwn1222@gmail.com | Đã xác nhận tham gia repo | Đối chiếu detection–panoptic; sinh ứng viên |
| HỒ XUÂN HÙNG (LEAD) | 2A202603062 | hohung16124@gmail.com | Đã xác nhận tham gia repo | Điều phối, tích hợp, quyết định QC, lineage và nộp bài |
| NGUYỄN XUÂN ANH | 2A202603117 | anhnguyenkaz@gmail.com | Đã xác nhận tham gia repo | Công cụ xem ảnh; tạo và kiểm tra bản bàn giao v2 |
| NGUYỄN ANH THƯ | 2A202603084 | 26ai.thuna@vinuni.edu.vn | Đã xác nhận tham gia repo | Truy vết ticket, bảo mật, tổng hợp báo cáo và nhật ký AI |

## Công việc và điều kiện hoàn thành

### 1. NGUYỄN KHOA MINH — validator file và detection

- Phụ trách `missing_image`, `wrong_hash`, `invalid_class`, `bbox_out_of_bounds`, `duplicate_box`.
- Tạo giao diện `validator/validate.py <delivery> --out <errors.json> [--candidates <candidates.json>]`; tích hợp các hàm của Nhung và Hiền.
- Tính SHA-256 từ bytes; kiểm box theo biên thực; nhận diện box lặp bằng lớp, kích thước và độ lệch tâm, tránh chỉ dùng IoU.
- Hoàn thành khi giao diện chạy được, trả đúng cấu trúc lỗi; cùng Nhung kiểm tra ít nhất hai seed và lô sạch.

### 2. VŨ THỊ NHUNG — validator metadata và panoptic

- Phụ trách `scene_leak`, `guideline_mismatch`, `invalid_category_id`, `thing_overlap`.
- Lấy guideline chuẩn từ job; target của `scene_leak` là scene_id; đếm pixel mask và so với area của segment.
- Dùng thư viện chuẩn, được dùng hàm đọc PNG của [pngutil.py](../scripts/pngutil.py).
- Phụ trách ghi số liệu kiểm thử lỗi luật trên hai seed và lô sạch; phối hợp Minh xử lý báo thừa.
- Hoàn thành khi đủ bốn loại kiểm tra, lỗi luật trên lô sạch bằng 0 và F1 lỗi luật trên lô luyện tập gần 1,0 nếu kết quả đo thực tế đạt được.

### 3. CAO THỊ THÚY HIỀN — đối chiếu và sinh ứng viên

- Ghép lớp detection–panoptic theo tên; chuyển box YOLO sang pixel; kết hợp IoU và độ phủ pixel mask.
- Sinh ứng viên cho `class_swap`, `category_swap`, `bbox_drift`, `missing_box`, `instance_merge`; chưa tự coi ứng viên là lỗi đã xác nhận.
- Đo số ứng viên trên lô sạch, giải thích ngưỡng và nhiễu tự nhiên; phối hợp Xuân Anh thống nhất dữ liệu công cụ review cần hiển thị.
- Chia danh sách ứng viên thành sáu phần không trùng nhau để mọi thành viên review; chuyển ca khó cho người thứ hai xem.
- Hoàn thành khi có candidates, số liệu lô sạch và hàng đợi đủ rõ để nhóm review trước khi chốt errors.

### 4. HỒ XUÂN HÙNG — trưởng nhóm, tích hợp và lineage

- Chuẩn bị dữ liệu, tạo seed luyện tập chính một lần; thống nhất giao diện các phần code, theo dõi tiến độ và xử lý xung đột Git.
- Seed bổ sung tạo bằng [inject_release.py](../scripts/inject_release.py), tránh chạy lại run_lab để thêm training run R-021 vào lineage.
- Sau review, gộp lỗi luật với lỗi đã confirmed; tính QC v1 theo quy ước đề và quyết định theo ngưỡng trên 2% thì HOLD.
- Ghi decision, kiểm tra tác động tới R-021; ghi release v2 có parent sau khi Xuân Anh hoàn tất bàn giao.
- Kiểm tra toàn bộ bài, xuất submission, rà soát tiêu đề README/tên repo theo yêu cầu lớp, commit và push phần của mình; nộp link đúng hạn.
- Hoàn thành khi kết quả tích hợp nhất quán, lineage đầy đủ, bộ kiểm không FAIL và đủ hồ sơ nộp.

### 5. NGUYỄN XUÂN ANH — công cụ review và bàn giao v2

- Ưu tiên công cụ xem ảnh có box detection và segment panoptic trước mốc P2; Pillow chỉ dùng trong công cụ xem ảnh, không đưa vào validator.
- Chuẩn bị sẵn quy trình tạo v2 trong lúc chờ kết quả review; chỉ chốt nội dung sau khi có errors đã xác nhận.
- Tạo images, labels, manifest, label summary, truyvet, README và rework queue theo P4 của [GUIDE.md](../GUIDE.md).
- Loại ảnh thiếu file/lỗi detection vào rework đúng người; giữ ảnh chỉ lỗi panoptic trong v2 detection và ghi chú; sửa hash/guideline/split theo quy định, không sửa v1 hoặc sửa tay nhãn v2.
- Phối hợp Hùng đóng gói, kiểm hash và chạy bộ kiểm; đóng gói lại nếu nội dung v2 thay đổi.
- Hoàn thành khi công cụ review dùng được và các kiểm tra bàn giao v2 đều PASS.

### 6. NGUYỄN ANH THƯ — truy vết, bảo mật và hồ sơ

- Đọc ticket và changelog; xây dựng tier_a, tier_b, notify từ guideline của job và lớp detection bị thay đổi quy tắc.
- Hoàn thiện security theo ba mục của mẫu, nêu ví dụ ảnh thật trong lô; ca khuôn mặt kết luận HOLD và báo người phụ trách.
- Tổng hợp [REPORT.md](REPORT.md) từ số liệu do Minh, Nhung, Hiền, Hùng và Xuân Anh cung cấp; không điền số liệu dự đoán.
- Tổng hợp [prompts.md](prompts.md); mỗi thành viên phải cung cấp prompt mình dùng, chỗ AI sai và cách kiểm lại.
- Hoàn thành khi trace có đủ ba khóa và đúng tiêu chí, security đủ mục, báo cáo có số liệu thật và giải thích được các quyết định.

## Trách nhiệm chung và cách phối hợp

- Mọi người đều xem ảnh trong P2 và đề ẩn. Hiền chia đều số ứng viên, điều chỉnh theo độ khó; không giao toàn bộ review cho một người.
- Mỗi dòng review giữ schema `image,type,verdict,note`; ghi người review trong note cùng mô tả bằng chứng nhìn thấy, tối thiểu 20 ký tự. Ca chưa rõ phải xem lại, không tự confirmed.
- Hùng chỉ gộp lỗi gán nhãn khi đã có kết luận review của thành viên; AI không thay kết luận xem ảnh.
- Minh sở hữu file entry point của validator; Nhung và Hiền làm các module riêng và thống nhất đầu vào/đầu ra trước khi viết để tránh cùng sửa một file.
- Hùng hỗ trợ Xuân Anh phần bàn giao sau khi chốt QC; các thành viên tự bổ sung nội dung phần mình vào báo cáo để Thư không phải viết thay toàn bộ nhóm.
- Mỗi người có ít nhất hai commit có nội dung bằng tên/email của chính mình: một commit phần chính và một commit hoàn thiện, kiểm thử hoặc bằng chứng review. Không tạo commit rỗng để đủ số lượng.
- Không sửa script đề, không sửa lô v1, không đọc dữ liệu đáp án hoặc dò đáp án qua điểm; validator chỉ đọc delivery được truyền vào và không dùng mạng.
- Không commit dữ liệu nguồn, runs, file ZIP hoặc secret. Xuất bài theo [SUBMISSION.md](../SUBMISSION.md).

## Mốc phối hợp

- **0:15:** Hùng hoàn tất lô chính; cả nhóm thống nhất giao diện code và phần việc.
- **0:55:** Minh và Nhung có đủ chín kiểm tra luật; Hiền và Xuân Anh có phiên bản đầu của đối chiếu/công cụ review.
- **1:50:** Cả sáu người hoàn tất review luyện tập; Hiền tổng hợp kết quả và số ứng viên lô sạch.
- **2:05:** Hùng chốt QC, decision và impact; bàn giao errors cho Xuân Anh.
- **2:45:** Xuân Anh hoàn tất v2, Hùng hỗ trợ lineage và kiểm tra; Thư hoàn thiện trace.
- **3:15:** Trace, security và hồ sơ luyện tập đầy đủ; bộ kiểm không còn FAIL.
- **3:55:** Hoàn tất 40 phút đề ẩn, xuất bài và nộp theo hướng dẫn lớp.

Các mốc là mục tiêu theo [CHECKPOINTS.md](../CHECKPOINTS.md), không phải xác nhận công việc đã hoàn thành. Thời điểm bắt đầu đề ẩn và hạn nộp thực tế theo giảng viên.

# Quy trình triển khai cho 6 thành viên — Nhóm 98

Tài liệu này dùng để cả sáu thành viên trực tiếp kiểm tra P2, lưu bằng chứng bằng tên của mình và làm việc trên các nhánh riêng. Không điền kết quả thay người chưa xem ảnh.

## 1. Phân ca kiểm tra P2

| Thành viên | Nhánh | Ca phải trực tiếp xem |
|---|---|---|
| NGUYỄN KHOA MINH | `review/minh-p2` | `000000001818` — kiểm tra gợi ý `bbox_drift`, đồng thời xem có thiếu instance zebra hay không |
| VŨ THỊ NHUNG | `review/nhung-p2` | `000000012748` — bất đồng `cow`/`horse` |
| CAO THỊ THÚY HIỀN | `review/hien-p2` | `000000014831` — `missing_box` chưa chắc chắn; `000000017115` — `instance_merge` |
| HỒ XUÂN HÙNG | `review/hung-p2` | `000000020333` — bất đồng `fork`/`tie` |
| NGUYỄN XUÂN ANH | `review/xuan-anh-p2` | `000000022935` — `instance_merge`; `000000023126` — bất đồng `horse`/`sheep` |
| NGUYỄN ANH THƯ | `review/thu-p2` | `000000025560` — bất đồng `dog`/`cat` |

Mỗi người phải mở ảnh và overlay, tự chọn verdict và viết điều quan sát được. Không sao chép kết luận cũ nếu chưa tự kiểm tra.

## 2. Chuẩn bị trên máy từng thành viên

```powershell
git clone https://github.com/Hiung0703/K5-L23-Day10-Nhom98-Dataset-Release-Handover.git
cd K5-L23-Day10-Nhom98-Dataset-Release-Handover
git switch main
git pull origin main
```

Thiết lập đúng tên và email của chính mình:

```powershell
git config user.name "HỌ VÀ TÊN"
git config user.email "EMAIL ĐÃ GHI TRONG submission/TEAM.md"
```

Kiểm tra trước khi commit:

```powershell
git config user.name
git config user.email
```

Mỗi máy cần Python 3.10 trở lên. Tạo lại dữ liệu làm việc; `runs/` và `data_source/` đã được Git bỏ qua:

```powershell
py -X utf8 scripts/download_public.py
py -X utf8 scripts/inject_release.py --seed 98007 --out runs/r98007
py -X utf8 validator/build_review.py runs/r98007/delivery --candidates submission/r98007/candidates.json --out runs/r98007/review.html
```

Mở `runs/r98007/review.html` bằng trình duyệt và lọc đến mã ảnh được giao.

## 3. Ghi kết quả riêng, tránh xung đột

Tạo nhánh theo bảng phân công, ví dụ với Minh:

```powershell
git switch -c review/minh-p2
```

Tạo file `submission/member_reviews/<MSHV>.csv` với đúng bốn cột:

```csv
image,type,verdict,note
000000001818,bbox_drift,rejected,"NGUYỄN KHOA MINH: mô tả cụ thể vật thể, box và mask đã quan sát; tối thiểu 20 ký tự"
```

Quy tắc:

- `verdict` chỉ dùng `confirmed` hoặc `rejected`. Ca chưa đủ căn cứ ghi `uncertain` trong note và báo Hùng, không tự thêm vào `errors.json`.
- Note phải bắt đầu bằng họ tên người trực tiếp xem và mô tả bằng chứng quan sát được.
- Không sửa `submission/r98007/review_log.csv`, `errors.json` hoặc lineage trên nhánh cá nhân.
- Không commit `runs/`, `data_source/`, delivery hoặc file ZIP.

Commit và push nhánh:

```powershell
git add submission/member_reviews/<MSHV>.csv
git commit -m "review(p2): xác nhận ca được phân công"
git push -u origin <tên-nhánh>
```

Sau đó gửi link nhánh hoặc pull request cho Hùng. Không cần gửi mật khẩu hay token GitHub.

## 4. Hùng tổng hợp

Hùng kiểm tra từng file thành viên, xử lý trường hợp hai người kết luận khác nhau, rồi cập nhật `submission/r98007/review_log.csv`. Mỗi dòng cuối phải ghi tên người trực tiếp xem. Chỉ dòng `confirmed` mới được gộp vào `errors.json`.

Sau khi merge đủ sáu nhánh:

```powershell
py -X utf8 scripts/merge_review.py --rules runs/r98007/rules.json --review runs/r98007/review_log.csv --out runs/r98007/errors.json
py -X utf8 scripts/export_submission.py --run runs/r98007
py -X utf8 scripts/check_handover.py --run runs/r98007
py -X utf8 -m unittest discover -s tests -v
```

Nếu nội dung `errors.json` thay đổi, phải tạo lại handover v2, đóng gói lại và cập nhật lineage trước khi push `main`.

## 5. Điều kiện hoàn thành

- Sáu thành viên đều có file review mang tên/MSHV của mình và commit bằng email của mình.
- Mỗi dòng review có bằng chứng quan sát, không dùng kết luận do AI tự điền.
- Mọi lỗi semantic trong `errors.json` có dòng `confirmed` tương ứng.
- `check_handover.py` không có FAIL và toàn bộ unit test đạt.
- Hùng chỉ merge/push `main` sau khi đã kiểm tra các điều kiện trên.

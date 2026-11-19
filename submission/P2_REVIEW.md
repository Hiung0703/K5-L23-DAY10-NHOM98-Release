# P2 — Hồ sơ kiểm tra hỗ trợ

- Phụ trách đối chiếu: **CAO THỊ THÚY HIỀN**.
- Phụ trách công cụ: **NGUYỄN XUÂN ANH**.
- Nguồn phân tích hỗ trợ ban đầu: Codex, theo yêu cầu người dùng ngày 2026-11-19.
- **Xác nhận thực hiện:** ngày 2026-11-19, người dùng xác nhận CAO THỊ THÚY HIỀN và NGUYỄN XUÂN ANH đã trực tiếp xem ảnh, kiểm tra và xác nhận kết quả P2. Ghi nhận này dựa trên xác nhận của người dùng; lịch sử hỗ trợ ban đầu được giữ lại.
- Phạm vi: đã xem 19 ca ban đầu trên 18 ảnh, ảnh gốc cho các ca phân loại khó và đối chiếu box/mask; không phải kiểm tra toàn bộ 250 ảnh.
- Kết quả được ghi nhận theo xác nhận người dùng: 7 lỗi có bằng chứng trên 7 ảnh (bao gồm một ca bổ sung missing_box), 12 gợi ý ban đầu bị loại, 1 ca vẫn chưa chắc chắn. Các nhãn supported/rejected/uncertain bên dưới giữ nguyên dấu vết phân tích ban đầu; đây không phải số liệu F1.
- Giữ riêng [dữ liệu phân tích](../runs/r98007/p2_advisory.json), [ứng viên trước sửa](../runs/r98007/candidates.before_visual_review.json). Các file runs và ảnh bằng chứng chỉ có trong máy làm việc, không được commit theo RULES.
- Cập nhật này chỉ ghi nhận người thực hiện, chưa tạo review_log.csv hoặc gộp kết quả vào errors.json. Quyết định HOLD v1 đã được ghi ở P3 trên cơ sở 10 lỗi luật; chưa release v2. Không tự suy đoán kết luận cho ca uncertain hoặc người xem riêng từng dòng ngoài xác nhận chung nêu trên.

## Bằng chứng từng ca

### 1. 000000001000 — instance_merge

- Đánh giá hỗ trợ: **rejected**; gợi ý gốc: instance_merge; segment 4542047.
- Mask chỉ thuộc người mặc váy tối, đội mũ sáng ở giữa bên phải. Box person #10 khớp segment (IoU 0,972); #9 và #11 là hai người bên cạnh.
- [Ảnh gốc](../runs/r98007/delivery/images/000000001000.jpg) · [Overlay đã xem](../runs/r98007/p2_case_0.png).

### 2. 000000001818 — bbox_drift

- Đánh giá hỗ trợ: **rejected**; gợi ý gốc: bbox_drift; segment 8092282.
- Box zebra #1 ôm con phía trước đang cúi đầu bú; mask ứng viên thuộc con lớn phía sau. Đây là ghép nhầm hai cá thể, chưa phải box bị dịch.
- [Ảnh gốc](../runs/r98007/delivery/images/000000001818.jpg) · [Overlay đã xem](../runs/r98007/p2_case_1.png).

### 3. 000000002153 — instance_merge

- Đánh giá hỗ trợ: **rejected**; gợi ý gốc: instance_merge; segment 5784894.
- Mask thuộc trọng tài áo xanh ngồi thấp phía trước; box person #1 khớp (IoU 0,993). #2 là người đánh bóng, #5 là catcher, không phải hai phần của mask.
- [Ảnh gốc](../runs/r98007/delivery/images/000000002153.jpg) · [Overlay đã xem](../runs/r98007/p2_case_2.png).

### 4. 000000008277 — instance_merge

- Đánh giá hỗ trợ: **rejected**; gợi ý gốc: instance_merge; segment 674121.
- Mask thuộc miếng broccoli giữa phía phải khay; box #4 khớp (IoU 0,977). Hai box #12/#13 là miếng lân cận chạm vào mask.
- [Ảnh gốc](../runs/r98007/delivery/images/000000008277.jpg) · [Overlay đã xem](../runs/r98007/p2_case_3.png).

### 5. 000000008844 — instance_merge

- Đánh giá hỗ trợ: **rejected**; gợi ý gốc: instance_merge; segment 3709110.
- Mask chỉ phủ quả chuối nhỏ gần giữa cụm bên phải; box banana #2 khớp (IoU 0,982). Box #3/#5 bao các cụm chuối lớn lân cận.
- [Ảnh gốc](../runs/r98007/delivery/images/000000008844.jpg) · [Overlay đã xem](../runs/r98007/p2_case_4.png).

### 6. 000000012748 — class_swap

- Đánh giá hỗ trợ: **supported**; gợi ý gốc: class_disagreement; segment 2369328.
- Ảnh gốc cho thấy đầu ngựa có tai dài dựng, bờm và mõm thuôn bên người bế em bé. Panoptic horse phù hợp; detection #1 ghi cow.
- [Ảnh gốc](../runs/r98007/delivery/images/000000012748.jpg) · [Overlay đã xem](../runs/r98007/p2_case_5.png).

### 7. 000000013923 — instance_merge

- Đánh giá hỗ trợ: **rejected**; gợi ý gốc: instance_merge; segment 4080824.
- Mask phủ chiếc ghế đỏ trước bàn tròn. Box chair #5 khớp (IoU 0,985); #4 thuộc ghế phía sau và #19 thuộc ghế phía trước.
- [Ảnh gốc](../runs/r98007/delivery/images/000000013923.jpg) · [Overlay đã xem](../runs/r98007/p2_case_6.png).

### 8. 000000014831 — missing_box

- Đánh giá hỗ trợ: **uncertain**; gợi ý gốc: missing_box; segment 5594996.
- Ảnh chỉ cho thấy cận cảnh bộ lông nâu trắng, không thấy mặt hoặc toàn thân để xác định chắc loài. File detection chỉ có bed; panoptic ghi cat nhưng riêng điều đó không chứng minh nhãn cat đúng. Cần người xem xác nhận ngữ nghĩa trước khi báo thiếu cat.
- [Ảnh gốc](../runs/r98007/delivery/images/000000014831.jpg) · [Overlay đã xem](../runs/r98007/p2_case_7.png).

### 9. 000000014888 — missing_box

- Đánh giá hỗ trợ: **rejected**; gợi ý gốc: missing_box; segment 2766656.
- Vùng thân/bầu vú bò vẫn có một dòng box detection, nhưng class là 80 ngoài danh sách. Đây đã là invalid_class của P1, không phải mất box. Bộ đọc P2 cũ loại bỏ dòng sai class nên gây ứng viên thiếu box.
- [Ảnh gốc](../runs/r98007/delivery/images/000000014888.jpg) · [Overlay đã xem](../runs/r98007/p2_case_8.png).

### 10. 000000015517 — instance_merge

- Đánh giá hỗ trợ: **rejected**; gợi ý gốc: instance_merge; segment 6443848.
- Bãi có nhiều xe buýt che nhau. Box bus #4 đã khớp segment (IoU 0,976); box #6/#7 thuộc xe lân cận. Không có đủ bằng chứng một segment gộp hai xe khác nhau.
- [Ảnh gốc](../runs/r98007/delivery/images/000000015517.jpg) · [Overlay đã xem](../runs/r98007/p2_case_9.png).

### 11. 000000017115 — instance_merge

- Đánh giá hỗ trợ: **supported**; gợi ý gốc: instance_merge; segment 4474975.
- Có hai ngựa vằn đứng cạnh nhau, hai thân và hai cặp chân tách biệt. Cùng segment 4474975 tô cả hai con trong box zebra #1 và #2; dấu hiệu gộp hai instance rõ.
- [Ảnh gốc](../runs/r98007/delivery/images/000000017115.jpg) · [Overlay đã xem](../runs/r98007/p2_case_10.png).

### 12. 000000017959 — instance_merge

- Đánh giá hỗ trợ: **rejected**; gợi ý gốc: instance_merge; segment 2365329.
- Mask thuộc dải diều hẹp giữa các diều cá; box kite #17 khớp (IoU 0,983). Các box #12/#13 chạm vùng mask nhưng là diều khác.
- [Ảnh gốc](../runs/r98007/delivery/images/000000017959.jpg) · [Overlay đã xem](../runs/r98007/p2_case_11.png).

### 13. 000000017959 — instance_merge

- Đánh giá hỗ trợ: **rejected**; gợi ý gốc: instance_merge; segment 3616632.
- Mask thuộc một diều hình cá ở giữa phía trên; box kite #12 khớp (IoU 0,993). Box #14/#16 rộng, bao các diều khác và chồng vùng mask.
- [Ảnh gốc](../runs/r98007/delivery/images/000000017959.jpg) · [Overlay đã xem](../runs/r98007/p2_case_12.png).

### 14. 000000018380 — instance_merge

- Đánh giá hỗ trợ: **rejected**; gợi ý gốc: instance_merge; segment 2436446.
- Mask thuộc một người ở giữa nhóm phía sau bàn ăn, có box person #22 khớp (IoU 0,979). #25/#26 là người ở phía dưới/trên, không chứng minh gộp.
- [Ảnh gốc](../runs/r98007/delivery/images/000000018380.jpg) · [Overlay đã xem](../runs/r98007/p2_case_13.png).

### 15. 000000019109 — instance_merge

- Đánh giá hỗ trợ: **rejected**; gợi ý gốc: instance_merge; segment 4865587.
- Mask thuộc một xe máy trong dãy đỗ, có box motorcycle #6 khớp (IoU 0,974). Hai box #5/#8 là xe bên cạnh chạm mask.
- [Ảnh gốc](../runs/r98007/delivery/images/000000019109.jpg) · [Overlay đã xem](../runs/r98007/p2_case_14.png).

### 16. 000000020333 — class_swap

- Đánh giá hỗ trợ: **supported**; gợi ý gốc: class_disagreement; segment 4617106.
- Vùng được đánh dấu là cà vạt hồng thắt ở cổ áo trẻ, rủ xuống trước thân, không phải nĩa. Panoptic tie phù hợp; detection fork sai.
- [Ảnh gốc](../runs/r98007/delivery/images/000000020333.jpg) · [Overlay đã xem](../runs/r98007/p2_case_15.png).

### 17. 000000022935 — instance_merge

- Đánh giá hỗ trợ: **supported**; gợi ý gốc: instance_merge; segment 9984846.
- Ảnh cho thấy hai cầu thủ tách biệt: người áo tím phía trước và người áo cam phía sau. Cùng segment 9984846 tô cả hai người, trong hai box person riêng.
- [Ảnh gốc](../runs/r98007/delivery/images/000000022935.jpg) · [Overlay đã xem](../runs/r98007/p2_case_16.png).

### 18. 000000023126 — category_swap

- Đánh giá hỗ trợ: **supported**; gợi ý gốc: class_disagreement; segment 3158064.
- Ảnh gốc có người đứng trên lưng ngựa; vùng mask có đầu ngựa, bờm và thân ngựa, không phải cừu. Detection horse phù hợp; panoptic sheep sai.
- [Ảnh gốc](../runs/r98007/delivery/images/000000023126.jpg) · [Overlay đã xem](../runs/r98007/p2_case_17.png).

### 19. 000000025560 — class_swap

- Đánh giá hỗ trợ: **supported**; gợi ý gốc: class_disagreement; segment 9081758.
- Ảnh gốc cho thấy mèo nâu trắng trên kệ trước TV, có đuôi dài và chân mèo. Panoptic cat phù hợp; detection dog sai.
- [Ảnh gốc](../runs/r98007/delivery/images/000000025560.jpg) · [Overlay đã xem](../runs/r98007/p2_case_18.png).

### 20. 000000001818 — missing_box

- Đánh giá hỗ trợ: **supported**; gợi ý gốc: manual_followup; segment 8092282.
- Ảnh có hai ngựa vằn: con lớn phía sau và con nhỏ đang bú. File nhãn chỉ có một box zebra ôm con nhỏ (x từ 178 đến 640); con lớn chiếm phần trái/phía sau không có box riêng. Đây là đề xuất bổ sung sau khi loại gợi ý drift.
- [Ảnh gốc](../runs/r98007/delivery/images/000000001818.jpg) · [Overlay đã xem](../runs/r98007/p2_case_1.png).

## Thay đổi kỹ thuật từ bằng chứng

- Bỏ gợi ý instance_merge khi đã có box cùng lớp khớp segment với IoU ≥ 0,85 và phủ mask ≥ 0,9. Khắc phục việc lựa hai box lân cận dù đã có box đúng.
- Giữ hình học box có class không hợp lệ để không báo nhầm missing_box; không biến dòng sai class thành ứng viên class_swap. Lỗi class vẫn do P1 xử lý.
- Chưa tự sửa thuật toán ghép chỉ theo một ảnh zebra; ghi đề xuất missing_box cho thành viên xem lại. Cần phát triển ghép một-một giữa box và segment để giảm ghép nhầm nhiều vật che nhau.
- Không dùng F1 để dò đáp án, không đọc ground truth, không sửa delivery hoặc script đề. Không thể suy ra recall từ 0 ứng viên trên lô sạch.

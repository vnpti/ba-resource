# Visual QA — Anki BA 1.0.1, trang 116–165

- Ngày: 2026-11-03.
- Status: DONE.
- Phạm vi: 50/50 trang PNG `plans/2026-11-03-oracle-ba-refresh/render/page-116.png` đến `page-165.png` của bản 215 trang.
- Phương pháp: mở từng trang bằng `view_image`, mức `original`; kiểm trực tiếp chữ, bảng, ngắt trang, lề và footer. Không suy kết quả từ contact sheet hoặc độ giống pixel. Không render lại, không sửa source.

## Kết quả

Không phát hiện lỗi cần sửa trong 50 trang được giao: không cắt chữ, mất dấu Việt, chữ chồng nhau, nội dung tràn lề/đè footer, trang trắng hoặc tiêu đề đứng riêng không có nội dung đi kèm.

| Trang đã xem riêng từng ảnh | Kết quả | Ghi nhận |
|---|---|---|
| 116–122 | PASS | User stories và bảng INVEST đọc rõ. Bảng sang trang có lặp header; không thấy hàng bị xén. Trang 122 có khoảng trắng cuối phần, không phải trang trắng. |
| 123–136 | PASS | AC và nguồn oracle đọc rõ; các đoạn tiếp nối trang không mất dòng. |
| 137–142 | PASS | AC067, AC072, AC077 cập nhật hiển thị đầy đủ; timestamp/hash dài xuống dòng trong lề. Cụ thể AC072 ở trang 139, AC077 ở trang 140. |
| 143–159 | PASS | Metadata và test cases rõ. “Steps” cuối trang có ít nhất một bước đi kèm; không còn nhãn Steps đứng riêng. |
| 160–165 | PASS | TC035 cập nhật ở trang 160 hiển thị đầy đủ fixture, request, expected và giới hạn oracle. Các test case tiếp theo không chồng dòng hoặc đè footer. |

## Phân trang được chấp nhận

Một số AC/TC bắt đầu bằng tiêu đề cùng metadata cuối trang, rồi tiếp tục scenario/steps ở trang sau: ví dụ 127–130, 133–136, 144–148, 150–157. Đây là đoạn tiếp nối có nội dung đi kèm, không phải tiêu đề đơn độc. Không yêu cầu sửa.

Không có sơ đồ trong phạm vi đã kiểm. Báo cáo chỉ xác nhận chất lượng trình bày của các trang 116–165; không xác nhận việc chạy test hoặc tính đúng nghiệp vụ.

## Câu hỏi còn mở

Không có.

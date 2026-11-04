# Visual QA bản Anki BA 1.0.1 — phần 1

- Ngày: 2026-11-03.
- Status: DONE.
- Kết quả: PASS trong phạm vi 50 trang được giao; không có lỗi trình bày cần sửa.
- Artifact: `plans/2026-11-03-oracle-ba-refresh/render/page-N.png`, bộ 215 trang đã render sẵn.
- Phương pháp: mở và đọc trực tiếp từng PNG bằng `view_image`, `detail: original`; không dùng contact sheet để thay thế kiểm tra trang; không render lại.

## Phạm vi đã kiểm tra

50/50 trang: **1, 3, 4, 13–35, 83–88, 98–115**.

Danh sách đầy đủ: 1, 3, 4, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 83, 84, 85, 86, 87, 88, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115.

## Kết quả quan sát

- Chữ tiếng Việt và ký tự kỹ thuật đọc được; không thấy glyph hỏng, chữ đè nhau hoặc nội dung bị cắt ở lề.
- Bảng nằm trong vùng trang, không thấy hàng bị cắt qua hai trang. Bảng dài lặp tiêu đề đúng tại phần tiếp theo.
- Tiêu đề có nội dung đi kèm; không thấy tiêu đề đứng lẻ ở cuối trang, trang trắng bất thường hoặc trang chỉ chứa footer.
- SRS, ma trận nguồn, use case và backlog có ngắt trang dài nhưng vẫn đọc liên tục. Ví dụ bảng 111→112, 113→114 giữ nguyên hàng và có header lặp; mục US-ANKI-11 ở trang 114 có cả đoạn mô tả trước khi tiếp sang trang 115.
- Trang 26 có từ kỹ thuật xuống dòng trong cột hẹp; vẫn đọc được, không coi là lỗi chặn phát hành.

Trang bị ảnh hưởng cần sửa: **không có**. Không thay đổi source, nội dung tài liệu hoặc cấu hình xuất bản.

## Giới hạn và câu hỏi còn mở

Đây là kiểm tra trình bày của 50 PNG đã nêu, không phải kiểm thử Anki hay phê duyệt nghiệp vụ, và không thay thế kiểm tra các trang do thành viên khác phụ trách. Không có câu hỏi còn mở trong phạm vi visual QA này.

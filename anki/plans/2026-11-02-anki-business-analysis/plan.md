# Phân tích nghiệp vụ Anki

- Ngày: 2026-11-02 (Asia/Ho_Chi_Minh).
- Trạng thái: hoàn tất trong phạm vi phân tích tĩnh.
- Mục tiêu: tái lập mô hình nghiệp vụ, luồng người dùng, quy tắc, dữ liệu và mô hình duy trì sản phẩm từ repo Anki; dùng REA theo yêu cầu.
- Phạm vi: Anki Desktop; hệ sinh thái chỉ ở mức ranh giới tích hợp và nguồn duy trì dự án.
- Không thực hiện: sửa/build/chạy Anki, đăng nhập/sync dữ liệu cá nhân, phân tích nội bộ dịch vụ AnkiWeb hoặc ứng dụng di động.
- Nguồn cố định: `sources/anki`, commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`, `.version` = `26.09.3`.

## Các bước

1. Đọc README và hướng dẫn repo; xác định ranh giới — hoàn tất.
2. REA phân tích tĩnh `ts/routes/deck-options`; lưu Evidence — hoàn tất.
3. Đối chiếu nghiệp vụ học và nghiệp vụ nội dung/sync với source và manual — hoàn tất.
4. Tổng hợp báo cáo tiếng Việt; kiểm tra liên kết, phân biệt chứng cứ và suy luận — hoàn tất.

## Tiêu chí hoàn tất

- Có phân khúc người dùng, giá trị, capability map, mô hình dữ liệu, luồng chính và ngoại lệ.
- Có các quy tắc nghiệp vụ dẫn tới source hoặc manual tại commit đã chốt.
- Phân biệt chức năng đã có với đề xuất/KPI; không bịa số liệu thị trường/doanh thu.
- Công bố Evidence ID, phạm vi/giới hạn REA, chưa kiểm thử runtime.
- Báo cáo chính tại `docs/anki-business-analysis.md`; bằng chứng REA tại `evidence/rea-deck-options.json`.

## Phân công

- `learning_business`: báo cáo riêng `plans/reports/learning-business.md`.
- `content_business`: báo cáo riêng `plans/reports/content-business.md`.
- Controller: REA, mô hình sản phẩm/kinh doanh, tổng hợp và kiểm chứng tài liệu.

## Xác minh cuối

- 123 liên kết local/source cố định: file tồn tại, dòng trích dẫn trong giới hạn.
- JSON Evidence đọc được, có 5 records; parent Evidence ID trong bản trích xuất khớp bundle.
- SHA-256 của `ts/routes/deck-options/lib.ts` khớp với bằng chứng REA.
- Reviewer nghiệp vụ nội dung không tìm thấy lỗi thực tế trọng yếu trong báo cáo chính.
- Checkout upstream giữ sạch, đúng commit đã chốt. Không build/test/run ứng dụng vì không thay đổi source; runtime là giới hạn được công bố.
- Docs impact: tạo bộ tài liệu khảo sát tại workspace này; không sửa docs upstream.
- Điểm còn mở được lưu ở cuối báo cáo chính và các phụ lục, không chặn bàn giao khảo sát tĩnh.

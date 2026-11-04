# Làm rõ bốn oracle và xuất lại bộ BA

- Ngày: 2026-11-03. Trạng thái: hoàn tất.
- Mục tiêu: chốt expected cho AC/TC-ANKI-035, 067, 072, 077 từ caller, implementation và test source; đồng bộ BA và xuất đủ HTML/DOCX/PDF/ZIP.
- Baseline source: commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`; không đổi source, không thực hiện sync/account thật. Runtime tests giữ Not Run.
- Bản phát hành: Draft 1.0.1; chỉ nâng phiên bản tài liệu thực sự thay đổi. Giữ lịch sử và các câu hỏi ngoài phạm vi.
- Bản ZIP cũ giữ ở `dist/archive/anki-ba-1.0.0.zip` trong workspace.

## Công việc đã hoàn tất

1. Truy vết FSRS, retention, profile và media; lập fixture và nhánh kết quả có source anchor.
2. Cập nhật SRS/BR, AC/TC, JSON/CSV, use case và governance bị ảnh hưởng.
3. Review chéo oracle, kiểm tra liên kết, độ phủ và 82 ca không thuộc phạm vi thay đổi.
4. Xuất HTML/Word/PDF, kiểm tra bản render 215 trang, đóng gói manifest và SHA-256.

## Phân công

- learning_business: khảo sát 035; review chéo sync/media; visual QA phần 1.
- ba_quality: khảo sát 067; review tích hợp; visual QA phần 3.
- content_business: khảo sát 072/077; visual QA phần 2.
- Root: tích hợp tài liệu, kiểm chứng, xuất và đóng gói.

## Kết quả theo tiêu chí bàn giao

- Bốn ca có fixture xác định, steps, expected quan sát được và nguồn caller → branch; các giới hạn của server thử nghiệm được ghi rõ.
- 86/86 AC có oracle đã đặc tả; 86 TC vẫn Not Run. Không biến bằng chứng source thành kết quả runtime.
- 12 tài liệu Markdown nâng patch 1.0.1; 12 tài liệu không đổi giữ 1.0.0; SRS và QA JSON/CSV đồng bộ. Không đổi ID.
- 82 AC/TC còn lại giữ nguyên nội dung catalog theo so sánh với ZIP 1.0.0.
- 24 tài liệu, 20 FR, 28 BR, 8 ERR, 8 NFR, 10 use case, 20 user story và 6 sơ đồ.
- HTML desktop/mobile: đủ 24 tài liệu và 6 sơ đồ, không broken anchor, không tràn ngang.
- PDF 215 trang: 150 trang thay đổi được mở kiểm riêng; 65 trang có nội dung pixel giống bản trước đã review (không tính footer). Không có lỗi visual cần sửa.
- Word chứa 24 bookmarks, 6 hình sơ đồ; PDF có đủ 86 AC và 86 TC. Không lỗi glyph thay thế trong text trích xuất.
- Không sửa source, build, chạy ứng dụng hoặc upstream tests. Bằng chứng REA cũ giữ nguyên; bổ sung báo cáo source và SHA-256.

## Bằng chứng và câu hỏi còn mở

- [Kiểm tra cấu trúc và độ phủ](validation.json).
- [Kiểm tra HTML](html-validation.json).
- [Kiểm tra bản xuất](export-validation.json).
- [Danh sách tài liệu thay đổi](changed-documents.json).
- [Review tích hợp](../reports/2026-11-03-integrated-oracle-review.md).
- [Visual 1](../reports/2026-11-03-visual-part1.md), [Visual 2](../reports/2026-11-03-visual-part2.md), [Visual 3](../reports/2026-11-03-visual-part3.md).

Còn mở: xác nhận nghiệp vụ To-Be cho khác biệt retention giữa manual và source; kiểm thử runtime/NFR và thẩm định của stakeholder. Hành vi hosted AnkiWeb chưa được kiểm chứng. Chi tiết nằm trong governance của bộ BA.

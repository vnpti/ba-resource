# Phân tích nghiệp vụ Anki

Bộ phân tích tiếng Việt cho [ankitects/anki](https://github.com/ankitects/anki), thực hiện ngày 02/11/2026 bằng đọc source/manual và phân tích tĩnh REA.

- [Báo cáo chính: Business / nghiệp vụ](docs/anki-business-analysis.md).
- [Chi tiết học và lập lịch](plans/reports/learning-business.md).
- [Chi tiết nội dung, import/export và đồng bộ](plans/reports/content-business.md).
- [REA Evidence đầy đủ](evidence/rea-deck-options.json) và [trích xuất liên quan nghiệp vụ](evidence/rea-business-extract.json).
- [Phạm vi, tiêu chí và trạng thái công việc](plans/2026-11-02-anki-business-analysis/plan.md).

Source nằm ở `sources/anki`, cố định tại commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`; `.version` là `26.09.3`. Không sửa source upstream, build hoặc chạy ứng dụng. REA khảo sát thư mục TypeScript `ts/routes/deck-options`; quy tắc Rust/Python và nghiệp vụ còn lại được đối chiếu trực tiếp trong source/manual.

Các liên kết GitHub trong báo cáo chính cố định theo commit. Source line trong phụ lục trỏ đến checkout cục bộ. Đây là báo cáo khảo sát, không phải tài liệu chính thức của dự án Anki.

## Bộ tài liệu BA để bàn giao

- [Mở bản HTML offline](dist/anki-ba-documentation.html).
- [Word chỉnh sửa được](dist/anki-ba-documentation.docx) · [PDF](dist/anki-ba-documentation.pdf).
- [Danh mục tài liệu nguồn](docs/anki/00-index.md). Gói phân phối: `dist/documentation-bundle.zip` (file ZIP không tự chứa chính nó).

Draft 1.0.1 (cập nhật 03/11/2026): 24 tài liệu, 20 FR, 28 BR, 8 ERR, 8 NFR, 10 use case, 20 user story, 86 AC/test case và 6 sơ đồ. Độ phủ thiết kế: FR 20/20, BR 28/28, ERR 8/8; AC có oracle hợp lệ 86/86. Tất cả test case ở trạng thái Not Run; 4 case035/067/072/077 đã chốt oracle từ source với fixture và giới hạn cụ thể. Câu hỏi mở và vai trò thẩm định nằm trong hồ sơ bàn giao.

Bộ ZIP giữ nguyên cây thư mục để liên kết tương đối hoạt động. Mở `dist/anki-ba-documentation.html` sau khi giải nén; liên kết GitHub cần mạng. JSON bằng chứng REA giữ nguyên provenance của lần khảo sát, kể cả đường dẫn máy khảo sát.

Bốn ca đã làm rõ: Optimize zero-item giữ params; retention tính cả hai log/card/ngày; profile cùng account theo Cancel/Download/Upload; media theo cursor/dirty/thứ tự sync. Source commit không đổi. Bản ZIP1.0.0 được lưu riêng trong `dist/archive/` tại workspace.

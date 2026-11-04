---
id: DOC-UC-ANKI-010
title: "UC-ANKI-010: Quản lý môi trường học cục bộ và phục hồi"
version: "1.0.1"
phase: Specification
domain: UseCases
tags: [anki, as-is, cockburn, draft]
depends_on: [FR-SYS-PROF-001, FR-DAT-BACK-001, FR-EXT-ADD-001]
related_diagrams: [DIAG-CTX-ANKI-001]
author: BA Agent
last_updated: "2026-11-03"
status: draft
---

# UC-ANKI-010 — Quản lý môi trường học cục bộ và phục hồi

**As-Is — DRAFT v1.0.1.** Nguồn cố định commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`; chưa thực thi runtime. FR/BR/ERR tham chiếu catalog [requirements.json](../srs/requirements.json) v1.0.1, không phải mã lỗi native hay HTTP do Anki công bố.

## Lịch sử sửa đổi

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---|---|---|---|
| 1.0.1 | 2026-11-03 | BA Analysis | Làm rõ oracle035/067/072/077 và truy vết liên quan; không thay source hoặc kết quả chạy |
| 1.0.0 | 2026-11-02 | BA Agent | Baseline As-Is, luồng chính/extension và truy vết source |

## Hợp đồng use case

| Thuộc tính | Giá trị |
|---|---|
| Primary Actor | Người dùng quản lý ứng dụng cục bộ |
| Scope | Anki Desktop, collection/profile cục bộ; server chỉ trong luồng sync được nêu |
| Level | Kite level |
| Stakeholders & interests | Người dùng cần tách collection và phục hồi đúng dữ liệu; tác giả addon cần biết phạm vi lifecycle; không có actor Admin/Super Admin được suy diễn. |
| Supporting actors | Không cần actor người hỗ trợ; backend/scheduler là thành phần nội bộ, không role RBAC |
| Trigger | Cần chuyển profile, bảo toàn/phục hồi dữ liệu hoặc quản lý extension. |
| Pre-conditions | Anki Desktop có thể mở profile manager; có backup hợp lệ nếu chọn restore; addon source/package có sẵn nếu chọn extension. |
| Success guarantees | Profile được chọn đúng collection/settings; backup/restore hoặc addon branch có kết quả riêng được kiểm tra; không gán quyền RBAC giả. |
| Minimal guarantees | Addon dùng chung profile; restore có thể mất thay đổi sau snapshot; không bảo đảm auto-backup chứa media hay mọi hook chạy khi import. |
| Functional scope | FR-SYS-PROF-001, FR-DAT-BACK-001, FR-EXT-ADD-001 |

## Main Success Scenario

1. Người dùng mở Switch Profile và chọn profile cần làm việc; hệ thống mở collection/settings tương ứng.
2. Người dùng chọn mục tiêu bảo toàn dữ liệu, phục hồi hoặc quản lý addon; các mục tiêu là nhánh độc lập, không phải chuỗi bắt buộc.
3. Ở đường bảo toàn dữ liệu, người dùng chọn Export collection .colpkg với Include Media nếu cần bản sao có ảnh/âm thanh.
4. Hệ thống tạo file package; người dùng kiểm tra vị trí và giữ bản sao ngoài thiết bị nếu theo quy trình backup của họ.
5. Người dùng quay về profile và tiếp tục học; quan sát trạng thái sync/backup theo thao tác đã thực hiện.

## Extensions gắn bước

| Điểm rẽ | Điều kiện | Xử lý / điểm quay lại |
|---|---|---|
| 1a | Hai profile cùng account | Caller khảo sát không reject trùng account. Trên server test, mod khác/schema khác và hai bên nonempty: Cancel giữ nội dung; Download thay active local; Upload thay server, profile local khác chưa sync vẫn giữ dữ liệu cũ. Xem TC-ANKI-072; manual khuyến cáo tránh dùng chung account. |
| 2a | Chọn restore automatic backup | Switch Profile → Open Backup → chọn snapshot. Dữ liệu sau snapshot bị mất; auto-sync/backup tạm tắt tới khi đóng và mở lại ứng dụng sau khi kiểm tra bản phục hồi. |
| 2b | Chọn Create Backup thay vì Export Media | Tạo kiểu backup tự động text/scheduling, không media; source bỏ nếu collection chưa đổi kể cả force. Không báo có snapshot mới khi thực tế guard bỏ qua. |
| 2c | Chọn quản lý addon | Dùng Tools Add-ons theo manual; addon là extension desktop dùng chung profile, không là quyền chỉ riêng profile này. Tác giả dùng hooks/filters đúng lifecycle. |
| 2d | Addon muốn chặn mọi đường thêm note | note_will_be_added không chạy khi import; phải kiểm tra hook đúng entry point, không tuyên bố chính sách được bao phủ mặc nhiên. |
| 5a | Sau restore muốn dùng lại auto-sync | Kiểm tra đúng snapshot rồi đóng/mở lại Anki; chọn hướng full sync có chủ đích nếu được yêu cầu. |

## Business Rules và lỗi liên quan

| Mã | Ràng buộc đã quan sát |
|---|---|
| BR-ANKI-027 | Mỗi profile giữ collection/settings và sync auth riêng, addon dùng chung. Caller khảo sát không reject account trùng profile; cùng user SimpleServer dẫn tới cùng server collection. Với local/remote nonempty, mod khác và schema khác: cho Upload/Download; Cancel không transfer, Download thay local, Upload thay server; profile local khác chưa sync không tự thay đổi. Giới hạn: Manual khuyến cáo một account cho một profile để tránh ghi đè, không phải guard uniqueness đã quan sát. Mod bằng có thể NoChanges; schema chung có thể normal merge. Không coi profile là tenant/RBAC. Hosted implementation chưa xác minh |
| BR-ANKI-022 | apkg bổ sung/cập nhật; colpkg thay collection và mang scheduling; tùy chọn media khi xuất. Ngoại lệ: Import colpkg không xóa media cũ ngoài package; không có scheduling thì bản chia sẻ loại dữ liệu scheduling và marked/leech |
| BR-ANKI-024 | Backup tự động giữ text/scheduling, không media; restore quay về snapshot và mất thay đổi sau đó. Ngoại lệ: Không đổi collection thì bỏ backup kể cả force; muốn có media xuất colpkg Include Media |
| BR-ANKI-026 | Hook gọi theo lifecycle; filter trả đối số biến đổi; nhiều addon gọi tuần tự. Ngoại lệ: note_will_be_added không áp dụng import; sync_did_finish không bảo đảm media hoàn tất |

Catalog chưa gán ERR riêng cho phạm vi này; không tự tạo mã lỗi hoặc status HTTP. Các nhánh thường (kết quả rỗng, hủy, đổi mode) không tự được coi là lỗi.

## Nguồn và kiểm chứng

- [docs-site/manual/profiles.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/profiles.mdx#L5)
- [rslib/src/collection/backup.rs:28](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/collection/backup.rs#L28)
- [docs-site/manual/backups.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L7)
- [docs-site/manual/backups.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L24)
- [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7)
- [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29)
- [docs-site/manual/backups.mdx:18](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L18)
- [docs-site/manual/addons.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L5)

Bổ sung đối chiếu 2026-11-03: [docs-site/manual/profiles.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/profiles.mdx#L5); [qt/aqt/profiles.py:212](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L212); [qt/aqt/profiles.py:659](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L659); [qt/aqt/profiles.py:681](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L681); [qt/aqt/sync.py:307](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L307); [rslib/src/sync/http_server/mod.rs:122](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/http_server/mod.rs#L122); [rslib/src/sync/collection/meta.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L59); [qt/aqt/sync.py:138](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L138); [rslib/src/sync/collection/download.rs:35](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/download.rs#L35); [rslib/src/sync/collection/upload.rs:79](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/upload.rs#L79); [rslib/src/sync/collection/tests.rs:591](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/tests.rs#L591).

## Giới hạn / câu hỏi mở

Phân tích Code/Docs theo snapshot; không có biên bản phê duyệt nghiệp vụ hoặc kết quả chạy kiểm thử. Thông báo UI/localization không được khẳng định bằng mã ERR phân tích. Owner xác nhận trước khi nghiệm thu runtime: maintainer phụ trách luồng và người dùng thử tác vụ.

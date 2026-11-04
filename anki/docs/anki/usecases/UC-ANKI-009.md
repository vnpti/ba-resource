---
id: DOC-UC-ANKI-009
title: "UC-ANKI-009: Đồng bộ collection và kiểm tra media"
version: "1.0.1"
phase: Specification
domain: UseCases
tags: [anki, as-is, cockburn, draft]
depends_on: [FR-DAT-SYNC-001, FR-DAT-MEDI-001]
related_diagrams: [DIAG-CTX-ANKI-001, DIAG-SEQ-ANKI-001]
author: BA Agent
last_updated: "2026-11-03"
status: draft
---

# UC-ANKI-009 — Đồng bộ collection và kiểm tra media

**As-Is — DRAFT v1.0.1.** Nguồn cố định commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`; chưa thực thi runtime. FR/BR/ERR tham chiếu catalog [requirements.json](../srs/requirements.json) v1.0.1, không phải mã lỗi native hay HTTP do Anki công bố.

## Lịch sử sửa đổi

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---|---|---|---|
| 1.0.1 | 2026-11-03 | BA Analysis | Làm rõ oracle035/067/072/077 và truy vết liên quan; không thay source hoặc kết quả chạy |
| 1.0.0 | 2026-11-02 | BA Agent | Baseline As-Is, luồng chính/extension và truy vết source |

## Hợp đồng use case

| Thuộc tính | Giá trị |
|---|---|
| Primary Actor | Người dùng nhiều thiết bị |
| Scope | Anki Desktop, collection/profile cục bộ; server chỉ trong luồng sync được nêu |
| Level | Sea level |
| Stakeholders & interests | Người dùng muốn tiếp tục học trên thiết bị khác; server là secondary actor, không phải role quản trị nội dung cục bộ. |
| Supporting actors | AnkiWeb hoặc sync server; client khác ngoài phạm vi source |
| Trigger | Chọn Sync hoặc ứng dụng kích hoạt auto-sync đã cấu hình. |
| Pre-conditions | Profile/endpoint hoặc AnkiWeb account được cấu hình; mạng/server khả dụng cho đường thành công; manual khuyến cáo một account cho một profile, không xem đây là guard runtime từ chối account trùng. |
| Success guarantees | Collection hoàn tất nhánh sync đã chọn; media có kết quả tiến trình riêng; vấn đề file thiếu/không dùng có thể được kiểm tra. |
| Minimal guarantees | Không coi collection sync xong là media đã xong; không bảo đảm giữ thay đổi cả hai phía khi full sync; lỗi chưa được xử lý không được báo là đồng bộ đầy đủ. |
| Functional scope | FR-DAT-SYNC-001, FR-DAT-MEDI-001 |

## Main Success Scenario

1. Người dùng bắt đầu Sync; hệ thống trao đổi metadata với endpoint.
2. Hệ thống xác định không đổi, normal sync hoặc full sync theo modified/schema.
3. Với normal sync, hệ thống trao đổi changes/chunks/graves, merge Note/Card theo USN và mtime, nhập revlog.
4. Hệ thống thông báo trạng thái collection; media tiếp tục/hoàn tất theo tiến trình riêng.
5. Người dùng chạy Check Media khi cần; hệ thống báo file không dùng và tham chiếu bị thiếu.
6. Người dùng kiểm tra kết quả và chỉ xử lý các file được chọn; sau đó chờ media sync đầy đủ trên thiết bị liên quan.

## Extensions gắn bước

| Điểm rẽ | Điều kiện | Xử lý / điểm quay lại |
|---|---|---|
| 2a | Cần full sync | Người dùng chọn Upload để giữ local hoặc Download để giữ remote trong hướng khả dụng; thao tác thay một phía collection. Sau Upload, thiết bị khác Download bản đó. |
| 3a | Hai thiết bị sửa field khác nhau của cùng note | Chọn toàn record theo logic mtime/usn; không merge field, nên có thể mất một thay đổi. |
| 3b | Mất mạng/server báo lỗi | Dừng báo thành công cho phần lỗi; giữ thông tin lỗi và thử lại theo UI. Chưa đặc tả wording/HTTP code chung vì catalog không gán một mã ERR cho mọi lỗi sync. |
| 4b | Media cùng tên chuẩn, khác checksum | Fetch remote change chưa nhận sẽ download ghi đè cả local dirty; nếu cursor đã bằng server, local dirty có thể upload. Cố định thứ tự/cursor theo TC-ANKI-077; không dùng mtime để chọn thắng. |
| 4a | One-way collection sync | Media vẫn merge riêng, không theo chiều Upload/Download của collection. |
| 5a | Static media chỉ được template tham chiếu | Check Media không quét question/answer templates; dùng quy ước tên bắt đầu _ cho tài nguyên tĩnh. |
| 6a | Xóa media trước khi sync media đầy đủ | Theo manual file trên server có thể được tải lại; hoàn tất sync trước khi muốn lan truyền xóa. |

## Business Rules và lỗi liên quan

| Mã | Ràng buộc đã quan sát |
|---|---|
| BR-ANKI-023 | Note/Card remote thay local khi local không pending hoặc remote mtime lớn hơn; revlog được nhập; khác schema yêu cầu full sync. Ngoại lệ: Không merge từng field; cùng mtime với local pending không thay local tại bước đó; upload/download chọn một phía collection |
| BR-ANKI-028 | Media sync riêng với collection; check tìm file thiếu/không dùng. Sync đăng ký thay đổi local, fetch remote mới trước upload pending. Tên chuẩn trùng nhưng hash khác: remote change chưa nhận làm download ghi đè dù local dirty rồi đánh clean. Nếu cursor đã bằng server và chỉ local dirty, upload thay server; winner phụ thuộc thứ tự request và cursor. Giới hạn: Không quét tham chiếu trong template; static media dùng _. Sequential từ nền trống C1→C2 nhận nội dung C1; không suy thành quy tắc first/last writer cho mọi race. Local add_file collision/filename normalization là nhánh khác; không bảo đảm rollback filesystem khi lỗi; oracle server test cùng commit |

Catalog chưa gán ERR riêng cho phạm vi này; không tự tạo mã lỗi hoặc status HTTP. Các nhánh thường (kết quả rỗng, hủy, đổi mode) không tự được coi là lỗi.

## Nguồn và kiểm chứng

- [rslib/src/sync/collection/chunks.rs:162](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/chunks.rs#L162)
- [rslib/src/sync/collection/meta.rs:65](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L65)
- [docs-site/manual/media.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/media.mdx#L24)
- [docs-site/manual/syncing.mdx:54](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/syncing.mdx#L54)
- [rslib/src/sync/collection/meta.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L59)
- [qt/tools/genhooks_gui.py:933](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/tools/genhooks_gui.py#L933)
- [docs-site/manual/syncing.mdx:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/syncing.mdx#L59)

Bổ sung đối chiếu 2026-11-03: [docs-site/manual/media.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/media.mdx#L24); [rslib/src/sync/media/syncer.rs:60](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/syncer.rs#L60); [rslib/src/sync/media/changes.rs:44](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/changes.rs#L44); [rslib/src/media/files.rs:403](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L403); [rslib/src/sync/media/database/client/mod.rs:206](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/client/mod.rs#L206); [rslib/src/sync/media/database/server/entry/upload.rs:35](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/server/entry/upload.rs#L35); [rslib/src/sync/media/tests.rs:278](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/tests.rs#L278); [rslib/src/backend/sync.rs:188](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/backend/sync.rs#L188); [rslib/src/sync/media/database/client/changetracker.rs:56](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/client/changetracker.rs#L56); [rslib/src/media/files.rs:165](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L165).

## Giới hạn / câu hỏi mở

Phân tích Code/Docs theo snapshot; không có biên bản phê duyệt nghiệp vụ hoặc kết quả chạy kiểm thử. Thông báo UI/localization không được khẳng định bằng mã ERR phân tích. Owner xác nhận trước khi nghiệm thu runtime: maintainer phụ trách luồng và người dùng thử tác vụ.

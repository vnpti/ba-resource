---
id: DOC-UC-ANKI-008
title: "UC-ANKI-008: Trao đổi deck và collection package"
version: "1.0.0"
phase: Specification
domain: UseCases
tags: [anki, as-is, cockburn, draft]
depends_on: [FR-DAT-PKG-001]
related_diagrams: [DIAG-CTX-ANKI-001]
author: BA Agent
last_updated: "2026-11-02"
status: draft
---

# UC-ANKI-008 — Trao đổi deck và collection package

**As-Is — DRAFT v1.0.0.** Nguồn cố định commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`; chưa thực thi runtime. FR/BR/ERR tham chiếu catalog [requirements.json](../srs/requirements.json) v1.0.0, không phải mã lỗi native hay HTTP do Anki công bố.

## Lịch sử sửa đổi

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---|---|---|---|
| 1.0.0 | 2026-11-02 | BA Agent | Baseline As-Is, luồng chính/extension và truy vết source |

## Hợp đồng use case

| Thuộc tính | Giá trị |
|---|---|
| Primary Actor | Người chia sẻ hoặc nhận nội dung |
| Scope | Anki Desktop, collection/profile cục bộ; server chỉ trong luồng sync được nêu |
| Level | Sea level |
| Stakeholders & interests | Người chia sẻ muốn người nhận có nội dung đúng; người nhận muốn giữ lịch cá nhân và hiểu thao tác thay collection. |
| Supporting actors | Không cần actor người hỗ trợ; backend/scheduler là thành phần nội bộ, không role RBAC |
| Trigger | Chọn export/import .apkg hoặc .colpkg. |
| Pre-conditions | Collection mở; có gói nguồn khi import hoặc phạm vi xuất; người dùng phân biệt bổ sung deck và thay collection. |
| Success guarantees | Export tạo gói theo phạm vi/options; import apkg thêm/cập nhật có điều kiện; import colpkg thay DB collection và restore media có trong gói. |
| Minimal guarantees | Không tuyên bố apkg merge toàn bộ lịch sử card cũ; không tuyên bố colpkg giữ các thay đổi collection ngoài gói. |
| Functional scope | FR-DAT-PKG-001 |

## Main Success Scenario

1. Người dùng chọn export deck .apkg, chọn phạm vi và Include Scheduling/Deck Presets/Media theo nhu cầu.
2. Hệ thống tạo package; người nhận chọn import package vào collection của họ.
3. Người nhận chọn chính sách update note/NoteType và có merge NoteType hay không.
4. Hệ thống đối chiếu note GUID, xử lý schema/field/template IDs và cập nhật theo policy.
5. Hệ thống thêm card ordinal còn thiếu, nhập review log gắn các card mới được thêm và báo kết quả.
6. Người dùng kiểm tra nội dung và tiếp tục sync nếu schema thay đổi.

## Extensions gắn bước

| Điểm rẽ | Điều kiện | Xử lý / điểm quay lại |
|---|---|---|
| 1a | Chọn .colpkg toàn collection | Xuất toàn collection có scheduling; Include Media quyết định asset có trong gói. |
| 2a | Import .colpkg | Thay collection hiện có; media cũ ngoài package không bị xóa. Backend kiểm tra DB tempfile, đổi schema, restore media rồi atomic rename; không dùng như additive apkg. |
| 1b | Bỏ Include Scheduling | Bản chia sẻ loại scheduling và tags marked/leech; không dùng để giữ tiến trình cá nhân. |
| 4a | Merge Normal với Cloze | ERR-ANKI-000-08: NotetypeKindMergeConflict; chọn cấu trúc/gói phù hợp, không tự ép merge. |
| 4b | Schema khác và không merge | Có thể tạo/remap NoteType; các note cũ lệch kiểu ghi conflict và không update như match hợp lệ. |
| 4c | Always nhưng mtime bằng nhau | Helper update note bỏ qua trường hợp timestamp bằng nhau; không diễn giải Always vô điều kiện tuyệt đối. |
| 5a | Card note/ordinal đã tồn tại | Không thay scheduling card cũ; review log trong gói của card cũ không được merge bằng nhánh thêm-card này. |

## Business Rules và lỗi liên quan

| Mã | Ràng buộc đã quan sát |
|---|---|
| BR-ANKI-021 | Nhận diện note bằng GUID; policy IfNewer/Always/Never; card cũ theo note/template giữ lịch, chỉ nhập log card mới. Ngoại lệ: Always vẫn bỏ khi mtime bằng nhau; không merge Normal/Cloze |
| BR-ANKI-022 | apkg bổ sung/cập nhật; colpkg thay collection và mang scheduling; tùy chọn media khi xuất. Ngoại lệ: Import colpkg không xóa media cũ ngoài package; không có scheduling thì bản chia sẻ loại dữ liệu scheduling và marked/leech |

| Mã lỗi BA | Trigger | Kết quả theo source |
|---|---|---|
| ERR-ANKI-000-08 | Merge NoteType Normal với Cloze trong package | Trả ImportError::NotetypeKindMergeConflict |

## Nguồn và kiểm chứng

- [rslib/src/import_export/package/apkg/import/notes.rs:333](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L333)
- [rslib/src/import_export/package/apkg/import/cards.rs:99](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/cards.rs#L99)
- [rslib/src/import_export/package/colpkg/import.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/colpkg/import.rs#L31)
- [docs-site/manual/exporting.mdx:34](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/exporting.mdx#L34)
- [rslib/src/import_export/package/apkg/import/notes.rs:521](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L521)

## Giới hạn / câu hỏi mở

Phân tích Code/Docs theo snapshot; không có biên bản phê duyệt nghiệp vụ hoặc kết quả chạy kiểm thử. Thông báo UI/localization không được khẳng định bằng mã ERR phân tích. Owner xác nhận trước khi nghiệm thu runtime: maintainer phụ trách luồng và người dùng thử tác vụ.

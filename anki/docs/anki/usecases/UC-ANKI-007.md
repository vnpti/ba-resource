---
id: DOC-UC-ANKI-007
title: "UC-ANKI-007: Nhập và cập nhật note từ text"
version: "1.0.0"
phase: Specification
domain: UseCases
tags: [anki, as-is, cockburn, draft]
depends_on: [FR-DAT-TEXT-001]
related_diagrams: [DIAG-CTX-ANKI-001]
author: BA Agent
last_updated: "2026-11-02"
status: draft
---

# UC-ANKI-007 — Nhập và cập nhật note từ text

**As-Is — DRAFT v1.0.0.** Nguồn cố định commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`; chưa thực thi runtime. FR/BR/ERR tham chiếu catalog [requirements.json](../srs/requirements.json) v1.0.0, không phải mã lỗi native hay HTTP do Anki công bố.

## Lịch sử sửa đổi

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---|---|---|---|
| 1.0.0 | 2026-11-02 | BA Agent | Baseline As-Is, luồng chính/extension và truy vết source |

## Hợp đồng use case

| Thuộc tính | Giá trị |
|---|---|
| Primary Actor | Người nhập nội dung |
| Scope | Anki Desktop, collection/profile cục bộ; server chỉ trong luồng sync được nêu |
| Level | Sea level |
| Stakeholders & interests | Người nhập muốn tránh duplicate/mất lịch; người học muốn dữ liệu cập nhật đúng NoteType. |
| Supporting actors | Không cần actor người hỗ trợ; backend/scheduler là thành phần nội bộ, không role RBAC |
| Trigger | Chọn File Import với plain text UTF-8 phân tách cột. |
| Pre-conditions | Có file text và NoteType đích; collection mở; người dùng chọn mapping/deck và duplicate policy. |
| Success guarantees | Các hàng được xử lý thành thêm/cập nhật/giữ hoặc nhóm lỗi; card cũ update note giữ lịch và deck. |
| Minimal guarantees | Lỗi hàng không đồng nghĩa toàn bộ import thất bại; không tạo duplicate của GUID đã tồn tại bằng lựa chọn Duplicate. |
| Functional scope | FR-DAT-TEXT-001 |

## Main Success Scenario

1. Người dùng chọn file; hệ thống xác định delimiter và hiển thị cấu hình/mapping.
2. Người dùng chọn NoteType, deck, map cột field/tags/GUID và match scope.
3. Người dùng chọn Update, Preserve hoặc Duplicate rồi bắt đầu import.
4. Hệ thống duyệt các hàng, kiểm tra first field, resolve deck/NoteType; ưu tiên GUID nếu có, nếu không đối chiếu first field và NoteType theo scope.
5. Hệ thống thêm note mới hoặc cập nhật note hợp lệ; sinh card còn thiếu và giữ card cũ.
6. Hệ thống trả log kết quả theo nhóm; người dùng kiểm tra các hàng không nhập/cập nhật và sửa file nếu cần.

## Extensions gắn bước

| Điểm rẽ | Điều kiện | Xử lý / điểm quay lại |
|---|---|---|
| 1a | File không plain text UTF-8 | Chuẩn bị lại file theo định dạng hỗ trợ; không coi xls/doc là text import trực tiếp. |
| 2a | Deck name chưa tồn tại | Backend có thể tạo deck theo tên; deck ID không resolve được được xử lý khác, không tự đổi thành một deck tùy ý. |
| 4a | First field rỗng | ERR-ANKI-000-05: ghi empty_first_field và tiếp tục hàng sau. |
| 4b | Thiếu deck/NoteType | ERR-ANKI-000-06: ghi missing_deck hoặc missing_notetype; người dùng sửa mapping/ID/tên. |
| 4c | GUID trùng nhưng NoteType không khớp | ERR-ANKI-000-07: ghi conflicting, không cập nhật note sai cấu trúc. |
| 5a | Duplicate và GUID đã tồn tại | Không tạo bản sao; ghi duplicate. Muốn round-trip chỉnh field đầu nên giữ GUID xuất từ Anki. |
| 5b | Không GUID và thay khóa first field | Có thể thêm note mới thay vì update; kiểm tra match scope trước khi nhập lại. |
| 6a | Text có media references | File media phải có ở collection.media; text không tự mang byte ảnh/âm thanh theo. |

## Business Rules và lỗi liên quan

| Mã | Ràng buộc đã quan sát |
|---|---|
| BR-ANKI-001 | Số field values bằng số field NoteType; nội dung/tags ở note, lịch ở card. Ngoại lệ: Không suy ra note thuộc đúng một deck |
| BR-ANKI-020 | Có GUID ưu tiên GUID; không GUID dùng first field và NoteType, có thể giới hạn deck; chọn update/preserve/duplicate. Ngoại lệ: GUID có sẵn không tạo duplicate; NoteType xung đột ghi conflicting; first field rỗng/missing deck/type ghi lỗi hàng |

| Mã lỗi BA | Trigger | Kết quả theo source |
|---|---|---|
| ERR-ANKI-000-05 | Text row có first field rỗng | Đưa vào log.empty_first_field và tiếp tục các hàng khác |
| ERR-ANKI-000-06 | Text row không giải được deck hoặc NoteType | Ghi missing_deck hoặc missing_notetype trong kết quả hàng |
| ERR-ANKI-000-07 | Note import đối chiếu GUID nhưng NoteType không tương thích | Ghi conflicting, không cập nhật note như một match hợp lệ |

## Nguồn và kiểm chứng

- [rslib/src/import_export/text/import.rs:250](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L250)
- [rslib/src/import_export/text/import.rs:318](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L318)
- [docs-site/manual/importing/text-files.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/importing/text-files.mdx#L5)
- [rslib/src/import_export/text/import.rs:354](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L354)
- [docs-site/manual/importing/text-files.mdx:127](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/importing/text-files.mdx#L127)

## Giới hạn / câu hỏi mở

Phân tích Code/Docs theo snapshot; không có biên bản phê duyệt nghiệp vụ hoặc kết quả chạy kiểm thử. Thông báo UI/localization không được khẳng định bằng mã ERR phân tích. Owner xác nhận trước khi nghiệm thu runtime: maintainer phụ trách luồng và người dùng thử tác vụ.

---
id: DOC-UC-ANKI-002
title: "UC-ANKI-002: Tạo câu hỏi Cloze và Image Occlusion"
version: "1.0.0"
phase: Specification
domain: UseCases
tags: [anki, as-is, cockburn, draft]
depends_on: [FR-CNT-CLOZ-001, FR-CNT-IMGO-001]
related_diagrams: [DIAG-CTX-ANKI-001]
author: BA Agent
last_updated: "2026-11-02"
status: draft
---

# UC-ANKI-002 — Tạo câu hỏi Cloze và Image Occlusion

**As-Is — DRAFT v1.0.0.** Nguồn cố định commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`; chưa thực thi runtime. FR/BR/ERR tham chiếu catalog [requirements.json](../srs/requirements.json) v1.0.0, không phải mã lỗi native hay HTTP do Anki công bố.

## Lịch sử sửa đổi

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---|---|---|---|
| 1.0.0 | 2026-11-02 | BA Agent | Baseline As-Is, luồng chính/extension và truy vết source |

## Hợp đồng use case

| Thuộc tính | Giá trị |
|---|---|
| Primary Actor | Người soạn nội dung |
| Scope | Anki Desktop, collection/profile cục bộ; server chỉ trong luồng sync được nêu |
| Level | Sea level |
| Stakeholders & interests | Người học muốn kiểm tra từng vùng thông tin; người soạn muốn kiểm soát các vùng che trên một card. |
| Supporting actors | Không cần actor người hỗ trợ; backend/scheduler là thành phần nội bộ, không role RBAC |
| Trigger | Chọn NoteType Cloze hoặc Image Occlusion để che thông tin cần kiểm tra. |
| Pre-conditions | Collection mở; có NoteType tương ứng; nhánh IO có ảnh local/clipboard có thể nạp. |
| Success guarantees | Note chứa các vùng che được lưu; card sinh theo cloze number hoặc shape/group; có thể bắt đầu review. |
| Minimal guarantees | Không tự coi xóa vùng che là xóa card có lịch sử; preview chưa lưu không được coi là dữ liệu đã commit. |
| Functional scope | FR-CNT-CLOZ-001, FR-CNT-IMGO-001 |

## Main Success Scenario

1. Người dùng chọn Cloze; hệ thống mở các field tương ứng.
2. Người dùng chọn đoạn văn để che và tạo c1/c2; có thể gán nhiều đoạn cùng một số để hỏi trong một card.
3. Người dùng xem lại nội dung che, thêm Extra hoặc tags rồi nhấn Add.
4. Hệ thống kiểm tra cấu trúc Note, trích số cloze và sinh ordinal còn thiếu với template Cloze.
5. Người dùng xem các card đã tạo và chỉnh nội dung nếu cần.

## Extensions gắn bước

| Điểm rẽ | Điều kiện | Xử lý / điểm quay lại |
|---|---|---|
| 1a | Chọn Image Occlusion | Nạp ảnh từ file/clipboard; vẽ rectangle/ellipse/polygon và nhóm shapes; chọn Hide All Guess One hoặc Hide One Guess One. Đi tiếp bước 3 với header/back extra/comments. |
| 2a | Các đoạn dùng cùng cloze number | Hệ thống che các đoạn cùng số trên một card; không sinh một card cho mỗi đoạn text. |
| 3a | IO có text overlay | Overlay text không sinh card; mỗi shape hoặc group sinh card. Comments mặc định không hiển thị trên card. |
| 4a | Note bị sai số field | ERR-ANKI-000-01: từ chối cấu trúc không khớp; chỉnh NoteType/values trước khi thử lại. |
| 5a | Xóa cloze hoặc shape đã có card | Card cũ không tự xóa; chạy Empty Cards và xác nhận card cần loại. Group hai shape tạo một card cho nhóm. |

## Business Rules và lỗi liên quan

| Mã | Ràng buộc đã quan sát |
|---|---|
| BR-ANKI-001 | Số field values bằng số field NoteType; nội dung/tags ở note, lịch ở card. Ngoại lệ: Không suy ra note thuộc đúng một deck |
| BR-ANKI-004 | Các số cloze khác nhau sinh card khác nhau; cùng số dùng cùng card, template đầu tiên. Ngoại lệ: Không coi mỗi vùng văn bản là một note |
| BR-ANKI-003 | Chỉ thêm ordinal chưa có với mặt hỏi render được; template có thể override deck. Ngoại lệ: ensure_not_empty có fallback ordinal 0; card trở thành rỗng không tự bị xóa ngay |
| BR-ANKI-005 | Shape hoặc nhóm có thể tạo card cloze; text overlay không tạo card. Ngoại lệ: Xóa shape không tự xóa card cũ; dùng Empty Cards |

| Mã lỗi BA | Trigger | Kết quả theo source |
|---|---|---|
| ERR-ANKI-000-01 | Note có số field values khác NoteType | Từ chối lưu qua guard; UI/localization chưa truy vết |

## Nguồn và kiểm chứng

- [rslib/src/notetype/cardgen.rs:160](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L160)
- [docs-site/manual/editing.mdx:364](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L364)
- [rslib/src/image_occlusion/notetype.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/image_occlusion/notetype.rs#L59)
- [docs-site/manual/editing.mdx:504](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L504)
- [docs-site/manual/editing.mdx:477](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L477)
- [docs-site/manual/editing.mdx:531](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L531)

## Giới hạn / câu hỏi mở

Phân tích Code/Docs theo snapshot; không có biên bản phê duyệt nghiệp vụ hoặc kết quả chạy kiểm thử. Thông báo UI/localization không được khẳng định bằng mã ERR phân tích. Owner xác nhận trước khi nghiệm thu runtime: maintainer phụ trách luồng và người dùng thử tác vụ.

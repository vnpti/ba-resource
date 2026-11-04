---
id: DOC-UC-ANKI-001
title: "UC-ANKI-001: Soạn và sửa nội dung có cấu trúc"
version: "1.0.0"
phase: Specification
domain: UseCases
tags: [anki, as-is, cockburn, draft]
depends_on: [FR-CNT-NOTE-001, FR-CNT-TYPE-001]
related_diagrams: [DIAG-CTX-ANKI-001]
author: BA Agent
last_updated: "2026-11-02"
status: draft
---

# UC-ANKI-001 — Soạn và sửa nội dung có cấu trúc

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
| Stakeholders & interests | Người soạn cần nội dung nhất quán giữa siblings; người học cần giữ lịch ôn card đã học. |
| Supporting actors | Không cần actor người hỗ trợ; backend/scheduler là thành phần nội bộ, không role RBAC |
| Trigger | Mở Add/Browse hoặc Manage Note Types để tạo/sửa nội dung. |
| Pre-conditions | Profile và collection đã mở; có NoteType hoặc người dùng tạo NoteType trong nhánh 1a; có deck đích cho card mới. |
| Success guarantees | Note/NoteType hợp lệ được lưu; card còn thiếu được sinh theo template; lịch card đã tồn tại được giữ khi chỉ sửa nội dung. |
| Minimal guarantees | Guard từ chối cấu trúc không hợp lệ; không coi thay đổi chưa được lưu là đã có trong collection. Không bảo đảm mọi sửa schema đều merge sync được. |
| Functional scope | FR-CNT-NOTE-001, FR-CNT-TYPE-001 |

## Main Success Scenario

1. Người dùng chọn NoteType và deck đích độc lập trong Add, hoặc chọn note đang có trong Browse.
2. Hệ thống trình bày các field của NoteType; người dùng nhập/sửa giá trị và tags, thêm media nếu cần.
3. Người dùng yêu cầu lưu; hệ thống kiểm tra số field khớp NoteType, chuẩn hóa field/tags và nhận diện các card cần sinh.
4. Hệ thống lưu Note và sinh ordinal còn thiếu theo template; card cũ tiếp tục dùng lịch riêng.
5. Người dùng xem lại các card liên quan hoặc tiếp tục soạn nội dung; note có thể có siblings ở nhiều deck.

## Extensions gắn bước

| Điểm rẽ | Điều kiện | Xử lý / điểm quay lại |
|---|---|---|
| 1a | Chưa có cấu trúc phù hợp | Mở Manage Note Types, thêm/chỉnh field và template; mỗi kiểu phải còn ít nhất một field, một template và tên không rỗng. Vi phạm → ERR-ANKI-000-02; sửa cấu trúc rồi quay lại bước 1. |
| 2a | First field trùng note cùng kiểu | UI cảnh báo duplicate; đây không phải UNIQUE constraint ngăn mọi đường lưu. Người dùng kiểm tra note hiện có trước khi quyết định. |
| 3a | Số field không khớp | ERR-ANKI-000-01: backend từ chối qua guard; sửa mapping/NoteType và gửi lại. Chưa chốt wording/key UI. |
| 4a | Mặt hỏi trở nên rỗng | Không tự xóa card cũ; dùng Empty Cards để xem và quyết định xóa. Generator có fallback card 0 khi ensure_not_empty được bật. |
| 1b | Thay đổi schema NoteType | Có thể cần full sync thay vì merge thông thường; tiếp tục UC-ANKI-009 khi đồng bộ. |

## Business Rules và lỗi liên quan

| Mã | Ràng buộc đã quan sát |
|---|---|
| BR-ANKI-001 | Số field values bằng số field NoteType; nội dung/tags ở note, lịch ở card. Ngoại lệ: Không suy ra note thuộc đúng một deck |
| BR-ANKI-003 | Chỉ thêm ordinal chưa có với mặt hỏi render được; template có thể override deck. Ngoại lệ: ensure_not_empty có fallback ordinal 0; card trở thành rỗng không tự bị xóa ngay |
| BR-ANKI-002 | Có ít nhất một field, một template và tên không rỗng. Ngoại lệ: Các bước chuẩn hóa tên được áp dụng trước/sau guard tương ứng; không suy ra UI trả nguyên thông báo kỹ thuật |

| Mã lỗi BA | Trigger | Kết quả theo source |
|---|---|---|
| ERR-ANKI-000-01 | Note có số field values khác NoteType | Từ chối lưu qua guard; UI/localization chưa truy vết |
| ERR-ANKI-000-02 | NoteType thiếu field/template hoặc tên rỗng | Từ chối ở guard tương ứng; không giả định HTTP |

## Nguồn và kiểm chứng

- [rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194)
- [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95)
- [rslib/src/notetype/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/mod.rs#L484)
- [proto/anki/notetypes.proto:102](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/notetypes.proto#L102)
- [docs-site/manual/editing.mdx:47](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L47)
- [docs-site/manual/templates/generation.mdx:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/templates/generation.mdx#L25)
- [docs-site/manual/syncing.mdx:85](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/syncing.mdx#L85)

## Giới hạn / câu hỏi mở

Phân tích Code/Docs theo snapshot; không có biên bản phê duyệt nghiệp vụ hoặc kết quả chạy kiểm thử. Thông báo UI/localization không được khẳng định bằng mã ERR phân tích. Owner xác nhận trước khi nghiệm thu runtime: maintainer phụ trách luồng và người dùng thử tác vụ.

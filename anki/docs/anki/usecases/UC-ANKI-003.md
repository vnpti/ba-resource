---
id: DOC-UC-ANKI-003
title: "UC-ANKI-003: Tổ chức và tìm nội dung để thao tác"
version: "1.0.0"
phase: Specification
domain: UseCases
tags: [anki, as-is, cockburn, draft]
depends_on: [FR-ORG-DECK-001, FR-ORG-SRCH-001]
related_diagrams: [DIAG-CTX-ANKI-001]
author: BA Agent
last_updated: "2026-11-02"
status: draft
---

# UC-ANKI-003 — Tổ chức và tìm nội dung để thao tác

**As-Is — DRAFT v1.0.0.** Nguồn cố định commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`; chưa thực thi runtime. FR/BR/ERR tham chiếu catalog [requirements.json](../srs/requirements.json) v1.0.0, không phải mã lỗi native hay HTTP do Anki công bố.

## Lịch sử sửa đổi

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---|---|---|---|
| 1.0.0 | 2026-11-02 | BA Agent | Baseline As-Is, luồng chính/extension và truy vết source |

## Hợp đồng use case

| Thuộc tính | Giá trị |
|---|---|
| Primary Actor | Người học quản lý nội dung |
| Scope | Anki Desktop, collection/profile cục bộ; server chỉ trong luồng sync được nêu |
| Level | Sea level |
| Stakeholders & interests | Người học cần phạm vi tìm/học xác định; người soạn muốn tránh gán tags nhầm cho toàn nhóm siblings. |
| Supporting actors | Không cần actor người hỗ trợ; backend/scheduler là thành phần nội bộ, không role RBAC |
| Trigger | Tạo/đổi deck hoặc tìm tập card trong Browse. |
| Pre-conditions | Profile mở; có card hoặc người dùng tạo deck chuẩn bị nhập card. |
| Success guarantees | Cây deck/tập kết quả search phản ánh lựa chọn; thao tác chuyển deck chỉ tác động card đã chọn. |
| Minimal guarantees | Kết quả rỗng không có nghĩa nội dung bị xóa; truy vấn tìm kiếm không mặc nhiên thay đổi note/card. |
| Functional scope | FR-ORG-DECK-001, FR-ORG-SRCH-001 |

## Main Success Scenario

1. Người dùng tạo/đổi tên deck, dùng phân cấp :: hoặc di chuyển deck trong cây.
2. Người dùng mở Browse và nhập điều kiện field, tag, deck hoặc state bằng cú pháp search.
3. Hệ thống đánh giá truy vấn và hiển thị note/card phù hợp theo chế độ duyệt.
4. Người dùng kiểm tra tập được chọn, rồi chọn chuyển card sang deck, thêm tags hoặc đặt flag.
5. Hệ thống áp thao tác theo đúng cấp: deck/flag ở card, tags ở note và các siblings cùng note.
6. Người dùng chọn deck để học; phạm vi học gồm descendants và bị giới hạn bởi chính sách học.

## Extensions gắn bước

| Điểm rẽ | Điều kiện | Xử lý / điểm quay lại |
|---|---|---|
| 2a | Tìm từ trần thay vì tag: | Search văn bản không mặc nhiên tìm tags; dùng cú pháp tag để thu hẹp đúng trường. |
| 3a | Không có kết quả | Hiển thị tập rỗng; sửa điều kiện tại bước 2; không suy ra mất dữ liệu. |
| 4a | Card siblings ở nhiều deck | Chuyển card chọn không có nghĩa Note thuộc deck mới; những card cùng note khác vẫn có deck riêng. |
| 5a | Chỉ muốn đánh dấu một sibling | Dùng flag, không tag; mỗi card có một flag tại một thời điểm. |
| 6a | Chỉ cần tập học tạm | Chuyển UC-ANKI-006 để tạo filtered deck thay vì hiểu như bản sao collection. |

## Business Rules và lỗi liên quan

| Mã | Ràng buộc đã quan sát |
|---|---|
| BR-ANKI-006 | Lấy card deck được chọn và descendants; card có một deck hiện tại. Ngoại lệ: Siblings có thể nằm khác deck; filtered giữ home deck riêng |
| BR-ANKI-012 | Ưu tiên mức today rồi deck rồi preset, trừ số đã học; mặc định new cũng tiêu thụ review limit. Ngoại lệ: New cards ignore review limit tách new; parent limits áp dụng theo cờ; intraday learning không bị review limit chặn như interday |
| BR-ANKI-007 | Tìm trong field note và trả card tương ứng; hỗ trợ AND/OR/NOT, lọc tag/deck bằng cú pháp. Ngoại lệ: Tìm văn bản đơn không tự tìm tags |

Catalog chưa gán ERR riêng cho phạm vi này; không tự tạo mã lỗi hoặc status HTTP. Các nhánh thường (kết quả rỗng, hủy, đổi mode) không tự được coi là lỗi.

## Nguồn và kiểm chứng

- [docs-site/manual/getting-started.mdx:75](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/getting-started.mdx#L75)
- [rslib/src/scheduler/queue/builder/mod.rs:135](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/mod.rs#L135)
- [docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5)
- [docs-site/manual/editing.mdx:217](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L217)

## Giới hạn / câu hỏi mở

Phân tích Code/Docs theo snapshot; không có biên bản phê duyệt nghiệp vụ hoặc kết quả chạy kiểm thử. Thông báo UI/localization không được khẳng định bằng mã ERR phân tích. Owner xác nhận trước khi nghiệm thu runtime: maintainer phụ trách luồng và người dùng thử tác vụ.

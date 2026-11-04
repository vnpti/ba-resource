---
id: DOC-UC-ANKI-005
title: "UC-ANKI-005: Điều chỉnh tải học và FSRS"
version: "1.0.1"
phase: Specification
domain: UseCases
tags: [anki, as-is, cockburn, draft]
depends_on: [FR-LRN-LIM-001, FR-LRN-FSRS-001]
related_diagrams: [DIAG-CTX-ANKI-001, DIAG-STATE-ANKI-001, DIAG-STATE-ANKI-002]
author: BA Agent
last_updated: "2026-11-03"
status: draft
---

# UC-ANKI-005 — Điều chỉnh tải học và FSRS

**As-Is — DRAFT v1.0.1.** Nguồn cố định commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`; chưa thực thi runtime. FR/BR/ERR tham chiếu catalog [requirements.json](../srs/requirements.json) v1.0.1, không phải mã lỗi native hay HTTP do Anki công bố.

## Lịch sử sửa đổi

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---|---|---|---|
| 1.0.1 | 2026-11-03 | BA Analysis | Làm rõ oracle035/067/072/077 và truy vết liên quan; không thay source hoặc kết quả chạy |
| 1.0.0 | 2026-11-02 | BA Agent | Baseline As-Is, luồng chính/extension và truy vết source |

## Hợp đồng use case

| Thuộc tính | Giá trị |
|---|---|
| Primary Actor | Người học quản lý chính sách học |
| Scope | Anki Desktop, collection/profile cục bộ; server chỉ trong luồng sync được nêu |
| Level | Sea level |
| Stakeholders & interests | Người học muốn kiểm soát công sức; các deck dùng chung preset cần cấu hình nhất quán. |
| Supporting actors | Không cần actor người hỗ trợ; backend/scheduler là thành phần nội bộ, không role RBAC |
| Trigger | Mở Deck Options để đổi hạn mức, preset hoặc FSRS. |
| Pre-conditions | Collection/deck mở; người dùng xác định deck/preset và phạm vi thay đổi; Optimize được phép với history rỗng; không cần giả định số lượt tối thiểu. |
| Success guarantees | Cấu hình được lưu theo phạm vi; queue lần sau dùng hạn mức mới; reschedule chỉ thực hiện khi được chọn theo luồng cấu hình. |
| Minimal guarantees | Không tuyên bố đổi retention luôn đổi tất cả due date hoặc bảo đảm đạt tỷ lệ nhớ; tham số không được chấp nhận không được coi là đã áp dụng. |
| Functional scope | FR-LRN-LIM-001, FR-LRN-FSRS-001 |

## Main Success Scenario

1. Người dùng chọn deck và mở Deck Options; hệ thống trình bày preset cùng override deck/today.
2. Người dùng đặt giới hạn new/review và các cờ liên quan; hệ thống xác định thứ tự ưu tiên today, deck, preset.
3. Người dùng chọn bật/tắt FSRS toàn collection, desired retention và tham số theo preset; có thể yêu cầu optimize từ history.
4. Người dùng xác định có reschedule cards on change hay không và xem phạm vi preset dùng chung.
5. Người dùng lưu; backend áp cập nhật cấu hình và các công việc reschedule được yêu cầu trong luồng update.
6. Khi học tiếp, backend tính queue/next state từ cấu hình vừa lưu và mức đã học trong ngày.

## Extensions gắn bước

| Điểm rẽ | Điều kiện | Xử lý / điểm quay lại |
|---|---|---|
| 1a | Preset được nhiều deck dùng | Người dùng phải hiểu thay preset ảnh hưởng các deck cùng preset; không coi là cấu hình riêng một deck. |
| 2a | Đã đạt review limit | Intraday learning vẫn có thể tiếp tục; interday/review/new xử lý theo giới hạn và các cờ, không dừng mọi hoạt động. |
| 3a | Không bật FSRS | Scheduler dùng nhánh legacy; không áp công thức ease SM-2 để giải thích FSRS. |
| 3b | 0 training item sau lọc | ComputeFsrsParams trả nguyên params, count0 và health absent; Optimize current preset báo không có reviews, không gán params mới. Không áp nhánh này cho Optimize All. |
| 4a | Không chọn reschedule | Không khẳng định mọi due date cũ được tính lại ngay; các lần trả lời sau dùng cấu hình hiện hành. |
| 6a | Retention đích cao | Đây là mục tiêu mô hình và có thể tăng tải ôn, không cam kết điểm thi hoặc trí nhớ thực tế. |

## Business Rules và lỗi liên quan

| Mã | Ràng buộc đã quan sát |
|---|---|
| BR-ANKI-006 | Lấy card deck được chọn và descendants; card có một deck hiện tại. Ngoại lệ: Siblings có thể nằm khác deck; filtered giữ home deck riêng |
| BR-ANKI-012 | Ưu tiên mức today rồi deck rồi preset, trừ số đã học; mặc định new cũng tiêu thụ review limit. Ngoại lệ: New cards ignore review limit tách new; parent limits áp dụng theo cờ; intraday learning không bị review limit chặn như interday |
| BR-ANKI-013 | FSRS dùng memory state, retention, elapsed days, tham số; legacy dùng interval/ease/multiplier. Ngoại lệ: Không sử dụng công thức ease SM-2 giải thích interval FSRS |
| BR-ANKI-014 | FSRS bật toàn cục; optimize từ lịch sử; reschedule on change quyết định cập nhật due cũ. Optimize current preset có 0 training item trả nguyên current_params, fsrs_items=0, health_check_passed absent; UI báo deck-config-fsrs-params-no-reviews và không gán params mới. Giới hạn: Không đồng nhất raw revlog count với training items; không áp nhánh này cho Optimize All hoặc assignment chưa lưu. Retention là mục tiêu, không bảo đảm kết quả; runtime chưa chạy |

Catalog chưa gán ERR riêng cho phạm vi này; không tự tạo mã lỗi hoặc status HTTP. Các nhánh thường (kết quả rỗng, hủy, đổi mode) không tự được coi là lỗi.

## Nguồn và kiểm chứng

- [rslib/src/decks/limits.rs:98](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/decks/limits.rs#L98)
- [rslib/src/scheduler/queue/builder/gathering.rs:23](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/gathering.rs#L23)
- [rslib/src/scheduler/answering/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L484)
- [docs-site/manual/deck-options.mdx:406](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L406)
- [docs-site/manual/deck-options.mdx:500](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L500)
- [rslib/src/deckconfig/update.rs:160](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/deckconfig/update.rs#L160)

Bổ sung đối chiếu 2026-11-03: [docs-site/manual/deck-options.mdx:406](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L406); [ts/routes/deck-options/FsrsOptions.svelte:200](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L200); [ts/routes/deck-options/FsrsOptions.svelte:225](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L225); [ts/routes/deck-options/FsrsOptions.svelte:235](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L235); [rslib/src/scheduler/service/mod.rs:264](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/service/mod.rs#L264); [rslib/src/scheduler/fsrs/params.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L95); [proto/anki/scheduler.proto:357](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L357); [ftl/core/deck-config.ftl:495](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ftl/core/deck-config.ftl#L495).

## Giới hạn / câu hỏi mở

Phân tích Code/Docs theo snapshot; không có biên bản phê duyệt nghiệp vụ hoặc kết quả chạy kiểm thử. Thông báo UI/localization không được khẳng định bằng mã ERR phân tích. Owner xác nhận trước khi nghiệm thu runtime: maintainer phụ trách luồng và người dùng thử tác vụ.

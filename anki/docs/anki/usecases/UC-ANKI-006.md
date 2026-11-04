---
id: DOC-UC-ANKI-006
title: "UC-ANKI-006: Điều chỉnh tập thẻ và ôn theo mục tiêu"
version: "1.0.0"
phase: Specification
domain: UseCases
tags: [anki, as-is, cockburn, draft]
depends_on: [FR-LRN-HIDE-001, FR-LRN-FILT-001]
related_diagrams: [DIAG-CTX-ANKI-001, DIAG-STATE-ANKI-001, DIAG-STATE-ANKI-002]
author: BA Agent
last_updated: "2026-11-02"
status: draft
---

# UC-ANKI-006 — Điều chỉnh tập thẻ và ôn theo mục tiêu

**As-Is — DRAFT v1.0.0.** Nguồn cố định commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`; chưa thực thi runtime. FR/BR/ERR tham chiếu catalog [requirements.json](../srs/requirements.json) v1.0.0, không phải mã lỗi native hay HTTP do Anki công bố.

## Lịch sử sửa đổi

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---|---|---|---|
| 1.0.0 | 2026-11-02 | BA Agent | Baseline As-Is, luồng chính/extension và truy vết source |

## Hợp đồng use case

| Thuộc tính | Giá trị |
|---|---|
| Primary Actor | Người học |
| Scope | Anki Desktop, collection/profile cục bộ; server chỉ trong luồng sync được nêu |
| Level | Sea level |
| Stakeholders & interests | Người học cần tập ôn đúng mục tiêu; lịch home card cần tránh bị thay ngoài mode đã chọn. |
| Supporting actors | Không cần actor người hỗ trợ; backend/scheduler là thành phần nội bộ, không role RBAC |
| Trigger | Muốn tạm bỏ card hoặc tạo một phiên ôn có mục tiêu bằng filtered deck. |
| Pre-conditions | Collection có card; người dùng biết tập thẻ/điều kiện cần học và lựa chọn reschedule hay preview. |
| Success guarantees | Card phù hợp được học trong filtered rồi trả home theo mode; các thao tác hide giữ trạng thái trí nhớ nền và lịch sử. |
| Minimal guarantees | Empty filtered không xóa note/card; không bury card suspended để tránh vô tình unsuspend; filtered không sao chép card. |
| Functional scope | FR-LRN-HIDE-001, FR-LRN-FILT-001 |

## Main Success Scenario

1. Người dùng tìm tập card muốn tập trung; có thể bury/suspend các card cần loại trước khi xây tập.
2. Người dùng tạo filtered deck, nhập search/order/limit và chọn reschedule hoặc preview.
3. Hệ thống loại card suspended/buried/đã ở filtered khác, chuyển card hợp lệ vào filtered và giữ home deck.
4. Người học trả lời card; reschedule dùng home settings, preview dùng delay tương ứng rating.
5. Hệ thống trả card về home khi nhánh học kết thúc; người dùng Empty để trả tất cả hoặc Rebuild để tìm lại.

## Extensions gắn bước

| Điểm rẽ | Điều kiện | Xử lý / điểm quay lại |
|---|---|---|
| 1a | Bury thủ công/tự động | Queue -3/-2 giữ tới unbury hoặc đổi ngày scheduler; suspend -1 giữ tới unsuspend, không tự hết vào ngày sau. |
| 1b | Leech được phát hiện | Tag leech ở note; chỉ suspend card nếu cấu hình hành động yêu cầu. Không phải mỗi Again đều là leech. |
| 3a | Không có card và allow_empty=false | ERR-ANKI-000-04: SearchReturnedNoCards; sửa search/loại bỏ điều kiện exclude rồi rebuild, không coi Browser count là số chắc chắn vào filtered. |
| 4a | Reschedule bật | Kết quả Review trả card home; Learning/Relearning còn ở filtered cho tới hoàn tất. |
| 4b | Preview tắt rescheduling | Again/Hard/Good lặp theo delay; Easy hoặc bất kỳ delay=0 kết thúc; vẫn ghi revlog. |
| 5a | Rebuild | Trả card hiện tại home trước rồi chạy query lại; không chồng các bản sao card. |

## Business Rules và lỗi liên quan

| Mã | Ràng buộc đã quan sát |
|---|---|
| BR-ANKI-015 | Bury được phục hồi khi rollover ngày hoặc unbury; suspend tới khi unsuspend; không bury card suspended. Ngoại lệ: Có tùy chọn bury interday learning; manual studying diễn đạt cũ không đủ phân biệt intraday/interday |
| BR-ANKI-016 | Đánh dấu tại threshold rồi mỗi ceil(threshold/2); tag leech ở note; suspend nếu cấu hình yêu cầu. Ngoại lệ: Threshold 0 không kích hoạt; leech action có thể chỉ tag |
| BR-ANKI-017 | Search/order/limit lấy card, loại suspended/buried/đang filtered; rebuild trả thẻ cũ về rồi tìm lại. Ngoại lệ: Zero result không được phép rỗng trả lỗi; đây là card tạm di chuyển, không copy |
| BR-ANKI-018 | Dùng home deck settings; chuyển Review thì trả home, learning/relearning còn trong filtered. Ngoại lệ: Review trước hạn có thuật toán riêng; không hứa lùi thêm nguyên interval |
| BR-ANKI-019 | Again/Hard/Good dùng delay; Easy hoặc bất kỳ delay=0 kết thúc, phục hồi home/queue. Ngoại lệ: Vẫn có revlog; last_review_time không cập nhật như normal study |

| Mã lỗi BA | Trigger | Kết quả theo source |
|---|---|---|
| ERR-ANKI-000-04 | Build filtered không tìm thấy card và allow_empty=false | SearchReturnedNoCards, không chấp nhận kết quả thao tác |

## Nguồn và kiểm chứng

- [rslib/src/scheduler/bury_and_suspend.rs:32](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L32)
- [rslib/src/scheduler/answering/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L194)
- [rslib/src/scheduler/filtered/mod.rs:123](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L123)
- [rslib/src/scheduler/states/preview_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/preview_filter.rs#L25)
- [rslib/src/scheduler/bury_and_suspend.rs:96](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L96)

## Giới hạn / câu hỏi mở

Phân tích Code/Docs theo snapshot; không có biên bản phê duyệt nghiệp vụ hoặc kết quả chạy kiểm thử. Thông báo UI/localization không được khẳng định bằng mã ERR phân tích. Owner xác nhận trước khi nghiệm thu runtime: maintainer phụ trách luồng và người dùng thử tác vụ.

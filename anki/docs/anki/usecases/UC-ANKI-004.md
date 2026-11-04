---
id: DOC-UC-ANKI-004
title: "UC-ANKI-004: Học, tự chấm và theo dõi phiên ôn"
version: "1.0.1"
phase: Specification
domain: UseCases
tags: [anki, as-is, cockburn, draft]
depends_on: [FR-LRN-REV-001, FR-LRN-SCH-001, FR-RPT-STAT-001]
related_diagrams: [DIAG-CTX-ANKI-001, DIAG-STATE-ANKI-001, DIAG-STATE-ANKI-002]
author: BA Agent
last_updated: "2026-11-03"
status: draft
---

# UC-ANKI-004 — Học, tự chấm và theo dõi phiên ôn

**As-Is — DRAFT v1.0.1.** Nguồn cố định commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`; chưa thực thi runtime. FR/BR/ERR tham chiếu catalog [requirements.json](../srs/requirements.json) v1.0.1, không phải mã lỗi native hay HTTP do Anki công bố.

## Lịch sử sửa đổi

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---|---|---|---|
| 1.0.1 | 2026-11-03 | BA Analysis | Làm rõ true retention không dedup card/ngày; runtime Not Run |
| 1.0.0 | 2026-11-02 | BA Agent | Baseline As-Is; làm rõ Good hết steps vẫn có thể short-term trong review trước phát hành |

## Hợp đồng use case

| Thuộc tính | Giá trị |
|---|---|
| Primary Actor | Người học |
| Scope | Anki Desktop, collection/profile cục bộ; server chỉ trong luồng sync được nêu |
| Level | Sea level |
| Stakeholders & interests | Người học cần lịch và lịch sử đúng; người xem thống kê cần hiểu đơn vị lượt/card và phạm vi của retention. |
| Supporting actors | Không cần actor người hỗ trợ; backend/scheduler là thành phần nội bộ, không role RBAC |
| Trigger | Chọn deck rồi Study Now. |
| Pre-conditions | Collection mở; scheduler có thể xây queue; có card phù hợp hoặc hệ thống trả trạng thái hết phiên. |
| Success guarantees | Các câu trả lời được chấp nhận có card/revlog/counters nhất quán; hạn ôn tiếp theo theo scheduler; thống kê theo định nghĩa từng chỉ số. |
| Minimal guarantees | Câu trả lời current state không khớp bị từ chối; “hết phiên” không đồng nghĩa không còn backlog hoặc đã nhớ tất cả nội dung. |
| Functional scope | FR-LRN-REV-001, FR-LRN-SCH-001, FR-RPT-STAT-001 |

## Main Success Scenario

1. Người học chọn deck; hệ thống gom card theo due, giới hạn và bury settings.
2. Hệ thống hiển thị câu hỏi; người học tự nhớ rồi chọn Show Answer.
3. Hệ thống hiển thị đáp án và các mức Again/Hard/Good/Easy; người học tự chấm.
4. Backend kiểm tra current state, tính/áp kết quả được chọn và trong transaction lưu card, revlog, counters cùng xử lý siblings.
5. Hệ thống tiếp tục card kế tiếp hoặc hiển thị kết thúc phiên/thẻ đang chờ.
6. Người học mở Statistics và chọn phạm vi để xem lượt học, lịch sắp tới và chỉ số nhớ.

## Extensions gắn bước

| Điểm rẽ | Điều kiện | Xử lý / điểm quay lại |
|---|---|---|
| 1a | Không có card có thể phục vụ | Đi thẳng bước 5; vẫn có thể tồn tại backlog, learning chờ hoặc card buried/suspended. |
| 3a | Không nhớ đáp án | Chọn Again; Hard biểu thị nhớ được nhưng khó, không thay Again. |
| 4a | State đã thay đổi từ lúc hiển thị | ERR-ANKI-000-03: từ chối current state cũ sau xử lý elapsed seconds; tải lại trạng thái trước khi trả lời tiếp. |
| 4b | Review Again và có relearning steps | Tăng lapse rồi vào học lại; Again tiếp trong cùng relearning không cộng lapse review gốc lần nữa. |
| 4c | Steps rỗng hoặc FSRS short-term | Dùng nhánh scheduler tính ra; Good không còn delay từ steps vẫn giữ Learning/Relearning nếu FSRS cho phép short-term, điều kiện steps tương ứng thỏa và good.interval < 0.5 ngày. Easy có nhánh trả Review riêng. Xem guard chính xác tại [states.md](../srs/states.md). Leech có thể tag/suspend theo cấu hình. |
| 6a | Đọc số lượt như số card duy nhất | Today đếm lượt trả lời; loại Manual/Rescheduled theo code. True retention dùng predicate riêng và đếm từng log đủ điều kiện, không dedup card/ngày; manual first/day khác code. Xem AC/TC-ANKI-067. |

## Business Rules và lỗi liên quan

| Mã | Ràng buộc đã quan sát |
|---|---|
| BR-ANKI-006 | Lấy card deck được chọn và descendants; card có một deck hiện tại. Ngoại lệ: Siblings có thể nằm khác deck; filtered giữ home deck riêng |
| BR-ANKI-008 | Again là không nhớ/sai; Hard, Good, Easy là nhớ với mức nỗ lực khác nhau. Ngoại lệ: Hard không thay Again khi quên; không đo được hiểu biết ngoài tín hiệu tự chấm |
| BR-ANKI-011 | So current state sau hiệu chỉnh elapsed seconds; trong transaction áp dụng state, revlog, stats, bury và lưu card. Ngoại lệ: State khác bị từ chối; cap thời gian theo preset; không tuyên bố xử lý mọi xung đột client |
| BR-ANKI-009 | Again về bước đầu; Good tiến; Hard lặp bước với công thức riêng ở bước đầu; Easy sang Review. Ngoại lệ: Steps rỗng hoặc FSRS short-term có nhánh khác; không ép mọi card đi qua số bước cố định |
| BR-ANKI-010 | Tăng lapse, tính lịch mới và vào Relearning nếu có steps; trả lời đúng tiếp tục Review. Ngoại lệ: Again trong Relearning không tự tăng lapse lần nữa; không steps có thể về thẳng Review |
| BR-ANKI-013 | FSRS dùng memory state, retention, elapsed days, tham số; legacy dùng interval/ease/multiplier. Ngoại lệ: Không sử dụng công thức ease SM-2 giải thích interval FSRS |
| BR-ANKI-025 | Today đếm lượt trả lời, Hard/Good/Easy là đúng; bỏ Manual/Rescheduled; mature theo interval trước >=21 ngày. True retention đếm mỗi revlog qua ease>0 và không phải Filtered factor=0, đồng thời type=Review hoặc lastIvl<=-86400 hoặc lastIvl>=1. Không dedup card/ngày; raw lastIvl>=21 là mature; Again fail, Hard/Good/Easy pass. Mỗi cửa sổ tính [start,end) theo next_day_at. Giới hạn: Manual mô tả first review/card/day nhưng pipeline code không thực hiện; discrepancy còn cần quyết định To-Be. Search/days giới hạn dữ liệu trước tổng hợp; oracle toàn lịch sử dùng days=0. Retention và Today có predicate riêng |

| Mã lỗi BA | Trigger | Kết quả theo source |
|---|---|---|
| ERR-ANKI-000-03 | AnswerCard gửi current state không còn khớp | Từ chối với invalid input sau hiệu chỉnh elapsed seconds; UI key chưa xác minh |

## Nguồn và kiểm chứng

- [docs-site/manual/studying.mdx:40](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L40)
- [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315)
- [proto/anki/scheduler.proto:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L80)
- [rslib/src/scheduler/states/review.rs:64](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L64)
- [rslib/src/stats/graphs/today.rs:17](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/today.rs#L17)
- [rslib/src/stats/graphs/retention.rs:53](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L53)
- [docs-site/manual/stats.mdx:229](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/stats.mdx#L229)

- [learning.rs:145](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/learning.rs#L145)
- [relearning.rs:174](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/relearning.rs#L174)

Bổ sung pipeline: [graphs/mod.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/mod.rs#L31), [true-retention.ts:105](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/graphs/true-retention.ts#L105).

## Giới hạn / câu hỏi mở

Phân tích Code/Docs theo snapshot; không có biên bản phê duyệt nghiệp vụ hoặc kết quả chạy kiểm thử. Thông báo UI/localization không được khẳng định bằng mã ERR phân tích. Owner xác nhận trước khi nghiệm thu runtime: maintainer phụ trách luồng và người dùng thử tác vụ.

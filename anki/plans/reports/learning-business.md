---
id: DOC-ANALYSIS-ANKI-LEARNING-001
title: Nghiệp vụ học và lập lịch Anki
version: "1.0.0"
phase: Analysis
domain: Learning
tags: [anki, learning, scheduler, fsrs, business-analysis]
depends_on: []
related_diagrams: []
author: BA Agent
last_updated: "2026-11-02"
status: draft
---

# Nghiệp vụ học và lập lịch Anki

Phạm vi: Anki desktop tại commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`, đã xác nhận bằng `git rev-parse HEAD`. Phân tích tĩnh; không build, chạy ứng dụng hay thay đổi source. Các đường dẫn dưới đây tính từ `sources/anki/` (checkout theo commit nêu trên); số sau dấu `:` là dòng nguồn. **Code** = đọc được trong implementation; **Doc** = tài liệu đi cùng commit; **Suy luận** = diễn giải nghiệp vụ, không phải yêu cầu đã được chủ sản phẩm duyệt.

## Actor và công việc cần hoàn thành

| Actor/vai trò | Công việc cần hoàn thành | Căn cứ |
|---|---|---|
| Người học | Mở bộ thẻ, tự truy hồi đáp án, đối chiếu và tự chấm để hệ thống chọn ngày ôn tiếp theo. | Doc: `docs-site/manual/studying.mdx:18`, `:40`, `:49`, `:58`. |
| Người học quản lý tải học | Giới hạn thẻ mới/ôn theo ngày, chỉnh retention và tạm bỏ qua thẻ để duy trì khối lượng phù hợp. | Doc: `docs-site/manual/deck-options.mdx:83`, `:129`, `:409`; code: `rslib/src/decks/limits.rs:98`. |
| Người học ôn theo mục tiêu | Tập trung vào tag/chủ đề/thẻ quên hoặc ôn trước lịch qua filtered deck. | Doc: `docs-site/manual/filtered-decks.mdx:7`, `:46`, `:63`, `:196`. |
| Scheduler, actor hệ thống | Xây hàng đợi, tính bốn kết quả có thể, áp dụng đánh giá và ghi lịch sử. | Code/API: `proto/anki/scheduler.proto:18`, `:42`, `:264`; `rslib/src/scheduler/answering/mod.rs:321`. |

Ba vai trò người dùng có thể là cùng một người; source đã đọc không chứng minh có phân quyền học viên/giáo viên/admin cho quy trình này. **Suy luận JTBD tổng quát:** chuyển việc “hôm nay cần học gì, ôn lúc nào” sang hệ thống, nhưng người học vẫn chịu trách nhiệm tự đánh giá trí nhớ trung thực.

## 15 quy tắc nghiệp vụ có truy vết

| Mã | Quy tắc | Mức chứng cứ và nguồn |
|---|---|---|
| BR-LEARN-001 | Phiên học thường lấy thẻ trong deck đang chọn và các deck con; người dùng xem số lượng New/Learning/Review trước khi Study Now. Kết thúc hàng đợi không đồng nghĩa mọi thẻ đã nhớ hoặc mọi thẻ trong deck đã được học: backend còn phân biệt learning chờ, new/review còn lại, thẻ buried. | Doc: `docs-site/manual/studying.mdx:10`, `:29`, `:40`. Code: `rslib/src/scheduler/queue/builder/mod.rs:135`; `rslib/src/scheduler/congrats.rs:30`. |
| BR-LEARN-002 | Again = sai/không nhớ; Hard = đúng nhưng khó nhớ; Good = đúng với nỗ lực; Easy = đúng gần như không tốn nỗ lực. Hard không biểu thị thất bại. Hệ thống nhận rating, không tự xác minh hiểu biết thực tế. | Doc: `docs-site/manual/studying.mdx:58`–`:77`. Code mapping 1–4: `rslib/src/scheduler/answering/mod.rs:217`. Phần “không tự xác minh” là suy luận từ contract tự chấm. |
| BR-LEARN-003 | New dùng cùng logic lựa chọn tiếp theo như Learning. Khi có learning steps: Again quay về bước đầu; Good tiến bước; Hard lặp bước hiện tại, riêng bước đầu lấy trung bình hai bước đầu, hoặc 1,5 lần bước đơn với mức tăng tối đa 1 ngày. Easy chuyển sang Review. Hết bước thì lịch review do thuật toán quyết định. Không áp dụng cứng quy tắc steps khi danh sách steps rỗng và FSRS short-term được phép. | Code: `rslib/src/scheduler/states/normal.rs:40`; `states/learning.rs:39`, `:86`, `:133`, `:180`; `states/steps.rs:38`, `:55`, `:68` (các đường dẫn `states/*` nằm trong `rslib/src/scheduler/`). |
| BR-LEARN-004 | Review + Again tăng lapse một lần, tính interval mới và vào Relearning khi có relearning steps; nếu không có steps có thể về thẳng Review hoặc tiếp tục trạng thái ngắn hạn theo FSRS. Again trong Relearning giữ số lapse của review gốc; không được hiểu mỗi lần nhấn Again trong cùng chuỗi học lại là một lapse mới. | Code: `rslib/src/scheduler/states/review.rs:95`–`:135`; `rslib/src/scheduler/states/relearning.rs:37`–`:82`. |
| BR-LEARN-005 | FSRS và legacy SM-2 là hai cách tính interval trong cùng quy trình đánh giá. Legacy dựa trên interval trước, ease, độ trễ và các multiplier; FSRS dùng memory state, desired retention, elapsed days, tham số cấu hình. Không được lấy công thức ease của SM-2 để giải thích interval FSRS. | Code: `rslib/src/scheduler/states/review.rs:169`, `:179`, `:220`; `rslib/src/scheduler/answering/mod.rs:484`–`:518`. Doc: `docs-site/manual/deck-options.mdx:388`. |
| BR-LEARN-006 | FSRS bật/tắt toàn cục, không bật riêng từng preset. Desired retention cao hơn hướng tới nhớ nhiều hơn tại hạn ôn và tăng tải ôn; mặc định tài liệu là 90%. Optimize học từ lịch sử của người dùng. “Reschedule cards on change” là quyết định riêng: mặc định tài liệu tắt, do đó đổi cấu hình không nhất thiết cập nhật ngay mọi due date cũ. | **Doc**, không xác minh toàn bộ UI/config flow: `docs-site/manual/deck-options.mdx:406`–`:413`, `:467`, `:500`–`:508`. Điểm đầu vào tính lịch đã kiểm chứng tại `rslib/src/scheduler/answering/mod.rs:512`. |
| BR-LEARN-007 | Hạn mức hôm nay ưu tiên override “today”, rồi mức riêng deck, rồi preset. Lượng đã học hôm nay được trừ. Mặc định thẻ mới cũng tiêu thụ review limit; bật New cards ignore review limit tách giới hạn này. Deck con bị giới hạn riêng, deck đang chọn giới hạn tổng; giới hạn tổ tiên chỉ được thêm khi bật Limits start from top. | Code: `rslib/src/decks/limits.rs:27`, `:33`, `:49`, `:98`–`:114`; `rslib/src/scheduler/queue/builder/mod.rs:130`–`:148`; `queue/builder/gathering.rs:35`–`:56`. Doc: `docs-site/manual/deck-options.mdx:91`, `:139`. |
| BR-LEARN-008 | Learning trong ngày không bị chặn bởi review limit như interday learning/review. Vì vậy đạt limit review không có nghĩa mọi hoạt động học trong ngày dừng. Thẻ học qua ranh giới ngày chịu review limit. | Code: `rslib/src/scheduler/queue/builder/gathering.rs:23`–`:60`; Doc: `docs-site/manual/deck-options.mdx:116`. |
| BR-LEARN-009 | Bury tạm ẩn tới khi sang ngày scheduler hoặc unbury thủ công; Suspend giữ ẩn tới khi unsuspend. Một card không đồng thời buried và suspended; không bury card đang suspended. Bury tự động theo siblings dựa trên cùng note, có tùy chọn new, review, interday learning; loại được gom sau không bury loại gom trước. | Code: `rslib/src/scheduler/bury_and_suspend.rs:32`, `:64`, `:96`, `:132`, `:148`; `rslib/src/scheduler/queue/builder/burying.rs:56`. Doc: `docs-site/manual/studying.mdx:125`, `:213`; `docs-site/manual/deck-options.mdx:325`–`:334`. |
| BR-LEARN-010 | Khi lapse chạm leech threshold (>0), rồi mỗi lần tăng thêm ceil(threshold/2), đánh dấu leech. Hệ thống gắn tag `leech` cho note; chỉ suspend card nếu hành động leech được cấu hình Suspend. Threshold 0 không phát leech theo hàm này. | Code: `rslib/src/scheduler/states/review.rs:95`, `:292`–`:300`; `rslib/src/scheduler/answering/mod.rs:194`, `:361`, `:572`. |
| BR-LEARN-011 | Filtered deck là tập thẻ tạm theo search, order và limit, không phải bản sao độc lập. Query tự loại suspended, buried và thẻ đã nằm trong filtered deck khác. Rebuild trả các thẻ hiện tại về home deck rồi tìm lại; không có kết quả và không cho phép rỗng thì trả lỗi. Empty trả thẻ về, không xóa thẻ học. | Code: `rslib/src/scheduler/filtered/mod.rs:82`–`:98`, `:123`–`:137`, `:175`–`:180`, `:202`. Doc: `docs-site/manual/filtered-decks.mdx:70`, `:80`, `:115`. |
| BR-LEARN-012 | Filtered với rescheduling bật dùng cấu hình home deck; kết quả Review trả thẻ về home deck, Learning/Relearning vẫn ở filtered deck cho đến khi kết thúc. Due review trả lời đúng thường trở về ngay; thất bại đi relearning. Review trước hạn có xử lý interval riêng theo thuật toán; không giả định cứ ôn trước là lùi lịch thêm nguyên interval. | Code: `rslib/src/scheduler/answering/mod.rs:475`–`:482`, `:153`; `rslib/src/scheduler/states/rescheduling_filter.rs:25`–`:54`; `rslib/src/scheduler/states/review.rs:169`, `:260`. Doc: `docs-site/manual/filtered-decks.mdx:188`–`:216`. |
| BR-LEARN-013 | Filtered với rescheduling tắt là Preview: Again/Hard/Good dùng delay cấu hình, Easy kết thúc; **bất kỳ delay bằng 0 cũng kết thúc**, không chỉ Easy. Khi kết thúc phục hồi queue/home deck; preview không cập nhật last_review_time như normal study, nhưng vẫn có revlog. | Code: `rslib/src/scheduler/states/preview_filter.rs:25`–`:47`; `rslib/src/scheduler/answering/preview.rs:17`–`:28`; `rslib/src/scheduler/answering/mod.rs:341`–`:353`. Doc: `docs-site/manual/filtered-decks.mdx:219`–`:226`. |
| BR-LEARN-014 | Một lần AnswerCard được ghi trong transaction: kiểm tra current state còn khớp, áp dụng next state, ghi revlog, cập nhật deck stats, xử lý siblings và lưu card. Nếu card đã thay đổi khác với state người dùng đang trả lời thì bị từ chối, sau khi hiệu chỉnh chênh elapsed seconds có thể giải thích do thời gian trôi. Thời gian trả lời bị cap theo preset trước khi ghi. | Code: `rslib/src/scheduler/answering/mod.rs:315`–`:362`. |
| BR-LEARN-015 | Today stats đếm **lượt trả lời**, không phải số card duy nhất; Hard/Good/Easy tính đúng. Phân loại learning/review/relearning/filtered; bỏ log Manual và Rescheduled. Mature dùng interval trước >=21 ngày. True retention có bộ lọc riêng cho log có rating và tác động scheduling; không nên đồng nhất với tỷ lệ đúng của mọi lượt học. | Code: `rslib/src/stats/graphs/today.rs:17`–`:42`; `rslib/src/stats/graphs/retention.rs:53`–`:71`. Doc: `docs-site/manual/stats.mdx:81`–`:96`. Xem chênh lệch tài liệu true retention bên dưới. |

## UC-LEARN-001 — Học hằng ngày

1. Người học chọn deck; hệ thống gom thẻ của deck và descendants theo giới hạn, thứ tự và bury settings (BR-001, 007–009).
2. Overview hiển thị New/Learning/Review. Người học chọn Study Now, thấy câu hỏi, tự nhớ rồi Show Answer (Doc: `docs-site/manual/studying.mdx:29`–`:59`).
3. Người học chọn Again/Hard/Good/Easy. Hệ thống lấy nhánh trạng thái tương ứng, ghi kết quả và tính hạn kế tiếp (BR-002–005, 014).
4. New/Learning hoàn thành steps hoặc Easy trở thành Review. Review quên thì học lại; review nhớ thì tiếp tục Review với interval mới. Không coi Suspend/Bury là giai đoạn trí nhớ: chúng là trạng thái loại khỏi queue, vẫn có lịch sử/type nền.
5. Hệ thống lặp cho tới hết thẻ có thể phục vụ; hiển thị thông tin thẻ chờ/hạn mức/buried và thống kê lượt học (BR-001, 015).

**Ngoại lệ:** đạt review limit vẫn có learning trong ngày; Again nhiều lần trong relearning không cộng lapse mỗi lần; leech có thể bị suspend; state cũ do chỉnh sửa card khiến answer bị từ chối; steps rỗng + FSRS không nhất thiết đi qua đúng chuỗi bước cố định; sang ngày scheduler tự unbury, không tự unsuspend. “Hết phiên hôm nay” không chứng minh đạt retention mục tiêu — đây là suy luận nghiệp vụ từ hạn mức và trạng thái kết thúc.

## UC-LEARN-002 — Ôn tập có mục tiêu bằng filtered deck

1. Người học xác định search, thứ tự và số lượng; ví dụ một tag hoặc thẻ đã quên. Chọn có/không reschedule (Doc: `docs-site/manual/filtered-decks.mdx:89`, `:107`, `:115`, `:219`).
2. Hệ thống loại thẻ buried/suspended/ở filtered khác, chuyển thẻ phù hợp vào deck tạm và giữ home deck (BR-011).
3. Nếu reschedule bật, ratings đổi lịch theo home deck; thẻ trở về khi đến Review. Nếu tắt, ratings điều khiển lượt preview, Easy hoặc delay 0 kết thúc và phục hồi thẻ (BR-012–013).
4. Người học dùng Empty để trả hết thẻ còn lại hoặc Rebuild để chạy lại điều kiện tìm (BR-011).

**Ngoại lệ:** search không có thẻ hợp lệ có thể báo lỗi dù browser tìm thấy thẻ bị loại; thẻ đang trong filtered deck khác không được mượn lần nữa; ôn trước quá sớm không bảo đảm đẩy due date xa thêm; lặp preview vẫn tạo lịch sử lượt trả lời nên không đồng nghĩa “không ghi nhận học”; chọn reschedule sai làm thay đổi lịch thật, không chỉ thay đổi màn hình.

## Mô hình chuyển trạng thái cần giữ khi đặc tả

Normal: `New → Learning → Review`; `Learning → Review` có thể đi thẳng bằng Easy; `Review → Relearning → Review` khi quên và có steps. Review + Hard/Good/Easy ở lại Review. Không có steps có thể bỏ qua Learning/Relearning; FSRS short-term có nhánh riêng, nên đây là mô hình thường gặp chứ không phải mọi chuyển trạng thái bắt buộc. Contract tách `Normal{New,Learning,Review,Relearning}` và `Filtered{Preview,ReschedulingFilter}` tại `proto/anki/scheduler.proto:80`–`:127`. Bury/Suspend là queue overlay, không nằm trong oneof trí nhớ normal này.

## Điểm không khớp và giới hạn chứng cứ

- **Bury learning:** `docs-site/manual/studying.mdx:208` nói chỉ new/review bị bury và không learning; nhưng `docs-site/manual/deck-options.mdx:334` và `rslib/src/scheduler/queue/builder/burying.rs:62` có interday learning. Với commit này, mô tả chính xác cần phân biệt intraday với interday; không lặp lại phát biểu tổng quát cũ.
- **True retention:** `docs-site/manual/stats.mdx:229` nói chỉ lần review đầu mỗi card/ngày được tính. `rslib/src/stats/graphs/retention.rs:53`–`:75` lọc rồi đếm từng log phù hợp, không thấy thao tác chọn lần đầu theo card/day trong hàm; `rslib/src/stats/graphs/mod.rs:52`–`:69` chuyển trực tiếp revlog từ storage. Chưa kiểm thử runtime tình huống hai review đủ điều kiện trong cùng ngày; cần xác nhận quy tắc mong muốn trước khi dùng “first review per day” làm acceptance criterion.
- Không chứng minh hiệu quả khoa học của thuật toán bằng đọc mã. Con số retention mong muốn là tham số/mục tiêu; không phải bảo đảm người học sẽ đạt cùng tỷ lệ thực tế.
- Không kiểm toán mọi add-on/custom scheduling, client mobile hoặc phiên bản phát hành ngoài commit đã chốt. Custom scheduling có thể thay đổi next states; báo cáo mô tả đường mặc định đã đọc.

## Câu hỏi chưa giải quyết

1. Chủ tài liệu muốn đặc tả đúng snapshot source hay hành vi bản Anki đang được triển khai? Hai nguồn có chênh lệch nêu trên.
2. Với true retention, quy tắc sản phẩm chuẩn có thực sự là chỉ lần đầu/ngày, hay mọi lượt đủ điều kiện? Cần owner thống kê xác nhận hoặc tái hiện runtime.

Status: DONE_WITH_CONCERNS
Summary: Hoàn thành 15 quy tắc truy vết, actor/JTBD, hai hành trình và ngoại lệ; phân biệt code, docs và suy luận.
Concerns/Blockers: Hai khác biệt tài liệu/source đã ghi; chưa chạy runtime theo phạm vi read-only.

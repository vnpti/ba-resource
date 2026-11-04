# Review tích hợp oracle 035 / 067 / 072 / 077

Date: 2026-11-03. Status: **DONE_WITH_CONCERNS**. Không có blocker export hoặc mâu thuẫn oracle trọng yếu; một bổ sung nhỏ giúp fixture072 tái lập rõ hơn. Read-only đối với source/BA/evidence; chỉ ghi report này. Không build/chạy Anki, không chạy TC.

## Findings

**Low — TC-ANKI-072 nên ghi rõ clock client/server đồng bộ trong 300 giây.** TC common setup đóng băng clock tại 2026-11-02T00:00:00Z; fixture072 dùng SimpleServer riêng nhưng chưa nói server cũng dùng clock đó. Nếu chỉ freeze client, bước Sync có thể trả ClockIncorrect trước FullSyncRequired. Preconditions hiện đã yêu cầu request thành công, nên đây là chi tiết setup cần cụ thể hóa, không phải oracle sai hay blocker export.

- Vị trí: [test-cases.md](../../docs/anki/test/test-cases.md), mục1 clock mặc định và TC-ANKI-072 Preconditions; cùng preconditions trong [evidence](../../evidence/oracle-resolutions-2026-11-03.json).
- Nguồn: [normal.rs:69–84](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/normal.rs#L69-L84) gọi [status.rs:42–64](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/status.rs#L42-L64): server phải should_continue=true, chênh lệch current_time tuyệt đối >300 giây trả ClockIncorrect trước so metadata.
- Đề xuất thêm: “clock client/server được harness đồng bộ, abs(remote.current_time−local.current_time)<=300s; server should_continue=true trước mỗi nhánh.” Không đổi expected hoặc ID.

## Kết quả đối chiếu

| Case | Kết quả |
|---|---|
|035|F035-empty đủ guard: params4/5/6 rỗng, preset/FSRS đã lưu, assignment không pending, Optimize current preset, healthCheck=false. Request search mặc định đúng source; response empty/0/health absent, no-reviews message và không gán params mới khớp báo cáo nguồn. Không trộn raw log count với training count hay Optimize All.|
|067|F067-min **chỉ hai log**, không dùng expected22row của báo cáo mở rộng. Cùng card1001, 05:00 Again và06:00 Good ngày03/11 UTC, rollover04:00. today/week/month/year/allTime đều `(1,1,0,0)`, Count2, Young/Total50.0%, MatureN/A; yesterday zero/N/A. Search cid1001 giữ kết quả. Chú thích rõ không cover mọi filter/boundary; không nhầm first/day manual thành code.|
|072|Giữ đủ guard nonempty+mod khác+schema khác và snapshot từng nhánh; giới hạn SimpleServer/caller. Cancel chỉ giữ nội dung, không hứa byte-identical metadata; Download replace active local, Upload replace server và không tự đổi A chưa sync. Login callback tiếp tục sync, backup request và hosted limitation đều được giữ.|
|077|Giữ normalized filename, hash khác, dirty/cursor/USN, fetch trước upload, completion thực sự và thứ tự tuần tự; nhánh reverse và local-only change tránh diễn giải server/first-writer luôn thắng. Phân biệt add_file collision, sync overwrite và mtime tracking. Base64 A/B và hai file PNG đều69byte, SHA1 đúng như Given; không giả định race không thứ tự hay rollback filesystem.|

Đã kiểm bằng đối chiếu cấu trúc:

- Evidence→catalog: title/Given/When/Then/sources của bốn scenario và data/steps/expected/sources của bốn test khớp chính xác.
- AC Markdown chứa đúng Given/When/Then; TC Markdown chứa đủ preconditions/data/steps/expected/limits/cleanup của evidence.
- BR014/025/027/028 trong requirements.json và spec.md khớp title/when/then/unless. Guard và giới hạn không bị mất khi tích hợp.
- Story→AC→TC→FR/BR đúng và tồn tại; CSV RTM bốn dòng là Specified/Not Run. Các nguồn file/line tồn tại tại checkout pinned.
- Bốn case không còn blocker design; tất cả86tests vẫn Not Run. Catalog1.0.1 Draft, coverage AC86/86 là thiết kế, không phải kết quả chạy. AC approval vẫn Draft.

## Phạm vi và unresolved questions

Đã đọc evidence bốn case, catalog targeted, AC/TC tương ứng, BR/SRS tương ứng và báo cáo oracle; kiểm source có mục tiêu cho035/default search và072/clock guard. Không đánh giá lại toàn bộ86case, không render tài liệu hoặc xác minh runtime/harness.

Unresolved questions: Không còn câu hỏi oracle As-Is trong bốn case. Quyết định To-Be về manual retention vẫn mở và được ghi đúng; harness/runtime chưa thực thi. Bổ sung clock guard072 là khuyến nghị rõ hóa setup ở trên.

## Resolution trước export

2026-11-03: đã xác minh evidence case072 và TC072 Preconditions bổ sung client/server dùng cùng clock t0, xác nhận timestamp đồng bộ trước request. Finding Low đã resolved; điều kiện request thành công vẫn bao gồm server cho tiếp tục. Trạng thái review cuối: **DONE**, không còn finding chưa xử lý trong phạm vi tích hợp.

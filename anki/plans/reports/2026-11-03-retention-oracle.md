# Oracle As-Is cho AC/TC-ANKI-067

Ngày: 2026-11-03. Status: DONE. Phạm vi: phân tích tĩnh checkout `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`; không build/chạy Anki, không sửa source hay tài liệu BA. TC vẫn **Not Run**. Oracle được xác định từ code, chưa được xác nhận bằng thực thi.

## Kết luận

**True retention đếm mọi revlog đủ điều kiện, không lấy riêng review đầu của mỗi card/ngày.** Hai Review log cùng card, cùng ngày scheduler, Again rồi Good, đều được cộng: fail 1, pass 1, retention 50.0%. Không có dedup theo card/day trong SQL đầu vào, Rust aggregation, protobuf hay frontend bảng retention.

Manual tại cùng commit nói chỉ lần đầu/ngày; đây là discrepancy tài liệu–code đã xác định, không còn là thiếu oracle As-Is. Có thể chuyển design status của AC/TC-067 từ Blocked sang Specified; approval vẫn Draft, execution/actual vẫn Not Run. Nếu muốn đổi sản phẩm để theo manual, đó là quyết định To-Be riêng.

## Bằng chứng xuyên suốt pipeline

Mọi link cố định cùng commit; số dòng là số dòng source checkout.

| Chặng | Bằng chứng và kết luận |
|---|---|
| Request | [WithGraphData.svelte:30–41](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/graphs/WithGraphData.svelte#L30-L41) gọi `graphs({search,days})`. [stats/service.rs:22–27](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/service.rs#L22-L27) chuyển trực tiếp vào `graph_data_for_search`. |
| Search/range | [graphs/mod.rs:31–69](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/mod.rs#L31-L69): search rỗng dùng toàn bộ revlog; search khác rỗng chỉ lấy cid được chọn. `days=0` lấy từ epoch; `days>0` lấy từ `next_day_at-(days+1)*86400`. Vec đọc được chuyển trực tiếp vào `calculate_true_retention`. |
| SQL/deserialize | [get.sql:1–10](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/get.sql#L1-L10) SELECT từng row; không DISTINCT/GROUP BY/MIN/window function. [storage/revlog/mod.rs:122–132](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/mod.rs#L122-L132) chỉ thêm cid membership và `id >= after*1000`; [175–179](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/mod.rs#L175-L179) chỉ thêm id lower bound. [34–45](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/mod.rs#L34-L45) map từng row, không dedup. |
| Clock | [scheduler/mod.rs:35–82](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/mod.rs#L35-L82) lấy/cached timing và rollover. [timing.rs:27–65](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/timing.rs#L27-L65) xác định mốc rollover kế tiếp theo current UTC offset. Retention dùng mốc này, không dùng midnight/calendar date hay `local_offset_secs` để group log. |
| Qualification | [revlog/mod.rs:107–131](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/revlog/mod.rs#L107-L131): `ease>0` và không phải `Filtered && factor==0`. [retention.rs:53–75](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L53-L75) thêm `type==Review OR lastIvl<=-86400 OR lastIvl>=1`, rồi cộng từng log. |
| Windows/classification | [retention.rs:16–44](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L16-L44): today/yesterday/7/30/365 ngày, all từ epoch, mọi cửa sổ `[start,end)`. [64–71](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L64-L71): raw `lastIvl<21` là young; còn lại mature; rating 1 fail, rating khác đã qua filter pass. [revlog/mod.rs:24–25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/revlog/mod.rs#L24-L25) chia id milliseconds cho 1000 trước so sánh. |
| Response/display | [stats.proto:162–175](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/stats.proto#L162-L175) chỉ chứa bốn counter mỗi window, không chứa cid để frontend dedup. [TrueRetention.svelte:30–36](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/graphs/TrueRetention.svelte#L30-L36) nhận response nguyên trạng. [true-retention.ts:37–121](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/graphs/true-retention.ts#L37-L121) cộng counter, retention=`pass/(pass+fail)`, 1 chữ số thập phân theo locale, denominator 0 → N/A; all-time row chỉ hiện khi RevlogRange.All. |
| Table | [TrueRetentionSingle.svelte:47–58](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/graphs/TrueRetentionSingle.svelte#L47-L58) hiện pass/fail/%; [TrueRetentionCombined.svelte:47–70](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/graphs/TrueRetentionCombined.svelte#L47-L70) hiện Young/Mature/Total/Count từ các counter, không lấy trung bình các tỷ lệ. |
| Discrepancy | [manual/stats.mdx:226–230](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/stats.mdx#L226-L230) nói “Only one review per day - the first one - counts.” Không có code tương ứng trên pipeline vừa truy vết. |

Manual/Rescheduled thông thường bị loại do rating 0: [revlog/mod.rs:155–176](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/revlog/mod.rs#L155-L176) tạo log với `button_chosen:0`. Không mô tả nhầm rằng retention loại hai loại này chỉ bằng enum: predicate thực tế không kiểm tra enum Manual/Rescheduled. Không đưa rating bất hợp lệ ngoài 0–4 vào fixture.

Interval âm là giây ([revlog/mod.rs:44–49](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/revlog/mod.rs#L44-L49)), nhưng phân nhóm mature dùng số raw, không normalize về ngày. Review với lastIvl âm ngắn vẫn qua nhánh `type==Review`; non-Review -86399 bị loại, -86400 được lấy và là young. Không thay oracle bằng mô tả subtitle tổng quát.

## Fixture hữu hạn F067

Collection/profile tạm riêng, không dữ liệu/credentials người dùng; không sync/add-on. Scheduler V2/new cutoff, creation offset UTC, current offset UTC, rollover 04:00, clock cố định `2026-11-03T12:00:00Z`; tạo/mở collection sau khi đặt clock để tránh timing cache cũ. `T=next_day_at=1793764800` (`2026-11-04T04:00:00Z`), `D=86400`. Request chính `search="", days=0` (All history). Locale en-US để so chuỗi phần trăm dưới đây; locale khác giữ giá trị, chấp nhận dấu phân cách locale.

Tạo 21 card tồn tại, cid 1001–1021, cùng deck tạm. A là cid 1001 ở hai row 01–02; các row còn lại mỗi row dùng cid riêng theo bảng. Có đúng 22 revlog row, không row khác. Mọi row `usn=-1, ivl=1, time=1000` (answer duration milliseconds), trừ cột ghi rõ; trường SQL `id` chính là thời điểm trả lời milliseconds. `factor` cần được chỉ rõ vì quyết định loại cramming. Fixture là dữ liệu tổng hợp để kiểm aggregation, không phải lịch học tạo bằng thao tác answer.

| Row | cid | type | ease/rating | lastIvl | factor | id (epoch ms) | Ý nghĩa |
|---|---:|---:|---:|---:|---:|---:|---|
|01|1001|1|1|20|2500|1793682000000|A Again 05:00 hôm nay|
|02|1001|1|3|20|2500|1793685600000|A Good 06:00 cùng ngày|
|03|1002|1|2|21|2500|1793682001000|Hard, mature đúng ngưỡng|
|04|1003|2|3|-86400|2500|1793682002000|Relearning đúng 1 ngày âm, young|
|05|1004|0|1|-86399|2500|1793682003000|Learning dưới 1 ngày, loại|
|06|1005|3|3|21|0|1793682004000|Filtered cramming, loại|
|07|1006|3|4|21|2500|1793682005000|Filtered có scheduling, mature pass|
|08|1007|4|0|21|2500|1793682006000|Manual rating0, loại|
|09|1008|5|0|21|2500|1793682007000|Rescheduled rating0, loại|
|10|1009|1|3|-600|2500|1793682008000|Review OR branch, young pass|
|11|1010|1|1|21|2500|1793592000000|T−2D: start yesterday|
|12|1011|1|3|21|2500|1793678400000|T−D: start today|
|13|1012|1|3|20|2500|1793160000000|T−7D: start week|
|14|1013|1|1|21|2500|1793159999999|1ms trước week|
|15|1014|1|1|20|2500|1791172800000|T−30D: start month|
|16|1015|1|3|21|2500|1791172799999|1ms trước month|
|17|1016|1|2|21|2500|1762228800000|T−365D: start year|
|18|1017|1|1|20|2500|1762228799999|1ms trước year|
|19|1018|1|3|21|2500|1793764800000|T: end exclusive, loại|
|20|1019|1|1|21|2500|1793764799999|1ms trước T, được lấy|
|21|1020|0|3|1|2500|1793682009000|Learning lastIvl=1, được lấy|
|22|1021|0|3|0|2500|1793682010000|Learning lastIvl=0, loại|

Type: 0 Learning; 1 Review; 2 Relearning; 3 Filtered; 4 Manual; 5 Rescheduled ([enum](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/revlog/mod.rs#L65-L75)). Row 19–20 cố ý nằm sau clock “now” để test upper cutoff bằng dữ liệu injection: code giới hạn tại next rollover, không tại now. Không dùng chúng để khẳng định scheduler tự sinh log tương lai.

### Expected F067, days=0

YP/YF/MP/MF là các counter response. Count=YP+YF+MP+MF. Phần trăm là UI en-US, 1 chữ số thập phân; N/A khi không có mẫu.

| Window | Khoảng epoch seconds | YP | YF | MP | MF | Young | Mature | Total | Count |
|---|---|---:|---:|---:|---:|---|---|---|---:|
|today|[1793678400,1793764800)|4|1|3|1|80.0%|75.0%|77.8%|9|
|yesterday|[1793592000,1793678400)|0|0|0|1|N/A|0.0%|0.0%|1|
|week|[1793160000,1793764800)|5|1|3|2|83.3%|60.0%|72.7%|11|
|month|[1791172800,1793764800)|5|2|3|3|71.4%|50.0%|61.5%|13|
|year|[1762228800,1793764800)|5|2|5|3|71.4%|62.5%|66.7%|15|
|allTime|[0,1793764800)|5|3|5|3|62.5%|62.5%|62.5%|16|

Counter arithmetic được đối chiếu bằng Python chuẩn, độc lập với Anki. Đây là kiểm phép tính fixture, **không** chạy app/test runtime hay gán Pass cho TC.

Phép thử cô lập quyết định first/day: cùng F067, request search `cid:1001`, days=0. today/week/month/year/allTime phải `(YP,YF,MP,MF)=(1,1,0,0)`; Young/Total 50.0%, Mature N/A, Count2. yesterday `(0,0,0,0)`, mọi retention N/A, Count0. Nếu first/day thì sẽ chỉ có fail1, Count1 và 0.0%; đó **không** là oracle code hiện tại.

## Thay thế AC-ANKI-067 (đề xuất nguyên văn)

ID/US/FR/BR giữ nguyên: AC-ANKI-067 → US-ANKI-17 → FR-RPT-STAT-001 → BR-ANKI-025; ERR không có. Kind boundary; design_status Specified; blocker bỏ/null; approval Draft.

```gherkin
Scenario: AC-ANKI-067 — True retention đếm mọi log đủ điều kiện cùng card/ngày
  Given collection tạm F067 có đúng 22 revlog như fixture, clock UTC cố định,
    rollover 04:00, next_day_at=1793764800, locale en-US và All history (days=0)
  When lấy graph data toàn collection và xem True retention ở Young, Mature, All
  Then các counter và tỷ lệ của 6 windows khớp bảng Expected F067
    And log 01 Again và log 02 Good cùng cid1001/ngày đều được cộng
    And khi search cid:1001, Today có pass1 fail1 retention50.0% Count2
    And Yesterday của search đó có Count0 và retention N/A
    And các log không đủ điều kiện và log đúng upper cutoff không được cộng
```

Sources cần thêm đúng pipeline: storage/revlog/get.sql:1; storage/revlog/mod.rs:122 và175; stats/graphs/mod.rs:31; stats/graphs/retention.rs:16 và53; revlog/mod.rs:107; ts/routes/graphs/true-retention.ts:105; manual/stats.mdx:229 để lưu discrepancy.

## Thay thế TC-ANKI-067 (đề xuất nguyên văn)

Title: True retention nhiều log/card/ngày, qualification và cửa sổ scheduler. Design Specified; priority kế thừa hiện tại; execution/actual **Not Run**; automation chưa có. References giữ cùng AC/US/FR/BR.

Preconditions/data: F067 ở trên, không có log ngoài bảng; collection disposable; clock/timezone/rollover được kiểm trước request; All history, locale en-US. Dùng harness fixture có khả năng chèn raw revlog và cố định clock; không mô phỏng bằng chuỗi answer rồi giả định log tự sinh giống fixture. Đây là test specification, chưa triển khai harness.

1. Tạo collection/card/revlog F067; đọc lại đủ 22 row và xác nhận hai row01–02 cùng cid1001, ID khác nhau. Expected: dữ liệu đúng bảng, next_day_at=1793764800.
2. Gọi graph data với search rỗng, days0. Expected: sáu object trueRetention có YP/YF/MP/MF đúng bảng Expected, bao gồm allTime Count16.
3. Mở bảng True retention Young rồi Mature rồi All; đối chiếu từng window. Expected: pass/fail của hai mode đơn đúng counter; phần trăm/count của All đúng Expected; Yesterday young hiện N/A. Không dùng rounding trung gian hay trung bình Young/Mature để tính Total.
4. Đổi search thành `cid:1001`, days0. Expected: Today Count2, Young pass1 fail1, 50.0%; Mature N/A; Yesterday Count0/N/A. Các window lớn có cùng hai log.
5. Đổi search về rỗng và đối chiếu boundary membership: row11 chỉ yesterday, không today; row12 today, không yesterday; row13/15/17 nằm trong cửa sổ tương ứng; row14/16/18 nằm ngoài cửa sổ tương ứng; row19 loại mọi window; row20 thuộc today. Row05/06/08/09/22 không được cộng; row04/07/10/21 được cộng như fixture. Expected: counter trở về bảng F067.
6. Đóng/xóa collection và profile tạm; khôi phục clock/timezone/preferences harness. Expected: không thay đổi collection người dùng, không sync/network credentials, không fixture sót.

Cleanup khi lỗi: vẫn thực hiện bước6; lưu response/counter thực tế và môi trường vào bằng chứng chạy riêng. Không sửa expected theo kết quả runtime nếu chưa điều tra.

## Cập nhật SRS/BR và trạng thái liên quan cần thiết

- FR-RPT-STAT-001.output: thay phần “first-review/day retention còn cần đối chiếu” bằng “True retention As-Is cộng từng revlog đủ điều kiện trong cửa sổ scheduler; cùng card/ngày có thể đóng góp nhiều lượt; discrepancy với manual được ghi nhận.” Giữ ID/priority/input.
- BR-ANKI-025: giữ quy tắc Today hiện tại; bổ sung retention riêng: qualification `ease>0 && !(type=Filtered && factor=0) && (type=Review || lastIvl<=-86400 || lastIvl>=1)`; mỗi row đếm một lượt trong từng window chứa nó; mature raw lastIvl>=21; Again fail, Hard/Good/Easy pass; không dedup card/ngày. Window 1/2/7/30/365 ngày và epoch theo `[start,next_day_at)`, riêng yesterday kết thúc tại T−D. Không lẫn Today counter với retention.
- BR-ANKI-025.unless: thay uncertainty bằng “Manual cùng commit mô tả first review/card/day nhưng code hiện tại không thực hiện; đây là discrepancy tài liệu–code. Dữ liệu lấy trước khi tổng hợp có thể bị giới hạn bởi search và days; full-history oracle dùng days=0.” Thêm các sources pipeline phía trên; không xóa nguồn Today.
- Đồng bộ case067 trong AC, TC, catalog, RTM/gap list/decision register; chỉ bỏ design blocker067. Nếu các case khác không đổi: Specified83/86, Blocked3/86, execution0/86; FR/BR/ERR coverage giữ nguyên. Không đổi Draft thành Approved, không đổi Not Run thành Pass.

## Kiểm thử upstream đã đọc và giới hạn

[storage/revlog/mod.rs:308–327](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/mod.rs#L308-L327) kiểm storage trả cả hai log cùng cid nhưng không trực tiếp test retention. [timing.rs:350–393](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/timing.rs#L350-L393) có assertions rollover trước/đúng04:00. [pylib/tests/test_stats.py:11–38](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tests/test_stats.py#L11-L38) có card-history hai log và report smoke tests; không chứng minh first/day. Tìm symbols true_retention/young_passed/youngPassed và retention trong stats/Rust và test TS/Python không tìm thấy test chuyên biệt cho quy tắc first/day. Không chạy những tests này.

Unresolved questions: Không còn câu hỏi để chốt oracle As-Is067. Còn quyết định sản phẩm ngoài scope: cập nhật manual theo code hay thay implementation theo first/day; chỉ stakeholder/upstream có thể chốt To-Be. Khả năng thực thi của môi trường/harness chưa được xác minh, nên execution vẫn Not Run.

---
id: DOC-ORACLE-FSRS-ANKI-035
title: Oracle AC/TC-ANKI-035 — Optimize không có lịch sử
version: "1.0.0"
phase: VerificationDesign
domain: Anki
tags: [fsrs, oracle, source-review, acceptance-criteria]
depends_on: [DOC-SRS-ANKI-001, DOC-US-ANKI-001, DOC-AC-ANKI-001, DOC-TC-ANKI-001]
related_diagrams: []
author: BA Agent
last_updated: "2026-11-03"
status: draft
---

# Oracle AC/TC-ANKI-035

| Phiên bản | Ngày | Thay đổi |
|---|---|---|
| 1.0.0 | 2026-11-03 | Lần theo call path Optimize current preset; chốt oracle tĩnh và fixture thay thế case 035 |

**Status: DONE.** Có thể đổi thiết kế AC/TC-ANKI-035 từ `Blocked` sang `Specified`; thực thi vẫn `Not Run`. Không chạy/build Anki, không sửa source hay bộ SRS/QA. HEAD được đọc lại và đúng `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`.

**Kết luận code-verified:** Khi tập mẫu huấn luyện có 0 FSRS item, `ComputeFsrsParams` trả thành công: `params` giữ nguyên `current_params`, `fsrs_items = 0`, `health_check_passed` không có giá trị. UI Optimize current preset hiển thị khóa `deck-config-fsrs-params-no-reviews`, giữ nguyên tham số hiện tại. Không phát sinh lỗi “thiếu 400 reviews”, không tự sinh một vector tham số mới trong nhánh này. [params.rs:95–108][P95], [FsrsOptions.svelte:235–267][U235].

## 1. Phạm vi và tài liệu đầu vào

- SRS hiện tại `docs/anki/srs/spec.md`, FR-LRN-FSRS-001 và BR-ANKI-014, draft 1.0.0: mới mô tả optimize theo lịch sử, chưa có nhánh zero-item. Đây là bổ sung oracle còn thiếu, không thay đổi hành vi upstream.
- `docs/anki/test/qa-catalog.json`: AC-ANKI-035 tại dòng 1622 và TC-ANKI-035 tại dòng 4106 đang Blocked. Story US-ANKI-10; FR-LRN-FSRS-001; BR-ANKI-014; ERR `[]` giữ nguyên vì kết quả này là thành công có thông báo, không phải mã lỗi.
- Quy tắc Given/When/Then theo ba-ac; đầu ra ở report này theo quyền sở hữu được giao. Controller đồng bộ SRS/JSON/AC/TC sau đó; report không tự tuyên bố bộ tài liệu đã cập nhật.
- Mọi liên kết source bên dưới khóa commit; “code-verified” chỉ là đối chiếu mã tĩnh. Test nguồn đã đọc nhưng **không chạy**.

## 2. Call path đầy đủ của Optimize current preset

| Tầng | Luồng và bằng chứng |
|---|---|
| UI khả dụng | FSRS controls chỉ render khi `$fsrs` true: [FsrsOptionsOuter.svelte:115][OUT115]. Nút Optimize gọi `computeParams()`, không có điều kiện disabled dựa trên review count: [FsrsOptions.svelte:433][U433]. |
| Guard trước request | Nếu đang compute: yêu cầu abort và return. Nếu `presetAssignmentsChanged()` true: hiện thông báo cần lưu rồi return. Fixture phải save/reopen để tránh guard này: [FsrsOptions.svelte:200][U200]; trạng thái assignment tại [lib.ts:165][L165], getter [lib.ts:278][L278]. |
| Request | `currentParams = fsrsParams($config)`; search là custom `paramSearch` nếu truthy, nếu không là `preset:"P035" -is:suspended`; date rỗng → `0n`; đếm relearn steps với tổng thời gian <1440 phút; truyền healthCheck. [FsrsOptions.svelte:81][U81], [192–233][U192], [lib.ts:468][L468]. |
| TS → local transport | Generator tạo hàm `computeFsrsParams` qua `postProto(methodName, request, responseType)`: [typescript.rs:71][TS71]. `postProto` serialize protobuf, gọi local `/_anki/${method}` rồi decode: [post.ts:11][POST11]. Đây là transport nội bộ desktop, không đề xuất API HTTP công khai hay ERR HTTP mới. |
| Python dispatch | `compute_fsrs_params` nằm trong exposed backend list: [mediasrv.py:1213][M1213]. Camelcase dispatch → `raw_backend_request` → `col._backend.compute_fsrs_params_raw(request.data)`: [mediasrv.py:1241][M1241], [1273][M1273]. Collection phải mở. |
| Python → Rust | Generator raw wrapper gọi `_run_command`: [python.rs:48][PY48]; triển khai Python gọi bridge `command`: [_backend.py:159][BE159]; bridge gọi `run_service_method`: [rsbridge/lib.rs:49][RS49]. Rust generator decode/dispatch/encode: [rust_interface.rs:141][RI141], [217][RI217]. Đây là bằng chứng generator, không giả vờ đã build/đọc file generated chưa tồn tại. |
| Contract/service | Protobuf khai báo request/response: [scheduler.proto:357][PROTO357]. Service chuyển request thành `ComputeParamsRequest`, preset index/count = 1: [scheduler/service/mod.rs:264][S264]. |
| Training scope | `revlog_for_srs` xử lý search; whole-collection có thể lấy cả log của card đã xóa, search khác lấy logs của cards được tìm thấy: [params.rs:211][P211]. Fixture collection rỗng tránh khác biệt này. |
| Zero items | `fsrs_items_for_training` nhóm log theo card và chuyển thành items; vector log rỗng tạo vector item rỗng: [params.rs:351][P351]. `fsrs_items == 0` trả sớm với tham số đầu vào, count 0, health absent, trước cả gọi thư viện optimize và health check: [params.rs:95][P95]. |
| UI nhận kết quả | Vector rỗng → `alreadyOptimal` true; vector không rỗng được trả nguyên cũng khớp so sánh 4 số thập phân. `fsrsItems == 0` chọn `deckConfigFsrsParamsNoReviews`; không gán `config.fsrsParams6` vì chỉ gán khi `!alreadyOptimal`. Cuối cùng `computingParams=false`: [FsrsOptions.svelte:235][U235], [278][U278]. |

Tên “alreadyOptimal” là biến điều khiển của UI. Với zero items, **không** diễn giải rằng mô hình đã được tối ưu theo lịch sử cá nhân: thông báo thực tế là không tìm thấy reviews.

## 3. Fixture chính có thể tái lập

Fixture `F035-empty` là dữ liệu thiết kế để đội QA dựng trong môi trường test sau này, không phải kết quả đã chạy.

| Thành phần | Giá trị cố định |
|---|---|
| App | Desktop tại commit nêu trên, không add-on; locale English để đối chiếu chuỗi FTL chính xác |
| Collection/profile | Collection test mới đang mở; 0 notes, 0 cards, 0 revlog rows toàn collection; không import/sync concurrent |
| Deck/preset | Normal deck `D035`, đã gán preset tên `P035`, đã lưu; đóng rồi mở lại Deck Options của D035, không đổi assignment |
| FSRS | Đã bật và lưu trước khi mở lại; desired retention 0.90, không thay đổi trong case |
| Params | `fsrs_params_4 = []`, `fsrs_params_5 = []`, `fsrs_params_6 = []` — mặc định stored config cho các trường này là rỗng; UI lấy mảng6 rỗng. Không nhầm giá trị `defaults` dùng cho tham chiếu với stored config. [deckconfig/mod.rs:77][DC77], [update.rs:55][DC55], [update.rs:96][DC96], [lib.ts:468][L468] |
| Search/date | `paramSearch = ""`; `ignoreRevlogsBeforeDate = ""` |
| Other controls | `relearnSteps = [10]` (phút); health check false; Reschedule cards on change false; không Evaluate/Optimize job đang chạy |
| Operation | Chỉ bấm **Optimize current preset** một lần; không bấm **Save and Optimize/Optimize All Presets** |

Request nội bộ tương ứng, biểu diễn kiểm thử chứ không phải JSON HTTP contract:

```text
ComputeFsrsParamsRequest {
  search: 'preset:"P035" -is:suspended',
  current_params: [],
  ignore_revlogs_before_ms: 0,
  num_of_relearning_steps: 1,
  health_check: false
}
```

Response kỳ vọng:

```text
params = []
fsrs_items = 0
health_check_passed = absent   // Rust None; TS undefined; không phải false
```

Backend không gọi `fsrs::compute_parameters` trong fixture này: return ở dòng102–107 trước lời gọi ở dòng150. Không có phép ghi params/card/due/revlog trong nhánh return. Các thao tác dựng fixture/lưu bật FSRS xảy ra **trước** snapshot baseline của TC.

## 4. Replacement AC-ANKI-035

- Title: **Optimize current preset khi không có lịch sử giữ nguyên tham số và thông báo không có reviews**.
- Kind: boundary.
- Story: US-ANKI-10; FR: FR-LRN-FSRS-001; BR: BR-ANKI-014; ERR: `[]`.
- `design_status: Specified`; bỏ blocker cũ; không đổi trạng thái chạy thành Pass.

```gherkin
Scenario: AC-ANKI-035 — Optimize trên collection không có lịch sử
  Given collection test F035-empty đang mở, không có note/card/revlog
  And deck D035 dùng preset P035 đã lưu, FSRS bật và tham số hiện tại là []
  And search và ignore-before date rỗng, relearning steps [10], health check tắt
  And không có đổi preset assignment chưa lưu hoặc tác vụ Optimize/Evaluate đang chạy
  When người dùng bấm Optimize current preset một lần
  Then backend trả thành công với params [], fsrs_items 0 và health_check_passed không có giá trị
  And UI hiện thông báo của khóa deck-config-fsrs-params-no-reviews
  And tham số trong form giữ nguyên [], không tạo tham số cá nhân hóa mới
  And thao tác Optimize không thêm review log hoặc thay đổi dữ liệu card/preset đã lưu
```

Text English xác định từ [ftl/core/deck-config.ftl:495][FTL495]:

> No reviews found. Make sure this preset is assigned to all decks (including subdecks) that you want to optimize, and try again.

Không tự dịch chuỗi rồi coi là localization chính thức tiếng Việt. `setTimeout(...,200)` là chi tiết lên lịch alert, **không** biến thành SLA phải xuất hiện trong đúng 200ms. Chờ thông báo bằng event/UI condition của harness.

## 5. Replacement TC-ANKI-035

**Type:** boundary, UI + internal backend contract. **Design:** Specified. **Status/Actual:** Not Run. **Priority:** giữ priority của catalog, không tự nâng.

| Bước | Dữ liệu/hành động | Expected quan sát được |
|---|---|---|
| 1 | Dựng F035-empty; mở lại Deck Options; chụp snapshot counts notes/cards/revlog, stored preset params và giá trị form. | Counts 0/0/0; params arrays rỗng; FSRS controls hiện; assignment guard false; Optimize khả dụng. |
| 2 | Bấm Optimize current preset một lần; ghi nhận request/response bằng harness nội bộ nếu có. | Request đúng fixture; response thành công `params=[]`, `fsrs_items=0`, optional health absent. Không trả `FsrsInsufficientData` do zero history. |
| 3 | Chờ alert bằng điều kiện xuất hiện, không dùng deadline sản phẩm tự đặt. | Alert khớp English FTL495; không có good-fit/bad-fit health message, không có thông báo “parameters currently optimal”. |
| 4 | Đóng alert; kiểm tra form và trạng thái nút sau promise hoàn tất. | Form params vẫn rỗng; computingParams đã false, nút trở lại Optimize. Không yêu cầu thấy animation/progress percentage vì nhánh return rất sớm. |
| 5 | So snapshot dữ liệu sau Optimize, trước bất kỳ Save hoặc hành động khác. | Không có note/card/revlog mới; stored preset params không đổi. Không assert toàn bộ DB byte-identical vì timing/cache không thuộc yêu cầu này. |

Nếu harness chỉ kiểm UI, không suy ra đã đo response field; ghi lớp backend riêng là Not Run cho đến khi quan sát nó. Có thể thực hiện bước2 trực tiếp qua service/Rust test trong fixture riêng để kiểm cấu trúc response, còn bước3–4 bắt buộc qua UI thật. Không dùng mock response để chứng minh backend thật.

**Nguồn tối thiểu cần thêm vào AC/TC JSON:**

```json
[
  {"path":"ts/routes/deck-options/FsrsOptions.svelte","line":200},
  {"path":"ts/routes/deck-options/FsrsOptions.svelte","line":225},
  {"path":"ts/routes/deck-options/FsrsOptions.svelte","line":235},
  {"path":"rslib/src/scheduler/service/mod.rs","line":264},
  {"path":"rslib/src/scheduler/fsrs/params.rs","line":95},
  {"path":"proto/anki/scheduler.proto","line":357},
  {"path":"ftl/core/deck-config.ftl","line":495}
]
```

**Bổ sung đề xuất vào BR-ANKI-014/SRS trước khi đồng bộ downstream:** “Khi Optimize current preset có 0 FSRS training item sau lọc lịch sử, trả nguyên tham số đầu vào, count0 và không có health result; UI báo không tìm thấy reviews. Không xem số raw revlog là số training item. Optimize current preset không đồng nghĩa Save and Optimize All.”

## 6. Nhánh/biên và positive alternatives

Các dòng sau là thiết kế mở rộng, chưa cấp ID AC/TC mới. Oracle zero-item áp dụng cho “không còn dữ liệu hợp lệ” ngoài collection trắng; không tự gộp tất cả thành cùng fixture.

| Biến thể | Fixture/guard cụ thể | Kết quả được source chứng minh |
|---|---|---|
| Health bật trên collection trắng | F035-empty, `health_check=true` | Vẫn return sớm count0, health absent, cùng no-reviews alert. Không phải health-check failed. [P95] |
| Params hiện hữu | Cùng zero items; đầu vào `current_params=P` với P là vector hợp lệ đang lưu, chụp trước request | Backend trả P nguyên vẹn sau biểu diễn protobuf f32, không reset default; UI so tới4 chữ số và không ghi vector mới. Không dùng float NaN/Infinity trong fixture. [P95], [U235] |
| Chỉ một lần học | Một card, đúng1 log Learning, rating3, interval1, timestamp cách next_day_at1ngày | Không có item để train → no-reviews. Test nguồn `single_learning_step_skipped_when_training` đã khẳng định converter trả None. [P802] |
| Chỉ lịch sử cùng ngày | Learning rating3 rồi Review rating3 trong cùng scheduler day; cả hai hợp lệ scheduling | `idx>=1` nhưng delta_t=0 nên không tạo item; count0 → cùng oracle. Đây là deduction trực tiếp từ guard, chưa có test runtime đã chạy. [P495] |
| Positive tối thiểu của converter | NEXT_DAY_AT=86400*1000 seconds; cùng card có Learning tại days_ago1, Review tại days_ago0; rating3, interval1 như helper nguồn | Converter tạo1 item với reviews `[(3,0),(3,1)]`; không đi zero-item return. Test `delta_t_is_correct` xác nhận cấu trúc. Không cam kết vector optimize cuối khác P hoặc giá trị số cố định: optimizer dependency và so sánh loss có thể giữ P. [P573], [P630], [P150] |
| Thiếu Learning | Chỉ Review/Relearning, không Learning trong nhóm sau reset | Training bỏ card; không nhầm với memory-state calculation (`training=false`). [P449], [P472], test [P766]. |
| Cutoff quanh Learning đầu | Learning L1 tại t, Learning L2 tại t+2ngày; giữ clock như helper; cutoff t−1ms, t, t+1ms | Trước/đúng t: không loại nhóm bởi cutoff; sau t: loại toàn card trong training. Source dùng `<`, test đã có boundary equal. [P449], [P814] |
| Suspended/search scope | Card duy nhất có Learning+Review hợp lệ nhưng suspended; custom search rỗng | Default `-is:suspended` loại card → count0. Nếu custom search chọn card đó, default exclusion không được tự thêm; converter có dữ liệu. [U81], [U192] |
| Health threshold khác Optimize threshold | 300 items vs301 items, health=true | Chỉ >300 mới thử time-series health check; <=300 health absent. Ngay cả >300, lỗi evaluate được chuyển thành None bởi `.ok()`. Đây không phải yêu cầu tối thiểu để bấm Optimize. [P182] |
| Chưa lưu assignment | Đổi preset assignment rồi bấm Optimize | UI alert `deck-config-please-save-your-changes-first`, return trước request; không dùng no-reviews oracle. [U200], [L165] |
| Optimize All | Bấm Save and Optimize, xác nhận | Luồng khác: `state.save(COMPUTE_ALL_PARAMS)` + reload; backend duyệt presets, healthfalse, gán response params vào config và cập nhật ngày optimize. Không áp no-reviews alert của current preset cho luồng này. [U348], [ALL363] |

**Test nguồn liên quan đã đọc, không chạy:** `delta_t_is_correct` [P630]; `card_ids_align_with_sorted_training_items` [P671] (5 review logs →3 training items); `cram_is_filtered` [P693]; `set_due_date_is_filtered` [P709]; `card_reset_drops_all_previous_history` [P729]; `single_learning_step_skipped_when_training` [P802]; cutoff test [P814]. Không tìm được test UI/compute_params trực tiếp cho alert zero history trong các test được tìm; oracle chính dựa vào nhánh Rust + UI rõ ràng, không tuyên bố regression test đã có hay đã pass.

## 7. Tài liệu khác biệt và giới hạn

1. Manual [deck-options.mdx:465][MAN465] nói optimizer cần “several reviews” và diễn đạt bấm Optimize sẽ tạo params. Mã có nhánh zero-item giữ nguyên và thông báo rõ. Đây là mô tả manual chưa đầy đủ cho biên, không căn cứ tạo lỗi thiếu dữ liệu.
2. FTL cũ [deck-config.ftl:603][FTL603] còn chuỗi nhắc1000+ reviews; comment Rust [params.rs:78][P78] nói không error nếu <400 items. Không lấy1000 hoặc400 làm guard của AC035. UI hiện tại dùng `weightsTooltip2`/`computeOptimalWeightsTooltip2` ([FsrsOptionsOuter:54][OUT54]), chuỗi mới [ftl:446][FTL446], không dùng hai tooltip cũ ở603/607. Cần ghi đây là khác biệt giữa chuỗi cũ còn trong repo và luồng hiện tại, không nói người dùng chắc chắn nhìn thấy tooltip1000.
3. `FsrsInsufficientData` ở export dataset [params.rs:228][P228] thuộc thao tác khác. Không chuyển mã lỗi đó sang ComputeFsrsParams.
4. “No reviews found” mô tả0 training items; không nhất thiết DB revlog trống. Filtering/cutoff/intraday có thể khiến raw history tồn tại mà vẫn no-reviews.
5. Code path zero-item không đi vào dependency optimizer. Vì vậy không cần suy đoán ngưỡng nội bộ thư viện để chốt case035. Positive training với dữ liệu >0 không có vector số oracle được chốt trong report này.

## 8. Câu hỏi chưa giải quyết

- Không còn câu hỏi chặn **thiết kế** case035 với F035-empty.
- QA vẫn cần dựng/chạy fixture, ghi môi trường và evidence để kết luận thực thi; hiện Not Run. Localized Vietnamese string chưa được xác minh; fixture English tránh khoảng trống này.
- Controller cần đồng bộ SRS/BR, qa-catalog, AC/TC và số liệu coverage; report này chỉ cung cấp replacement, không thực hiện các sửa đổi ngoài quyền sở hữu.

[P78]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L78
[P95]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L95
[P150]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L150
[P182]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L182
[P211]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L211
[P228]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L228
[P351]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L351
[P449]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L449
[P472]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L472
[P495]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L495
[P573]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L573
[P630]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L630
[P671]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L671
[P693]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L693
[P709]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L709
[P729]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L729
[P766]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L766
[P802]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L802
[P814]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L814
[U81]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L81
[U192]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L192
[U200]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L200
[U235]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L235
[U278]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L278
[U348]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L348
[U433]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L433
[OUT54]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptionsOuter.svelte#L54
[OUT115]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptionsOuter.svelte#L115
[L165]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/lib.ts#L165
[L278]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/lib.ts#L278
[L468]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/lib.ts#L468
[TS71]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/proto/typescript.rs#L71
[POST11]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/lib/generated/post.ts#L11
[M1213]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/mediasrv.py#L1213
[M1241]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/mediasrv.py#L1241
[M1273]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/mediasrv.py#L1273
[PY48]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/proto/python.rs#L48
[BE159]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/anki/_backend.py#L159
[RS49]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/rsbridge/lib.rs#L49
[RI141]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/rust_interface.rs#L141
[RI217]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/rust_interface.rs#L217
[PROTO357]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L357
[S264]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/service/mod.rs#L264
[DC77]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/deckconfig/mod.rs#L77
[FTL446]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ftl/core/deck-config.ftl#L446
[FTL495]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ftl/core/deck-config.ftl#L495
[FTL603]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ftl/core/deck-config.ftl#L603
[MAN465]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L465
[DC55]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/deckconfig/update.rs#L55
[DC96]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/deckconfig/update.rs#L96
[ALL363]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/deckconfig/update.rs#L363

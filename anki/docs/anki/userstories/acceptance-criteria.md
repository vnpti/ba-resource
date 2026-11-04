---
id: DOC-AC-ANKI-001
title: "Acceptance Criteria Anki Desktop — As-Is"
version: "1.0.1"
phase: Acceptance
domain: Anki
tags: [anki, as-is, reconstructed, qa, draft]
depends_on: ["DOC-SRS-ANKI-001", "DOC-US-ANKI-001"]
related_diagrams: []
author: BA Agent
last_updated: "2026-11-03"
status: draft
---

# Acceptance Criteria Anki Desktop — As-Is

## Lịch sử sửa đổi

| Phiên bản | Ngày | Tác giả | Nội dung |
|---|---|---|---|
| 1.0.1 | 2026-11-03 | BA Analysis | Làm rõ oracle035/067/072/077 và truy vết liên quan; không thay source hoặc kết quả chạy |
| 1.0.0 | 2026-11-02 | BA Agent | Tái lập As-Is từ SRS v1.0.0; Draft, chưa phê duyệt, chưa thực thi kiểm thử. |

Nguồn: [SRS](../srs/spec.md) và [index yêu cầu](../srs/requirements.json) v1.0.1; [backlog](backlog.md) DOC-US-ANKI-001 v1.0.1. Đây là oracle thiết kế tái lập từ code/manual, **Draft**, chưa phê duyệt. ERR-ANKI-000-xx là nhãn BA, không phải mã HTTP/response thực. “Negative” có thể là hành động không tạo hiệu ứng hoặc điều kiện bị loại; không tự thêm lỗi UI.

## Quy ước kiểm thử

Mỗi scenario dùng collection/profile tạm độc lập, dữ liệu tổng hợp và auto-sync tắt, trừ sync test dùng server cô lập. Clock mặc định t0 là 2026-11-02T00:00:00Z được harness điều khiển; case có clock riêng như AC-ANKI-067 dùng giá trị tại Given; múi giờ và rollover scheduler được ghi rõ, không mặc định nửa đêm máy. Mtime có độ phân giải giây, revlog có định danh/thời gian theo source; không dùng sleep thay clock. Các dòng có nhiều tổ hợp phải chạy từng tổ hợp trên snapshot mới. Không cố định interval tùy ý khi fuzz/FSRS phụ thuộc fixture; ghi next state/seed/input và so nhánh hoặc invariant được nguồn bảo đảm.

Bản cập nhật 1.0.1 có 86/86 scenario Design: Specified. Bốn oracle035/067/072/077 đã được chốt từ source với fixture giới hạn rõ; không biến nguồn tĩnh thành approval hoặc kết quả thực thi. Nếu môi trường chưa đáp ứng fixture thì ghi blocker thực thi, không đổi expected hoặc đánh Pass. Không chạy thao tác phá dữ liệu trên profile thật.

## AC-ANKI-001 — Lưu note hai chiều

Nguồn: **US-ANKI-01** · FR: FR-CNT-NOTE-001 · BR: BR-ANKI-001, BR-ANKI-003 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95).

```gherkin
Scenario: AC-ANKI-001 — Lưu note hai chiều
  Given collection tạm có NoteType BasicQA gồm Front/Back và hai template hợp lệ; Front=apple, Back=quả táo; deck QA
  When thêm note và đọc note/card đã lưu
  Then một note giữ hai field; hai card có cùng note_id và ordinal khác nhau, mỗi card có lịch riêng
```

## AC-ANKI-002 — Sai số field

Nguồn: **US-ANKI-01** · FR: FR-CNT-NOTE-001 · BR: BR-ANKI-001 · ERR: ERR-ANKI-000-01. Loại: **negative**. Design: **Specified**; approval: Draft.

[rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95); [rslib/src/notes/mod.rs:198](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L198).

```gherkin
Scenario: AC-ANKI-002 — Sai số field
  Given NoteType có hai field; note thử chỉ có một field apple; đã chụp số note/card
  When gọi đường lưu note của backend
  Then guard từ chối ERR-ANKI-000-01; note thử không được lưu thành note hợp lệ; không gán HTTP/UI message
```

## AC-ANKI-003 — Chỉ thêm ordinal còn thiếu

Nguồn: **US-ANKI-01** · FR: FR-CNT-NOTE-001 · BR: BR-ANKI-003 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95).

```gherkin
Scenario: AC-ANKI-003 — Chỉ thêm ordinal còn thiếu
  Given note N có card ordinal 0 và lịch đã học; template ordinal 1 trước rỗng, nay Back được điền quả táo
  When lưu note rồi lưu lại cùng nội dung lần nữa
  Then ordinal 1 được thêm đúng một card; ordinal 0 giữ card ID và lịch; lần lưu lặp không tạo card cùng ordinal
```

## AC-ANKI-004 — Card rỗng và fallback cấp lõi

Nguồn: **US-ANKI-01** · FR: FR-CNT-NOTE-001 · BR: BR-ANKI-003 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95); [docs-site/manual/templates/generation.mdx:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/templates/generation.mdx#L25).

```gherkin
Scenario: AC-ANKI-004 — Card rỗng và fallback cấp lõi
  Given hai fixture riêng: A có card đã học rồi xóa field làm mặt hỏi rỗng; B chưa có card, mọi template rỗng và ensure_not_empty=true
  When lưu A và chạy sinh card cấp lõi B
  Then A không bị tự xóa card cũ; B sinh ordinal 0; không suy ra mọi caller UI bật ensure_not_empty
```

## AC-ANKI-005 — NoteType tối thiểu hợp lệ

Nguồn: **US-ANKI-02** · FR: FR-CNT-TYPE-001 · BR: BR-ANKI-002, BR-ANKI-003 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[rslib/src/notetype/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/mod.rs#L484); [proto/anki/notetypes.proto:102](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/notetypes.proto#L102); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95).

```gherkin
Scenario: AC-ANKI-005 — NoteType tối thiểu hợp lệ
  Given collection tạm chưa có loại QA-Min; tên QA-Min, một field Front, một template hỏi {{Front}} và đáp án {{Front}}
  When thêm NoteType rồi tạo note Front=alpha
  Then NoteType được lưu với một field/một template; note sinh card phù hợp
```

## AC-ANKI-006 — Thiếu cấu trúc bắt buộc

Nguồn: **US-ANKI-02** · FR: FR-CNT-TYPE-001 · BR: BR-ANKI-002 · ERR: ERR-ANKI-000-02. Loại: **negative**. Design: **Specified**; approval: Draft.

[rslib/src/notetype/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/mod.rs#L484); [proto/anki/notetypes.proto:102](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/notetypes.proto#L102).

```gherkin
Scenario: AC-ANKI-006 — Thiếu cấu trúc bắt buộc
  Given ba fixture NoteType độc lập: không field; không template; tên rỗng tại guard sau bước chuẩn hóa; không dùng UI để suy đoán thông báo
  When gọi validation/lưu tại đúng guard của từng fixture
  Then cả ba bị từ chối theo ERR-ANKI-000-02; ghi guard thực tế, không áp mã HTTP
```

## AC-ANKI-007 — Template override deck

Nguồn: **US-ANKI-02** · FR: FR-CNT-TYPE-001 · BR: BR-ANKI-003 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/notetype/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/mod.rs#L484); [proto/anki/notetypes.proto:102](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/notetypes.proto#L102); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95); [rslib/src/notetype/cardgen.rs:141](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L141).

```gherkin
Scenario: AC-ANKI-007 — Template override deck
  Given note có hai template đều render hỏi; deck chọn QA-A; riêng template 1 override QA-B
  When sinh card cho note
  Then card template 0 ở QA-A, template 1 ở QA-B; một note không buộc các card cùng deck
```

## AC-ANKI-008 — Hai số cloze tạo hai card

Nguồn: **US-ANKI-03** · FR: FR-CNT-CLOZ-001 · BR: BR-ANKI-001, BR-ANKI-004 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[rslib/src/notetype/cardgen.rs:160](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L160); [docs-site/manual/editing.mdx:364](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L364); [rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194).

```gherkin
Scenario: AC-ANKI-008 — Hai số cloze tạo hai card
  Given Cloze NoteType đúng số field; Text={{c1::alpha}} và {{c2::beta}}
  When thêm note cloze
  Then một note tạo hai card tương ứng c1/c2; cùng dùng template cloze đầu tiên
```

## AC-ANKI-009 — Cloze không bỏ qua field guard

Nguồn: **US-ANKI-03** · FR: FR-CNT-CLOZ-001 · BR: BR-ANKI-001 · ERR: ERR-ANKI-000-01. Loại: **negative**. Design: **Specified**; approval: Draft.

[rslib/src/notetype/cardgen.rs:160](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L160); [docs-site/manual/editing.mdx:364](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L364); [rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194); [rslib/src/notes/mod.rs:198](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L198).

```gherkin
Scenario: AC-ANKI-009 — Cloze không bỏ qua field guard
  Given Cloze NoteType có hai field; note cloze thử có một field chứa {{c1::alpha}}
  When gọi lưu note qua backend
  Then guard ERR-ANKI-000-01 từ chối note có số field sai dù chuỗi cloze hợp lệ
```

## AC-ANKI-010 — Nhiều đoạn cùng số

Nguồn: **US-ANKI-03** · FR: FR-CNT-CLOZ-001 · BR: BR-ANKI-004 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/notetype/cardgen.rs:160](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L160); [docs-site/manual/editing.mdx:364](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L364).

```gherkin
Scenario: AC-ANKI-010 — Nhiều đoạn cùng số
  Given Text={{c1::alpha}} và {{c1::beta}}; các field khác đủ theo NoteType
  When thêm note rồi xem card được sinh
  Then chỉ một card cho c1; khi hiện câu hỏi cả hai đoạn c1 được che cùng lượt
```

## AC-ANKI-011 — Hai vùng che riêng

Nguồn: **US-ANKI-04** · FR: FR-CNT-IMGO-001 · BR: BR-ANKI-005 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[rslib/src/image_occlusion/notetype.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/image_occlusion/notetype.rs#L59); [docs-site/manual/editing.mdx:504](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L504).

```gherkin
Scenario: AC-ANKI-011 — Hai vùng che riêng
  Given ảnh QA.png tự tạo không dữ liệu cá nhân; hai shape che hai vùng, không group
  When lưu note Image Occlusion
  Then một note dùng cấu trúc cloze/image occlusion, sinh card theo hai vùng được đánh số riêng
```

## AC-ANKI-012 — Xóa shape không tự xóa card

Nguồn: **US-ANKI-04** · FR: FR-CNT-IMGO-001 · BR: BR-ANKI-003, BR-ANKI-005 · ERR: —. Loại: **negative**. Design: **Specified**; approval: Draft.

[rslib/src/image_occlusion/notetype.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/image_occlusion/notetype.rs#L59); [docs-site/manual/editing.mdx:504](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L504); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95); [docs-site/manual/editing.mdx:531](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L531).

```gherkin
Scenario: AC-ANKI-012 — Xóa shape không tự xóa card
  Given note Image Occlusion có hai shape và hai card; card thứ hai đã có lịch
  When xóa shape thứ hai rồi lưu và mở Empty Cards để kiểm tra, chưa xác nhận xóa
  Then card cũ tương ứng không tự bị xóa; Empty Cards cho phép nhận diện card không còn nội dung che
```

## AC-ANKI-013 — Overlay không tăng số card

Nguồn: **US-ANKI-04** · FR: FR-CNT-IMGO-001 · BR: BR-ANKI-005 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/image_occlusion/notetype.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/image_occlusion/notetype.rs#L59); [docs-site/manual/editing.mdx:504](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L504); [docs-site/manual/editing.mdx:531](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L531).

```gherkin
Scenario: AC-ANKI-013 — Overlay không tăng số card
  Given note ảnh có một shape và một card; thêm text overlay QA label
  When lưu lại note
  Then vẫn một card do shape; overlay hiển thị nội dung, không sinh card bổ sung
```

## AC-ANKI-014 — Deck cha gồm descendants

Nguồn: **US-ANKI-05** · FR: FR-ORG-DECK-001 · BR: BR-ANKI-006, BR-ANKI-012 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[docs-site/manual/getting-started.mdx:75](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/getting-started.mdx#L75); [rslib/src/scheduler/queue/builder/mod.rs:135](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/mod.rs#L135); [docs-site/manual/studying.mdx:10](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L10); [rslib/src/decks/limits.rs:98](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/decks/limits.rs#L98).

```gherkin
Scenario: AC-ANKI-014 — Deck cha gồm descendants
  Given QA-Parent có card A; QA-Parent::Child có B; QA-Other có C; cả ba đủ hạn, limit đủ và không bury
  When chọn QA-Parent và xây queue
  Then phạm vi lấy A và B; C không thuộc deck được chọn hoặc descendants
```

## AC-ANKI-015 — Không kéo sibling ngoài phạm vi

Nguồn: **US-ANKI-05** · FR: FR-ORG-DECK-001 · BR: BR-ANKI-006 · ERR: —. Loại: **negative**. Design: **Specified**; approval: Draft.

[docs-site/manual/getting-started.mdx:75](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/getting-started.mdx#L75); [rslib/src/scheduler/queue/builder/mod.rs:135](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/mod.rs#L135); [docs-site/manual/studying.mdx:10](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L10).

```gherkin
Scenario: AC-ANKI-015 — Không kéo sibling ngoài phạm vi
  Given hai card A/B chung note; A ở QA-Selected, B ở QA-Other; cả hai đủ hạn, bury siblings tắt
  When chọn học QA-Selected
  Then B không vào phạm vi chỉ vì có chung note với A; note không có một deck owner chung
```

## AC-ANKI-016 — Chuyển một sibling

Nguồn: **US-ANKI-05** · FR: FR-ORG-DECK-001 · BR: BR-ANKI-006 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[docs-site/manual/getting-started.mdx:75](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/getting-started.mdx#L75); [rslib/src/scheduler/queue/builder/mod.rs:135](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/mod.rs#L135); [docs-site/manual/studying.mdx:10](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L10); [docs-site/manual/editing.mdx:217](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L217).

```gherkin
Scenario: AC-ANKI-016 — Chuyển một sibling
  Given note N có card A/B cùng QA-A; queue chưa xây; QA-B tồn tại
  When chuyển riêng A sang QA-B rồi đọc cả hai card
  Then A thuộc QA-B và B vẫn thuộc QA-A; cùng giữ note_id N
```

## AC-ANKI-017 — Tìm nội dung field

Nguồn: **US-ANKI-06** · FR: FR-ORG-SRCH-001 · BR: BR-ANKI-007 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226).

```gherkin
Scenario: AC-ANKI-017 — Tìm nội dung field
  Given N1 có Front=alpha, N2 có Front=beta; không field nào khác chứa alpha
  When tìm alpha trong Browse chế độ Cards
  Then kết quả là các card của N1; không có card N2
```

## AC-ANKI-018 — Text thường không tìm tag

Nguồn: **US-ANKI-06** · FR: FR-ORG-SRCH-001 · BR: BR-ANKI-007 · ERR: —. Loại: **negative**. Design: **Specified**; approval: Draft.

[docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226).

```gherkin
Scenario: AC-ANKI-018 — Text thường không tìm tag
  Given N1 có tag=needle nhưng field chỉ alpha; N2 có field=needle nhưng không tag đó
  When tìm needle rồi tìm tag:needle trong Browse, dùng snapshot kết quả riêng
  Then query needle trả card N2, không N1; query tag:needle trả card N1
```

## AC-ANKI-019 — Kết hợp toán tử

Nguồn: **US-ANKI-06** · FR: FR-ORG-SRCH-001 · BR: BR-ANKI-007 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226).

```gherkin
Scenario: AC-ANKI-019 — Kết hợp toán tử
  Given ba note: N1 field alpha và tag qa; N2 field beta và tag qa; N3 field beta không tag qa
  When tìm (alpha or beta) tag:qa rồi tìm cùng biểu thức với -tag:qa
  Then truy vấn đầu trả card N1/N2; truy vấn sau chỉ trả card N3; AND/OR/NOT giữ phạm vi đã mô tả
```

## AC-ANKI-020 — Answer sau khi xem đáp án

Nguồn: **US-ANKI-07** · FR: FR-LRN-REV-001 · BR: BR-ANKI-006, BR-ANKI-008, BR-ANKI-011 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[docs-site/manual/studying.mdx:40](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L40); [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315); [docs-site/manual/studying.mdx:10](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L10); [docs-site/manual/studying.mdx:58](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L58).

```gherkin
Scenario: AC-ANKI-020 — Answer sau khi xem đáp án
  Given một card Review tới hạn ở QA; đã ghi current state, reps/lapses, revlog count và deck stats; clock=t0; không addon
  When Study Now, Show Answer rồi chọn Good một lần
  Then answer hợp lệ commit trạng thái card, một revlog và deck stats tương ứng; Good là phản hồi nhớ được, không xác minh hiểu biết thực tế
```

## AC-ANKI-021 — Current state đã thay đổi

Nguồn: **US-ANKI-07** · FR: FR-LRN-REV-001 · BR: BR-ANKI-011 · ERR: ERR-ANKI-000-03. Loại: **negative**. Design: **Specified**; approval: Draft.

[docs-site/manual/studying.mdx:40](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L40); [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315); [rslib/src/scheduler/answering/mod.rs:335](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L335).

```gherkin
Scenario: AC-ANKI-021 — Current state đã thay đổi
  Given đã lấy current state S của card; sửa trạng thái nền khiến current state thật khác S ngoài elapsed seconds; chụp lại card/log/stats sau sửa
  When gửi AnswerCard dựa trên S
  Then ERR-ANKI-000-03; không thêm revlog hoặc cập nhật card/stats do answer bị từ chối; thay đổi hợp lệ trước answer vẫn còn
```

## AC-ANKI-022 — Chưa xem đáp án

Nguồn: **US-ANKI-07** · FR: FR-LRN-REV-001 · BR: BR-ANKI-008 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[docs-site/manual/studying.mdx:40](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L40); [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315); [docs-site/manual/studying.mdx:58](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L58); [qt/aqt/reviewer.py:532](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/reviewer.py#L532).

```gherkin
Scenario: AC-ANKI-022 — Chưa xem đáp án
  Given reviewer đang ở question của card QA, chưa Show Answer; chụp revlog count và card state
  When gửi thao tác rating qua reviewer trước khi vào trạng thái answer
  Then reviewer bỏ qua thao tác; không gửi answer hợp lệ và không tạo revlog cho lần nhấn này
```

## AC-ANKI-023 — Cap thời gian answer

Nguồn: **US-ANKI-07** · FR: FR-LRN-REV-001 · BR: BR-ANKI-011 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[docs-site/manual/studying.mdx:40](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L40); [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315); [rslib/src/scheduler/answering/mod.rs:330](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L330).

```gherkin
Scenario: AC-ANKI-023 — Cap thời gian answer
  Given preset cap_answer_time_to_secs=60; ba bản sao card độc lập có elapsed answer 59, 60, 61 giây; đã hiện đáp án
  When gửi Good trên mỗi fixture bằng clock kiểm soát
  Then revlog lưu thời gian tương ứng 59, 60, 60 giây; không lưu vượt cap 60
```

## AC-ANKI-024 — Learning theo bốn rating

Nguồn: **US-ANKI-08** · FR: FR-LRN-SCH-001 · BR: BR-ANKI-009, BR-ANKI-013 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[proto/anki/scheduler.proto:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L80); [rslib/src/scheduler/states/review.rs:64](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L64); [rslib/src/scheduler/states/learning.rs:39](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/learning.rs#L39); [rslib/src/scheduler/answering/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L484); [rslib/src/scheduler/states/steps.rs:38](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/steps.rs#L38).

```gherkin
Scenario: AC-ANKI-024 — Learning theo bốn rating
  Given learning steps [1m,10m], legacy, card ở bước đầu; dùng bốn bản sao độc lập cùng cấu hình
  When tính next states rồi chọn lần lượt Again, Hard, Good, Easy trên từng bản sao
  Then Again về bước đầu; Hard dùng trung bình hai bước đầu; Good tiến bước; Easy sang Review; không khẳng định due số học nếu fuzz được áp dụng
```

## AC-ANKI-025 — Quên Review và Again khi học lại

Nguồn: **US-ANKI-08** · FR: FR-LRN-SCH-001 · BR: BR-ANKI-010 · ERR: —. Loại: **negative**. Design: **Specified**; approval: Draft.

[proto/anki/scheduler.proto:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L80); [rslib/src/scheduler/states/review.rs:64](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L64); [rslib/src/scheduler/states/review.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L95).

```gherkin
Scenario: AC-ANKI-025 — Quên Review và Again khi học lại
  Given card Review lapse=2, relearning steps [1m,10m], chưa leech; clock kiểm soát
  When chọn Again ở Review rồi Again trong Relearning
  Then lapse tăng thành 3 ở thất bại Review; tiếp tục bằng 3 khi Again trong cùng chuỗi Relearning
```

## AC-ANKI-026 — Hard với một learning step

Nguồn: **US-ANKI-08** · FR: FR-LRN-SCH-001 · BR: BR-ANKI-009 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[proto/anki/scheduler.proto:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L80); [rslib/src/scheduler/states/review.rs:64](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L64); [rslib/src/scheduler/states/learning.rs:39](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/learning.rs#L39); [rslib/src/scheduler/states/steps.rs:55](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/steps.rs#L55).

```gherkin
Scenario: AC-ANKI-026 — Hard với một learning step
  Given legacy learning có đúng một step 10 phút; card tại bước đầu; lấy trạng thái tính toán trước fuzz nếu có
  When tính Hard next state
  Then hard delay cơ sở là 15 phút theo 1,5 lần step; không áp công thức trung bình hai step không tồn tại
```

## AC-ANKI-027 — Reject state lỗi trước xếp lịch

Nguồn: **US-ANKI-08** · FR: FR-LRN-SCH-001 · BR: BR-ANKI-010, BR-ANKI-011 · ERR: ERR-ANKI-000-03. Loại: **negative**. Design: **Specified**; approval: Draft.

[proto/anki/scheduler.proto:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L80); [rslib/src/scheduler/states/review.rs:64](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L64); [rslib/src/scheduler/states/review.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L95); [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315); [rslib/src/scheduler/answering/mod.rs:335](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L335).

```gherkin
Scenario: AC-ANKI-027 — Reject state lỗi trước xếp lịch
  Given card Review đã được thay current state thực sau khi UI nhận S; không chỉ chênh elapsed seconds
  When gửi Again với current state S
  Then ERR-ANKI-000-03; không tăng lapse, không ghi revlog hoặc lịch mới từ answer này
```

## AC-ANKI-028 — Ưu tiên today, deck, preset

Nguồn: **US-ANKI-09** · FR: FR-LRN-LIM-001 · BR: BR-ANKI-012 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[rslib/src/decks/limits.rs:98](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/decks/limits.rs#L98); [rslib/src/scheduler/queue/builder/gathering.rs:23](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/gathering.rs#L23).

```gherkin
Scenario: AC-ANKI-028 — Ưu tiên today, deck, preset
  Given preset new limit=20, deck limit=10, today override=3, đã học new=1; review limit dư; có 30 new đủ điều kiện
  When xây queue hôm nay
  Then còn tối đa 2 new theo today override; không chọn mức 10 hoặc 20
```

## AC-ANKI-029 — Review limit bằng không

Nguồn: **US-ANKI-09** · FR: FR-LRN-LIM-001 · BR: BR-ANKI-012 · ERR: —. Loại: **negative**. Design: **Specified**; approval: Draft.

[rslib/src/decks/limits.rs:98](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/decks/limits.rs#L98); [rslib/src/scheduler/queue/builder/gathering.rs:23](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/gathering.rs#L23).

```gherkin
Scenario: AC-ANKI-029 — Review limit bằng không
  Given hai collection giống nhau có new và due review; review remaining=0, new remaining=5; một tắt và một bật New cards ignore review limit
  When xây queue ở từng collection
  Then khi tắt không lấy thêm new do review limit; khi bật có thể lấy new tới new remaining, review vẫn bị chặn
```

## AC-ANKI-030 — Intraday khác interday

Nguồn: **US-ANKI-09** · FR: FR-LRN-LIM-001 · BR: BR-ANKI-012 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/decks/limits.rs:98](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/decks/limits.rs#L98); [rslib/src/scheduler/queue/builder/gathering.rs:23](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/gathering.rs#L23).

```gherkin
Scenario: AC-ANKI-030 — Intraday khác interday
  Given review remaining=0; có một intraday learning đã đến giờ và một interday learning đã tới ngày; không giới hạn khác
  When xây queue tại clock t0
  Then intraday vẫn đủ điều kiện; interday chịu review limit và không được lấy trong fixture này
```

## AC-ANKI-031 — Giới hạn cây deck

Nguồn: **US-ANKI-09** · FR: FR-LRN-LIM-001 · BR: BR-ANKI-006, BR-ANKI-012 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/decks/limits.rs:98](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/decks/limits.rs#L98); [rslib/src/scheduler/queue/builder/gathering.rs:23](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/gathering.rs#L23); [docs-site/manual/studying.mdx:10](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L10); [rslib/src/scheduler/queue/builder/mod.rs:130](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/mod.rs#L130).

```gherkin
Scenario: AC-ANKI-031 — Giới hạn cây deck
  Given QA-P limit tổng=3; QA-P::A limit=2 và QA-P::B limit=2; mỗi con có 4 card đủ điều kiện; các counts bằng 0
  When chọn QA-P xây queue; lặp trên fixture mới với card count đã học bằng limit
  Then tổng các con không vượt 3 và từng con không vượt 2; khi đã học đúng limit không còn quota tương ứng; kiểm riêng cờ Limits start from top khi chọn con
```

## AC-ANKI-032 — FSRS ở phạm vi collection

Nguồn: **US-ANKI-10** · FR: FR-LRN-FSRS-001 · BR: BR-ANKI-013, BR-ANKI-014 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[rslib/src/scheduler/answering/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L484); [docs-site/manual/deck-options.mdx:406](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L406); [docs-site/manual/deck-options.mdx:500](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L500).

```gherkin
Scenario: AC-ANKI-032 — FSRS ở phạm vi collection
  Given hai deck dùng hai preset trong cùng collection; có lịch sử nhân tạo; cấu hình retention/params hợp lệ
  When bật FSRS và đọc cấu hình cùng next states của card thuộc cả hai preset
  Then cờ bật áp dụng toàn collection; next states theo nhánh FSRS dùng memory state/retention/params, không còn diễn giải bằng công thức ease SM-2
```

## AC-ANKI-033 — Không reschedule khi tùy chọn tắt

Nguồn: **US-ANKI-10** · FR: FR-LRN-FSRS-001 · BR: BR-ANKI-014 · ERR: —. Loại: **negative**. Design: **Specified**; approval: Draft.

[rslib/src/scheduler/answering/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L484); [docs-site/manual/deck-options.mdx:406](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L406); [docs-site/manual/deck-options.mdx:500](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L500).

```gherkin
Scenario: AC-ANKI-033 — Không reschedule khi tùy chọn tắt
  Given FSRS đang bật; card đã có due D; dùng bản sao collection và chụp due trước sửa; reschedule on change tắt
  When đổi desired retention hợp lệ rồi lưu mà không học card
  Then không tự tính lại toàn bộ due cũ; card fixture giữ D do thao tác đổi cấu hình này
```

## AC-ANKI-034 — Reschedule là lựa chọn riêng

Nguồn: **US-ANKI-10** · FR: FR-LRN-FSRS-001 · BR: BR-ANKI-014 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/scheduler/answering/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L484); [docs-site/manual/deck-options.mdx:406](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L406); [docs-site/manual/deck-options.mdx:500](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L500).

```gherkin
Scenario: AC-ANKI-034 — Reschedule là lựa chọn riêng
  Given hai bản sao cùng card/history và cấu hình; cùng thay retention; một bật và một tắt reschedule on change
  When lưu cấu hình ở từng bản sao rồi kiểm tra tác vụ reschedule và due
  Then nhánh bật thực hiện tính lại lịch cho scope bị ảnh hưởng; nhánh tắt không thực hiện đợt reschedule; không bắt buộc mọi card đều có ngày mới khác ngày cũ
```

## AC-ANKI-035 — Optimize không có lịch sử giữ nguyên tham số

Nguồn: **US-ANKI-10** · FR: FR-LRN-FSRS-001 · BR: BR-ANKI-014 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[ts/routes/deck-options/FsrsOptions.svelte:200](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L200); [ts/routes/deck-options/FsrsOptions.svelte:225](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L225); [ts/routes/deck-options/FsrsOptions.svelte:235](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L235); [rslib/src/scheduler/service/mod.rs:264](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/service/mod.rs#L264); [rslib/src/scheduler/fsrs/params.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L95); [proto/anki/scheduler.proto:357](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L357); [ftl/core/deck-config.ftl:495](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ftl/core/deck-config.ftl#L495).

```gherkin
Scenario: AC-ANKI-035 — Optimize không có lịch sử giữ nguyên tham số
  Given collection tạm F035-empty có 0 note/card/revlog; deck D035 dùng preset P035 đã lưu, FSRS bật, fsrs_params_4/5/6 đều []; search và ignore-before date rỗng, relearnSteps=[10], healthCheck=false, reschedule=false; mở lại Deck Options, không có assignment chưa lưu hoặc tác vụ đang chạy
  When bấm Optimize current preset một lần và chờ request cùng thông báo hoàn tất, chưa bấm Save hoặc Optimize All
  Then backend trả thành công params=[], fsrs_items=0, health_check_passed absent (không phải false); UI hiện khóa deck-config-fsrs-params-no-reviews; tham số form và preset đã lưu không đổi, counts note/card/revlog vẫn 0/0/0; computingParams trở về false
```

**Giới hạn oracle:** 0 training item là nhánh return sớm, không phải lỗi thiếu 400/1000 reviews và không có mô hình cá nhân hóa mới. Không áp oracle này cho Optimize All hoặc preset assignment chưa lưu. Nếu chỉ quan sát UI thì lớp response backend vẫn chưa được kiểm thử. Source tĩnh, chưa chạy test.

## AC-ANKI-036 — Bury và unbury thủ công

Nguồn: **US-ANKI-11** · FR: FR-LRN-HIDE-001 · BR: BR-ANKI-015 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[rslib/src/scheduler/bury_and_suspend.rs:32](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L32); [rslib/src/scheduler/answering/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L194).

```gherkin
Scenario: AC-ANKI-036 — Bury và unbury thủ công
  Given card A đang Review đủ hạn, có interval/lapse đã chụp, chưa suspended
  When bury A rồi unbury thủ công
  Then A rời queue khi buried rồi có thể trở lại theo due/limit sau unbury; interval/lapse nền không bị biến thành một giai đoạn trí nhớ mới
```

## AC-ANKI-037 — Không bury card suspended

Nguồn: **US-ANKI-11** · FR: FR-LRN-HIDE-001 · BR: BR-ANKI-015 · ERR: —. Loại: **negative**. Design: **Specified**; approval: Draft.

[rslib/src/scheduler/bury_and_suspend.rs:32](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L32); [rslib/src/scheduler/answering/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L194).

```gherkin
Scenario: AC-ANKI-037 — Không bury card suspended
  Given card A đã suspended; ghi queue và lịch nền
  When gọi bury A rồi xây queue
  Then A vẫn suspended và không được biến thành buried; không được đưa lại vào queue
```

## AC-ANKI-038 — Rollover khác ngày lịch máy

Nguồn: **US-ANKI-11** · FR: FR-LRN-HIDE-001 · BR: BR-ANKI-015 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/scheduler/bury_and_suspend.rs:32](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L32); [rslib/src/scheduler/answering/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L194).

```gherkin
Scenario: AC-ANKI-038 — Rollover khác ngày lịch máy
  Given A buried, B suspended; clock scheduler có rollover R xác định; ba bản sao ở R−1s, R, R+1s
  When mở/xây lại queue để scheduler chạy xử lý ngày tại từng mốc
  Then trước R A còn buried; tại/sau R A được unbury theo ngày scheduler; B vẫn suspended ở cả ba mốc
```

## AC-ANKI-039 — Mốc leech dương và bằng không

Nguồn: **US-ANKI-11** · FR: FR-LRN-HIDE-001 · BR: BR-ANKI-016 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/scheduler/bury_and_suspend.rs:32](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L32); [rslib/src/scheduler/answering/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L194); [rslib/src/scheduler/states/review.rs:292](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L292).

```gherkin
Scenario: AC-ANKI-039 — Mốc leech dương và bằng không
  Given fixture ngưỡng 8 có lapse sau answer lần lượt 7,8,9,11,12; fixture khác threshold=0; action Tag Only; dùng bản sao độc lập
  When tính trạng thái leech sau Review Again và commit answer khi phù hợp
  Then phát leech ở 8 và 12, không phát mới ở 7/9/11; threshold=0 không kích hoạt; tag leech thuộc note; không tự xóa tag cũ khi không phát mới
```

## AC-ANKI-040 — Tag only khác Suspend

Nguồn: **US-ANKI-11** · FR: FR-LRN-HIDE-001 · BR: BR-ANKI-016 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/scheduler/bury_and_suspend.rs:32](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L32); [rslib/src/scheduler/answering/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L194); [rslib/src/scheduler/states/review.rs:292](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L292).

```gherkin
Scenario: AC-ANKI-040 — Tag only khác Suspend
  Given hai bản sao note có siblings A/B; A đang Review, lapse sắp chạm threshold; một action Tag Only, một action Suspend
  When trả lời Again cho A tại threshold
  Then cả hai note có tag leech; Tag Only không suspend A, Suspend làm A suspended; không tự suy ra sibling B cũng suspended
```

## AC-ANKI-041 — Build rồi Empty không copy card

Nguồn: **US-ANKI-12** · FR: FR-LRN-FILT-001 · BR: BR-ANKI-017 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[rslib/src/scheduler/filtered/mod.rs:123](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L123); [rslib/src/scheduler/states/preview_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/preview_filter.rs#L25).

```gherkin
Scenario: AC-ANKI-041 — Build rồi Empty không copy card
  Given QA-Home có hai card hợp query tag:qa; filtered QA-F có limit=2; chụp card IDs
  When Build QA-F rồi Empty
  Then hai card tạm thuộc QA-F và giữ home deck; Empty trả về QA-Home với cùng IDs, không xóa hoặc tạo bản sao
```

## AC-ANKI-042 — Không có card được phép lấy

Nguồn: **US-ANKI-12** · FR: FR-LRN-FILT-001 · BR: BR-ANKI-017 · ERR: ERR-ANKI-000-04. Loại: **negative**. Design: **Specified**; approval: Draft.

[rslib/src/scheduler/filtered/mod.rs:123](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L123); [rslib/src/scheduler/states/preview_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/preview_filter.rs#L25); [rslib/src/scheduler/filtered/mod.rs:178](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L178).

```gherkin
Scenario: AC-ANKI-042 — Không có card được phép lấy
  Given query tag:qa chỉ khớp card suspended, buried hoặc đã thuộc filtered khác; allow_empty=false
  When Build filtered mới
  Then trả ERR-ANKI-000-04 / SearchReturnedNoCards; không lấy các card bị loại để làm đầy filtered
```

## AC-ANKI-043 — Limit một và Rebuild

Nguồn: **US-ANKI-12** · FR: FR-LRN-FILT-001 · BR: BR-ANKI-017 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/scheduler/filtered/mod.rs:123](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L123); [rslib/src/scheduler/states/preview_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/preview_filter.rs#L25).

```gherkin
Scenario: AC-ANKI-043 — Limit một và Rebuild
  Given QA-F limit=1 có card cũ A; search mới chỉ khớp B/C, order xác định đưa B trước C
  When Rebuild QA-F
  Then A được trả home; chỉ B vào QA-F, C không được lấy vượt limit; toàn collection không tăng card count
```

## AC-ANKI-044 — Reschedule dùng home deck

Nguồn: **US-ANKI-12** · FR: FR-LRN-FILT-001 · BR: BR-ANKI-018 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[rslib/src/scheduler/filtered/mod.rs:123](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L123); [rslib/src/scheduler/states/preview_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/preview_filter.rs#L25); [rslib/src/scheduler/states/rescheduling_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/rescheduling_filter.rs#L25).

```gherkin
Scenario: AC-ANKI-044 — Reschedule dùng home deck
  Given filtered bật reschedule; home deck có preset P; hai bản sao card Review: Good về Review, Again vào Relearning có steps
  When trả lời trên từng bản sao theo next states từ home preset
  Then Good chuyển Review và trả home; Again ở Relearning còn trong filtered; lịch thay đổi theo home settings
```

## AC-ANKI-045 — Preview delay bằng không

Nguồn: **US-ANKI-12** · FR: FR-LRN-FILT-001 · BR: BR-ANKI-019 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/scheduler/filtered/mod.rs:123](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L123); [rslib/src/scheduler/states/preview_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/preview_filter.rs#L25); [rslib/src/scheduler/answering/preview.rs:17](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/preview.rs#L17); [rslib/src/scheduler/answering/mod.rs:341](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L341).

```gherkin
Scenario: AC-ANKI-045 — Preview delay bằng không
  Given reschedule tắt; ba fixture độc lập: Good delay=0, Good delay=60s, Easy; giữ last_review_time trước học
  When trả lời rồi đọc card, home/queue và revlog
  Then Good delay=0 và Easy kết thúc và phục hồi home/queue; Good 60s tiếp tục preview; có revlog nhưng last_review_time không cập nhật như normal study
```

## AC-ANKI-046 — Text update giữ lịch

Nguồn: **US-ANKI-13** · FR: FR-DAT-TEXT-001 · BR: BR-ANKI-001, BR-ANKI-020 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[rslib/src/import_export/text/import.rs:250](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L250); [rslib/src/import_export/text/import.rs:318](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L318); [rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194).

```gherkin
Scenario: AC-ANKI-046 — Text update giữ lịch
  Given note BasicQA GUID=gQA, Front=alpha, Back=old có card đã học ở QA-A; UTF-8 TSV GUID=gQA, Front=alpha, Back=new; mapping đúng và Update
  When nhập TSV rồi đọc note/card
  Then Back thành new; card hiện có giữ ID, deck, due/interval và lịch; không tạo note thứ hai cho GUID đó
```

## AC-ANKI-047 — First field rỗng không chặn hàng sau

Nguồn: **US-ANKI-13** · FR: FR-DAT-TEXT-001 · BR: BR-ANKI-020 · ERR: ERR-ANKI-000-05. Loại: **negative**. Design: **Specified**; approval: Draft.

[rslib/src/import_export/text/import.rs:250](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L250); [rslib/src/import_export/text/import.rs:318](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L318); [rslib/src/import_export/text/import.rs:252](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L252).

```gherkin
Scenario: AC-ANKI-047 — First field rỗng không chặn hàng sau
  Given UTF-8 TSV gồm dòng 1 first field rỗng, dòng 2 Front=valid; NoteType/deck hợp lệ và mapping đủ
  When import file rồi đọc log và note count
  Then dòng 1 thuộc log.empty_first_field theo ERR-ANKI-000-05; dòng 2 vẫn được xử lý; không tạo note hợp lệ từ dòng 1
```

## AC-ANKI-048 — Không resolve NoteType/deck

Nguồn: **US-ANKI-13** · FR: FR-DAT-TEXT-001 · BR: BR-ANKI-020 · ERR: ERR-ANKI-000-06. Loại: **negative**. Design: **Specified**; approval: Draft.

[rslib/src/import_export/text/import.rs:250](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L250); [rslib/src/import_export/text/import.rs:318](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L318); [rslib/src/import_export/text/import.rs:266](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L266).

```gherkin
Scenario: AC-ANKI-048 — Không resolve NoteType/deck
  Given hai hàng có first field hợp lệ; hàng A tham chiếu NoteType ID không tồn tại; hàng B có NoteType hợp lệ nhưng deck ID không tồn tại; dùng ID, không tên deck mới
  When import rồi đọc row log
  Then A thuộc missing_notetype, B thuộc missing_deck theo ERR-ANKI-000-06; không nhập hai hàng như added
```

## AC-ANKI-049 — GUID trùng nhưng type xung đột

Nguồn: **US-ANKI-13** · FR: FR-DAT-TEXT-001 · BR: BR-ANKI-020 · ERR: ERR-ANKI-000-07. Loại: **negative**. Design: **Specified**; approval: Draft.

[rslib/src/import_export/text/import.rs:250](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L250); [rslib/src/import_export/text/import.rs:318](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L318); [rslib/src/import_export/text/import.rs:401](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L401).

```gherkin
Scenario: AC-ANKI-049 — GUID trùng nhưng type xung đột
  Given note hiện có GUID=gQA kiểu BasicQA; hàng nhập GUID=gQA nhưng NoteType khác không tương thích, first field không rỗng
  When import với Update
  Then row log conflicting theo ERR-ANKI-000-07; note hiện có không được cập nhật như một match hợp lệ
```

## AC-ANKI-050 — Duplicate policy và ưu tiên GUID

Nguồn: **US-ANKI-13** · FR: FR-DAT-TEXT-001 · BR: BR-ANKI-020 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/import_export/text/import.rs:250](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L250); [rslib/src/import_export/text/import.rs:318](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L318).

```gherkin
Scenario: AC-ANKI-050 — Duplicate policy và ưu tiên GUID
  Given các bản sao collection có một note alpha/BasicQA; các hàng lần lượt không GUID cùng first field, và GUID=gQA đã tồn tại; chọn từng policy Update/Preserve/Duplicate
  When nhập từng tổ hợp vào bản sao độc lập
  Then không GUID áp policy first-field/NoteType: cập nhật, giữ hoặc thêm bản sao; có GUID đã tồn tại không tạo bản sao mới dù Duplicate; chụp log từng nhánh
```

## AC-ANKI-051 — apkg giữ lịch card cũ

Nguồn: **US-ANKI-14** · FR: FR-DAT-PKG-001 · BR: BR-ANKI-021 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[rslib/src/import_export/package/apkg/import/notes.rs:333](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L333); [rslib/src/import_export/package/apkg/import/cards.rs:99](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/cards.rs#L99); [rslib/src/import_export/package/colpkg/import.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/colpkg/import.rs#L31).

```gherkin
Scenario: AC-ANKI-051 — apkg giữ lịch card cũ
  Given collection có note GUID=gQA card ordinal 0 đã học; apkg có note cùng GUID mới hơn, ordinal 0 lịch khác và ordinal 1 mới với log có ID duy nhất; cùng NoteType Normal schema hai template; IfNewer
  When import apkg
  Then note được cập nhật; card ordinal 0 giữ lịch hiện tại và không nhập log của card đó từ gói; ordinal 1 được thêm và log duy nhất của card mới được nhập
```

## AC-ANKI-052 — Không merge Normal và Cloze

Nguồn: **US-ANKI-14** · FR: FR-DAT-PKG-001 · BR: BR-ANKI-021 · ERR: ERR-ANKI-000-08. Loại: **negative**. Design: **Specified**; approval: Draft.

[rslib/src/import_export/package/apkg/import/notes.rs:333](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L333); [rslib/src/import_export/package/apkg/import/cards.rs:99](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/cards.rs#L99); [rslib/src/import_export/package/colpkg/import.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/colpkg/import.rs#L31); [rslib/src/import_export/package/apkg/import/notes.rs:234](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L234).

```gherkin
Scenario: AC-ANKI-052 — Không merge Normal và Cloze
  Given collection có NoteType Normal; apkg yêu cầu merge NoteType tương ứng nhưng loại Cloze; bật merge
  When import apkg qua đường merge NoteType
  Then trả ERR-ANKI-000-08 / ImportError::NotetypeKindMergeConflict; không báo merge Normal/Cloze thành công
```

## AC-ANKI-053 — Ranh giới mtime và policy

Nguồn: **US-ANKI-14** · FR: FR-DAT-PKG-001 · BR: BR-ANKI-021 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/import_export/package/apkg/import/notes.rs:333](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L333); [rslib/src/import_export/package/apkg/import/cards.rs:99](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/cards.rs#L99); [rslib/src/import_export/package/colpkg/import.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/colpkg/import.rs#L31); [rslib/src/import_export/package/apkg/import/notes.rs:521](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L521).

```gherkin
Scenario: AC-ANKI-053 — Ranh giới mtime và policy
  Given note local mtime=t; các apkg cùng GUID với mtime=t−1,t,t+1 và nội dung khác; thử IfNewer/Always/Never trên bản sao độc lập
  When import mỗi tổ hợp và so nội dung note
  Then IfNewer chỉ cập nhật t+1; Always cập nhật khi mtime khác t nhưng bỏ t; Never không cập nhật note cũ; đây là As-Is source, không diễn giải Always vô điều kiện
```

## AC-ANKI-054 — colpkg thay collection nhưng giữ media ngoài gói

Nguồn: **US-ANKI-14** · FR: FR-DAT-PKG-001 · BR: BR-ANKI-022 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[rslib/src/import_export/package/apkg/import/notes.rs:333](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L333); [rslib/src/import_export/package/apkg/import/cards.rs:99](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/cards.rs#L99); [rslib/src/import_export/package/colpkg/import.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/colpkg/import.rs#L31); [docs-site/manual/exporting.mdx:34](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/exporting.mdx#L34).

```gherkin
Scenario: AC-ANKI-054 — colpkg thay collection nhưng giữ media ngoài gói
  Given profile tạm có note LOCAL-ONLY và media orphan-old.png; colpkg QA gồm note SNAPSHOT, scheduling và new.png; bật media khi export
  When import colpkg vào profile tạm
  Then collection trở thành nội dung gói gồm SNAPSHOT và scheduling; LOCAL-ONLY không còn như merge apkg; orphan-old.png không bị xóa chỉ vì ngoài package
```

## AC-ANKI-055 — Export không scheduling

Nguồn: **US-ANKI-14** · FR: FR-DAT-PKG-001 · BR: BR-ANKI-022 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/import_export/package/apkg/import/notes.rs:333](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L333); [rslib/src/import_export/package/apkg/import/cards.rs:99](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/cards.rs#L99); [rslib/src/import_export/package/colpkg/import.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/colpkg/import.rs#L31); [docs-site/manual/exporting.mdx:34](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/exporting.mdx#L34); [docs-site/manual/exporting.mdx:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/exporting.mdx#L80).

```gherkin
Scenario: AC-ANKI-055 — Export không scheduling
  Given note có tags marked/leech/qa, card đã học; export apkg với scheduling tắt; profile nhận rỗng
  When import bản export vào profile nhận và so với bản gốc
  Then bản chia sẻ không mang scheduling cũ và không mang marked/leech; dữ liệu gốc vẫn giữ lịch/tag; scope media theo tùy chọn export
```

## AC-ANKI-056 — Remote mới hơn thay toàn record

Nguồn: **US-ANKI-15** · FR: FR-DAT-SYNC-001 · BR: BR-ANKI-023 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[rslib/src/sync/collection/chunks.rs:162](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/chunks.rs#L162); [rslib/src/sync/collection/meta.rs:65](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L65).

```gherkin
Scenario: AC-ANKI-056 — Remote mới hơn thay toàn record
  Given hai collection fixture cùng note_id và GUID; local pending với fields [localA,oldB], mtime=t; remote [oldA,remoteB], mtime=t+1; endpoint thử nghiệm cô lập
  When áp chunk sync note/card theo protocol tương thích
  Then record remote thắng theo mtime; không ghép thành [localA,remoteB]; revlog hợp lệ được nhập theo nhánh riêng
```

## AC-ANKI-057 — Remote không mới hơn local pending

Nguồn: **US-ANKI-15** · FR: FR-DAT-SYNC-001 · BR: BR-ANKI-023 · ERR: —. Loại: **negative**. Design: **Specified**; approval: Draft.

[rslib/src/sync/collection/chunks.rs:162](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/chunks.rs#L162); [rslib/src/sync/collection/meta.rs:65](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L65).

```gherkin
Scenario: AC-ANKI-057 — Remote không mới hơn local pending
  Given hai bản sao fixture: local pending mtime=t; remote mtime=t−1 hoặc t; nội dung khác
  When áp incoming chunk của từng fixture
  Then remote không thay local tại bước áp chunk này; không suy ra toàn bộ sync luôn giữ cả hai chỉnh sửa
```

## AC-ANKI-058 — Local không pending

Nguồn: **US-ANKI-15** · FR: FR-DAT-SYNC-001 · BR: BR-ANKI-023 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/sync/collection/chunks.rs:162](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/chunks.rs#L162); [rslib/src/sync/collection/meta.rs:65](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L65).

```gherkin
Scenario: AC-ANKI-058 — Local không pending
  Given local record không pending sync, mtime=t; incoming remote hợp lệ mtime=t−1
  When áp incoming chunk
  Then điều kiện không pending cho phép nhận remote dù timestamp không lớn hơn local; kiểm tra đúng branch thay record
```

## AC-ANKI-059 — Full sync theo chiều và media riêng

Nguồn: **US-ANKI-15** · FR: FR-DAT-SYNC-001 · BR: BR-ANKI-023, BR-ANKI-028 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/sync/collection/chunks.rs:162](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/chunks.rs#L162); [rslib/src/sync/collection/meta.rs:65](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L65); [docs-site/manual/media.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/media.mdx#L24).

```gherkin
Scenario: AC-ANKI-059 — Full sync theo chiều và media riêng
  Given hai bản sao local/remote có schema khác; LOCAL-ONLY và REMOTE-ONLY phân biệt rõ; media có file riêng mỗi phía
  When thực hiện Upload trên fixture thứ nhất và Download trên fixture thứ hai bằng server test cô lập
  Then Upload chọn collection local làm phía gửi; Download thay local bằng remote; không dùng lựa chọn collection một chiều để kết luận media đã xong hoặc bị thay một chiều
```

## AC-ANKI-060 — Restore snapshot

Nguồn: **US-ANKI-16** · FR: FR-DAT-BACK-001 · BR: BR-ANKI-024 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[rslib/src/collection/backup.rs:28](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/collection/backup.rs#L28); [docs-site/manual/backups.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L7); [docs-site/manual/backups.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L24).

```gherkin
Scenario: AC-ANKI-060 — Restore snapshot
  Given profile tạm có snapshot gồm note S và card lịch D; sau snapshot thêm note L và sửa D; backup tự động không media
  When restore snapshot rồi kiểm tra collection và mở lại ứng dụng trong môi trường test
  Then note S và lịch tại snapshot được phục hồi; thay đổi sau snapshot như L không còn; auto-sync/backup tạm dừng đến khi mở lại theo manual
```

## AC-ANKI-061 — Force không vượt guard không thay đổi

Nguồn: **US-ANKI-16** · FR: FR-DAT-BACK-001 · BR: BR-ANKI-024 · ERR: —. Loại: **negative**. Design: **Specified**; approval: Draft.

[rslib/src/collection/backup.rs:28](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/collection/backup.rs#L28); [docs-site/manual/backups.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L7); [docs-site/manual/backups.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L24).

```gherkin
Scenario: AC-ANKI-061 — Force không vượt guard không thay đổi
  Given collection chưa đổi từ lần backup gần nhất; ghi danh sách file backup; force=true
  When gọi maybe_backup và chờ kết quả nếu có handle
  Then không tạo backup mới; trả None ở guard changed_since_last_backup trước kiểm tra interval
```

## AC-ANKI-062 — Ngay trước, tại và sau interval backup

Nguồn: **US-ANKI-16** · FR: FR-DAT-BACK-001 · BR: BR-ANKI-024 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/collection/backup.rs:28](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/collection/backup.rs#L28); [docs-site/manual/backups.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L7); [docs-site/manual/backups.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L24); [rslib/src/collection/backup.rs:62](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/collection/backup.rs#L62).

```gherkin
Scenario: AC-ANKI-062 — Ngay trước, tại và sau interval backup
  Given ba fixture collection đã đổi; minimum_interval_mins=30; backup gần nhất tại t0; clock filesystem/SystemTime có thể kiểm soát t0+1799s,1800s,1801s; force=false
  When gọi maybe_backup mỗi mốc với thư mục backup riêng
  Then 1799s bị skip do còn recent; tại 1800s và 1801s không còn recent nên có thể tạo backup; chờ writer hoàn tất và kiểm file thuộc fixture
```

## AC-ANKI-063 — Media phải backup bằng colpkg

Nguồn: **US-ANKI-16** · FR: FR-DAT-BACK-001 · BR: BR-ANKI-022, BR-ANKI-024 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/collection/backup.rs:28](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/collection/backup.rs#L28); [docs-site/manual/backups.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L7); [docs-site/manual/backups.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L24); [docs-site/manual/exporting.mdx:34](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/exporting.mdx#L34); [docs-site/manual/backups.mdx:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L59).

```gherkin
Scenario: AC-ANKI-063 — Media phải backup bằng colpkg
  Given profile fixture có note tham chiếu QA.png; tạo một backup tự động và một export colpkg Include Media; hai profile nhận rỗng
  When restore/import từng gói vào profile nhận tương ứng
  Then backup tự động phục hồi text/scheduling nhưng không khôi phục QA.png ở profile rỗng; colpkg Include Media mang cả asset đã xuất
```

## AC-ANKI-064 — Today đếm lượt, không card duy nhất

Nguồn: **US-ANKI-17** · FR: FR-RPT-STAT-001 · BR: BR-ANKI-025 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[rslib/src/stats/graphs/today.rs:17](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/today.rs#L17); [rslib/src/stats/graphs/retention.rs:53](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L53).

```gherkin
Scenario: AC-ANKI-064 — Today đếm lượt, không card duy nhất
  Given cùng card có hai log học hôm nay: Again rồi Good; không log khác; clock/day range cố định
  When tính Today statistics
  Then hai lượt trả lời được đếm, một lượt đúng; không rút thành một card hay kết luận card đã nhớ hoàn toàn
```

## AC-ANKI-065 — Loại log thao tác thủ công

Nguồn: **US-ANKI-17** · FR: FR-RPT-STAT-001 · BR: BR-ANKI-025 · ERR: —. Loại: **negative**. Design: **Specified**; approval: Draft.

[rslib/src/stats/graphs/today.rs:17](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/today.rs#L17); [rslib/src/stats/graphs/retention.rs:53](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L53).

```gherkin
Scenario: AC-ANKI-065 — Loại log thao tác thủ công
  Given fixture cùng phạm vi có hai log Manual/Rescheduled và một log Review Hard hợp lệ
  When tính Today statistics
  Then Manual/Rescheduled không được tính vào số lượt trả lời Today; Hard hợp lệ được tính đúng
```

## AC-ANKI-066 — Mature theo interval trước

Nguồn: **US-ANKI-17** · FR: FR-RPT-STAT-001 · BR: BR-ANKI-025 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/stats/graphs/today.rs:17](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/today.rs#L17); [rslib/src/stats/graphs/retention.rs:53](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L53).

```gherkin
Scenario: AC-ANKI-066 — Mature theo interval trước
  Given ba Review log hợp lệ có last_interval 20,21,22 ngày; cùng rating Good và cùng khoảng thời gian
  When tính thống kê mature
  Then 20 là young; 21 và 22 là mature; không dùng interval mới thay last_interval
```

## AC-ANKI-067 — True retention đếm cả hai lượt cùng card trong ngày

Nguồn: **US-ANKI-17** · FR: FR-RPT-STAT-001 · BR: BR-ANKI-025 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/storage/revlog/get.sql:1](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/get.sql#L1); [rslib/src/storage/revlog/mod.rs:122](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/mod.rs#L122); [rslib/src/storage/revlog/mod.rs:175](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/mod.rs#L175); [rslib/src/stats/graphs/mod.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/mod.rs#L31); [rslib/src/stats/graphs/retention.rs:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L16); [rslib/src/stats/graphs/retention.rs:53](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L53); [rslib/src/revlog/mod.rs:107](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/revlog/mod.rs#L107); [ts/routes/graphs/true-retention.ts:105](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/graphs/true-retention.ts#L105); [docs-site/manual/stats.mdx:229](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/stats.mdx#L229).

```gherkin
Scenario: AC-ANKI-067 — True retention đếm cả hai lượt cùng card trong ngày
  Given fixture F067-min có đúng một card cid=1001 và hai revlog: id=1793682000000/ease=1 rồi id=1793685600000/ease=3; cả hai type=Review(1), lastIvl=20, factor=2500, ivl=1, usn=-1, time=1000; không có log khác; clock=2026-11-03T12:00:00Z, offset UTC, rollover 04:00, next_day_at=1793764800; search="", days=0 và locale en-US
  When lấy graph data All history và xem True retention ở các chế độ Young, Mature, All; sau đó lấy lại với search cid:1001
  Then today/week/month/year/allTime đều có young_passed=1, young_failed=1, mature_passed=0, mature_failed=0; Count=2, Young và Total=50.0%, Mature=N/A; yesterday có bốn counter=0, Count=0 và các tỷ lệ N/A; search cid:1001 không đổi kết quả; không bỏ lượt Good thứ hai cùng ngày
```

**Giới hạn oracle:** Oracle As-Is theo pipeline source đếm từng log đủ điều kiện, khác manual first review/card/day. Chỉ giải quyết kết quả hiện hành; quyết định sửa manual hay đổi sản phẩm còn mở. Fixture tối thiểu này không chứng minh mọi bộ lọc/biên; fixture mở rộng 22 row nằm trong báo cáo retention riêng, chưa thực thi.

## AC-ANKI-068 — Hook Add và filter trả giá trị

Nguồn: **US-ANKI-18** · FR: FR-EXT-ADD-001 · BR: BR-ANKI-026 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16); [qt/tools/genhooks_gui.py:313](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/tools/genhooks_gui.py#L313); [qt/aqt/reviewer.py:391](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/reviewer.py#L391).

```gherkin
Scenario: AC-ANKI-068 — Hook Add và filter trả giá trị
  Given profile thử nghiệm chỉ cài addon QA cục bộ không network: hook note_will_be_added ghi counter, filter card_will_show nối QA_SUFFIX vào text rồi trả text; collection rỗng
  When thêm note bằng Add screen rồi hiện câu hỏi card trong reviewer
  Then hook Add được gọi; filter card_will_show nhận kind=reviewQuestion và trả text có QA_SUFFIX, reviewer nhận text đã đổi
```

## AC-ANKI-069 — Hook Add không chặn import

Nguồn: **US-ANKI-18** · FR: FR-EXT-ADD-001 · BR: BR-ANKI-026 · ERR: —. Loại: **negative**. Design: **Specified**; approval: Draft.

[docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16).

```gherkin
Scenario: AC-ANKI-069 — Hook Add không chặn import
  Given cùng addon QA ghi counter note_will_be_added; trước import reset counter=0; file text hợp lệ
  When import file text
  Then note_will_be_added không được gọi do import; counter vẫn 0; không xem hook này là policy cho mọi đường nhập
```

## AC-ANKI-070 — Nhiều addon và profile

Nguồn: **US-ANKI-18** · FR: FR-EXT-ADD-001 · BR: BR-ANKI-026, BR-ANKI-027 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16); [docs-site/manual/profiles.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/profiles.mdx#L5); [docs-site/addons/hooks-and-filters.mdx:49](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L49).

```gherkin
Scenario: AC-ANKI-070 — Nhiều addon và profile
  Given hai callback QA đăng ký reviewer_did_show_question theo thứ tự A rồi B, mỗi callback ghi vào log fixture; hai profile tạm dùng chung thư mục addon
  When hiện câu hỏi ở profile thứ nhất rồi chuyển profile thứ hai có card fixture và hiện câu hỏi
  Then callback được gọi tuần tự theo contract hooks; addon cùng được dùng giữa profile; không suy ra collection của hai profile là chung
```

## AC-ANKI-071 — Hai collection riêng

Nguồn: **US-ANKI-19** · FR: FR-SYS-PROF-001 · BR: BR-ANKI-027 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[docs-site/manual/profiles.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/profiles.mdx#L5).

```gherkin
Scenario: AC-ANKI-071 — Hai collection riêng
  Given profile QA-A có note ALPHA; QA-B mới rỗng; auto-sync tắt ở cả hai
  When chuyển QA-A sang QA-B rồi trở lại QA-A
  Then QA-B không có ALPHA; QA-A vẫn có ALPHA trong collection riêng; thiết lập thuộc profile được đọc theo profile hiện hành
```

## AC-ANKI-072 — Hai profile cùng account và lựa chọn full sync

Nguồn: **US-ANKI-19** · FR: FR-SYS-PROF-001 · BR: BR-ANKI-027 · ERR: —. Loại: **negative**. Design: **Specified**; approval: Draft.

[qt/aqt/profiles.py:212](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L212); [qt/aqt/profiles.py:659](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L659); [qt/aqt/profiles.py:681](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L681); [qt/aqt/sync.py:307](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L307); [rslib/src/sync/http_server/mod.rs:122](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/http_server/mod.rs#L122); [rslib/src/sync/collection/meta.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L59); [qt/aqt/sync.py:138](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L138); [rslib/src/sync/collection/download.rs:35](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/download.rs#L35); [rslib/src/sync/collection/upload.rs:79](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/upload.rs#L79); [rslib/src/sync/collection/tests.rs:591](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/tests.rs#L591); [docs-site/manual/profiles.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/profiles.mdx#L5).

```gherkin
Scenario: AC-ANKI-072 — Hai profile cùng account và lựa chọn full sync
  Given F072 có hai profile tạm A/B, collection path riêng; cùng auth của một user SimpleServer đúng commit, auto-sync/media/add-on tắt; A có một note/card ONLY_A, B có một note/card ONLY_B với ID/GUID khác; server đã nhận full upload A; B và server đều có card, B.scm khác S.scm và B.mod khác S.mod; snapshot từng nhánh độc lập
  When B bấm Sync, quan sát FullSyncRequired có upload_ok=true và download_ok=true, rồi chọn Cancel, Download hoặc Upload trên từng snapshot mới
  Then không có chặn trùng account trong caller đã khảo sát; Cancel không gọi full upload/download và giữ ONLY_B ở B, ONLY_A ở server/A; Download thay active B bằng snapshot A từ server, ONLY_B không còn ở active B; Upload thay active server bằng B nhưng A local vẫn giữ ONLY_A vì chưa sync tiếp; collection paths vẫn riêng và không có namespace server riêng theo tên profile
```

**Giới hạn oracle:** Oracle cho SimpleServer và caller desktop tại commit. Khi mod bằng nhau có thể NoChanges trước khi xét schema; khi schema chung có thể normal merge. B rỗng/server nonempty chỉ cho Download. Không suy thành mọi lần trùng account đều full-sync, mất dữ liệu ngay hoặc server hosted có cùng implementation. Cancel chỉ cam kết nội dung collection, không cam kết byte-identical metadata/profile.

## AC-ANKI-073 — Addon dùng chung giữa profile

Nguồn: **US-ANKI-19** · FR: FR-SYS-PROF-001 · BR: BR-ANKI-027 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[docs-site/manual/profiles.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/profiles.mdx#L5).

```gherkin
Scenario: AC-ANKI-073 — Addon dùng chung giữa profile
  Given profile QA-A/QA-B collection riêng; addon QA cục bộ được cài một lần, không lưu thông tin cá nhân
  When mở lần lượt hai profile và quan sát danh sách/lifecycle addon
  Then cùng addon dùng được ở cả hai profile; sự riêng biệt collection không tạo sandbox addon theo từng profile
```

## AC-ANKI-074 — Check Media phân biệt thiếu và không dùng

Nguồn: **US-ANKI-20** · FR: FR-DAT-MEDI-001 · BR: BR-ANKI-028 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[docs-site/manual/media.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/media.mdx#L24); [docs-site/manual/syncing.mdx:54](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/syncing.mdx#L54).

```gherkin
Scenario: AC-ANKI-074 — Check Media phân biệt thiếu và không dùng
  Given note tham chiếu exists.png và missing.png; thư mục chỉ có exists.png và orphan.png; không file/template khác
  When chạy Check Media trên profile tạm
  Then missing.png thuộc tham chiếu thiếu; orphan.png thuộc file không dùng; exists.png không thuộc hai nhóm đó
```

## AC-ANKI-075 — Template media không được quét như field

Nguồn: **US-ANKI-20** · FR: FR-DAT-MEDI-001 · BR: BR-ANKI-028 · ERR: —. Loại: **negative**. Design: **Specified**; approval: Draft.

[docs-site/manual/media.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/media.mdx#L24); [docs-site/manual/syncing.mdx:54](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/syncing.mdx#L54).

```gherkin
Scenario: AC-ANKI-075 — Template media không được quét như field
  Given template tham chiếu logo.png; không note field nào tham chiếu; logo.png có trong media và không có tiền tố _
  When chạy Check Media, chỉ xem kết quả không xác nhận xóa
  Then không coi tham chiếu template là bằng chứng file đang dùng trong phép quét; logo.png được báo unused trong fixture này
```

## AC-ANKI-076 — Tiền tố underscore cho static media

Nguồn: **US-ANKI-20** · FR: FR-DAT-MEDI-001 · BR: BR-ANKI-028 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[docs-site/manual/media.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/media.mdx#L24); [docs-site/manual/syncing.mdx:54](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/syncing.mdx#L54).

```gherkin
Scenario: AC-ANKI-076 — Tiền tố underscore cho static media
  Given template tham chiếu _logo.png có trong media; không field nào tham chiếu; một file logo.png thường cũng tồn tại không dùng
  When chạy Check Media
  Then _logo.png được bảo vệ bởi quy ước static media; logo.png thường được xét unused; không tự xóa file trong test
```

## AC-ANKI-077 — Media cùng tên khác hash với thứ tự sync xác định

Nguồn: **US-ANKI-20** · FR: FR-DAT-MEDI-001 · BR: BR-ANKI-028 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[rslib/src/sync/media/syncer.rs:60](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/syncer.rs#L60); [rslib/src/sync/media/changes.rs:44](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/changes.rs#L44); [rslib/src/media/files.rs:403](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L403); [rslib/src/sync/media/database/client/mod.rs:206](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/client/mod.rs#L206); [rslib/src/sync/media/database/server/entry/upload.rs:35](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/server/entry/upload.rs#L35); [rslib/src/sync/media/tests.rs:278](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/tests.rs#L278); [rslib/src/backend/sync.rs:188](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/backend/sync.rs#L188); [rslib/src/sync/media/database/client/changetracker.rs:56](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/client/changetracker.rs#L56); [rslib/src/media/files.rs:165](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L165).

```gherkin
Scenario: AC-ANKI-077 — Media cùng tên khác hash với thứ tự sync xác định
  Given F077 có C1/C2 và SimpleServer S cùng user test, media DB/folder riêng, cursors=0 và S trống USN0; C1 thêm shared.png=A và C2 thêm shared.png=B qua add_file ở folder trống, hai entry dirty=true; A/B là PNG 1×1/69byte có bytes PNG trong mục dữ liệu TC-ANKI-077, SHA1 A=2732f12a8f18d27cf0fa78ef41091bfa1ccec9ce, B=3b37538efb87e9eb1c6d547562f499932b894f17; không sửa đồng thời
  When chạy media sync C1 hoàn tất rồi C2 hoàn tất rồi C1 kiểm tra lại; lặp trên fixture reset với thứ tự đảo; sau đó kiểm nhánh C2 sửa B khi toàn bộ đã đồng nhất A ở USN1 và server không có thay đổi mới
  Then thứ tự C1→C2: C2 fetch server USN1 và download A dù B local dirty, ghi đè shared.png, DB clean và không upload B; C1/C2/S đều hash A, server vẫn USN1 và có một filename; không tạo hash-suffix hay bản B trong media.trash. Đảo thứ tự cho hash B. Nhánh sửa sau đồng nhất: C2 dirty B với cursor1=S.USN1 sẽ upload B lên S.USN2, rồi C1 fetch B; các bên hash B. Không dùng file mtime để chọn winner
```

**Giới hạn oracle:** Server-favors yêu cầu remote change chưa được client nhận; local dirty một mình không bảo vệ file trước nhánh download. Hai upload in-flight chưa có thứ tự thì không có winner duy nhất; server self-host nhận upload khác hash sau có thể thay nội dung. Local add_file vào folder đã có tên dùng hash-suffix là luồng khác. Không khẳng định rollback filesystem khi I/O/network lỗi hoặc hosted AnkiWeb đã được kiểm thử.

## AC-ANKI-078 — Thêm/gỡ tag ở cấp note

Nguồn: **US-ANKI-06** · FR: FR-ORG-SRCH-001 · BR: BR-ANKI-007 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226).

```gherkin
Scenario: AC-ANKI-078 — Thêm/gỡ tag ở cấp note
  Given note N có siblings A/B, note M có card C; cả hai chưa có tag qa; chỉ chọn A trong Browse Cards
  When Add Tags qa rồi kiểm tra, sau đó Remove Tags qa trên cùng lựa chọn
  Then tag qa được thêm rồi gỡ trên note N nên cả A/B phản ánh thay đổi; note M/card C không nhận hoặc mất tag do thao tác này
```

## AC-ANKI-079 — Một flag trên một card

Nguồn: **US-ANKI-06** · FR: FR-ORG-SRCH-001 · BR: BR-ANKI-007 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226).

```gherkin
Scenario: AC-ANKI-079 — Một flag trên một card
  Given siblings A/B cùng note; A chưa flag, B flag=3; chỉ chọn A; note tags đã chụp
  When đặt flag 1 cho A, thay bằng flag 2, rồi chọn flag 2 lần nữa để gỡ
  Then A lần lượt flag 1, flag 2, không flag; không đồng thời giữ hai flag; B vẫn flag 3 và note tags không đổi
```

## AC-ANKI-080 — Đổi tên tag đang dùng

Nguồn: **US-ANKI-06** · FR: FR-ORG-SRCH-001 · BR: BR-ANKI-007 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226).

```gherkin
Scenario: AC-ANKI-080 — Đổi tên tag đang dùng
  Given note N có tag qa_old, note M có tag unrelated; không tag qa_new tồn tại
  When đổi tên qa_old thành qa_new trong Browser rồi tìm tag:qa_new
  Then N có qa_new và truy vấn trả siblings của N; qa_old không còn là tag của N; M giữ unrelated
```

## AC-ANKI-081 — Cài addon local hợp lệ

Nguồn: **US-ANKI-18** · FR: FR-EXT-ADD-001 · BR: BR-ANKI-026 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16); [qt/aqt/addons.py:1025](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1025).

```gherkin
Scenario: AC-ANKI-081 — Cài addon local hợp lệ
  Given profile thử nghiệm chỉ có thư mục addon QA; package ZIP tự tạo chứa __init__.py không side effect và manifest hợp schema với package=qa_fixture, name=QA Fixture; chưa có package đó
  When Install from file với force_enable=True rồi đọc metadata/files và danh sách addon
  Then cài file vào addon folder qa_fixture, metadata name tương ứng và disabled=False; danh sách được redraw; chưa coi code addon đã nạp cho đến lifecycle restart
```

## AC-ANKI-082 — Hủy hoặc sai mã Get Add-ons

Nguồn: **US-ANKI-18** · FR: FR-EXT-ADD-001 · BR: BR-ANKI-026 · ERR: —. Loại: **negative**. Design: **Specified**; approval: Draft.

[docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16); [qt/aqt/addons.py:1091](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1091).

```gherkin
Scenario: AC-ANKI-082 — Hủy hoặc sai mã Get Add-ons
  Given hai fixture dialog riêng: A nhập not-a-number, B đóng Cancel; instrumentation chỉ đếm download dispatch, không gọi AnkiWeb thật
  When bấm OK ở A và Cancel ở B
  Then A hiển thị cảnh báo invalid code và không accept; B không có IDs; cả hai không phát lệnh tải addon; không gán ERR/HTTP chưa có trong SRS
```

## AC-ANKI-083 — Get IDs và kiểm tra cập nhật

Nguồn: **US-ANKI-18** · FR: FR-EXT-ADD-001 · BR: BR-ANKI-026 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16); [qt/aqt/addons.py:1091](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1091).

```gherkin
Scenario: AC-ANKI-083 — Get IDs và kiểm tra cập nhật
  Given dialog Get Add-ons có chuỗi 123 456 hoặc URL https://ankiweb.net/shared/info/123; dùng hai fixture độc lập; dispatcher được quan sát trước network; mọi addon giả lập ở thư mục test
  When accept Get Add-ons rồi riêng biệt nhấn Check for Updates
  Then IDs được parse thành integer theo input và chuyển tới download_addons với force_enable=True; Check for Updates gọi check_and_prompt_for_updates và callback after_downloading; chưa khẳng định ID ví dụ tồn tại hoặc tải/cập nhật thành công trên AnkiWeb
```

## AC-ANKI-084 — Delete hủy hoặc không chọn addon

Nguồn: **US-ANKI-18** · FR: FR-EXT-ADD-001 · BR: BR-ANKI-026 · ERR: —. Loại: **negative**. Design: **Specified**; approval: Draft.

[docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16).

```gherkin
Scenario: AC-ANKI-084 — Delete hủy hoặc không chọn addon
  Given hai fixture có addon QA đã cài: A không chọn hàng; B chọn addon QA nhưng chọn No ở xác nhận; ghi hash thư mục và metadata trước
  When nhấn Delete theo từng fixture
  Then A không xóa và không hỏi xác nhận; B dừng sau No; cả hai giữ thư mục/metadata addon QA, không phát lifecycle will_delete
```

## AC-ANKI-085 — Delete addon bật sau xác nhận

Nguồn: **US-ANKI-18** · FR: FR-EXT-ADD-001 · BR: BR-ANKI-026 · ERR: —. Loại: **happy**. Design: **Specified**; approval: Draft.

[docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16); [qt/aqt/addons.py:526](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L526).

```gherkin
Scenario: AC-ANKI-085 — Delete addon bật sau xác nhận
  Given addon qa_fixture đang enabled trong profile test; chọn riêng addon đó; trash chỉ chứa dữ liệu test; không có addon thật
  When nhấn Delete và xác nhận Yes
  Then gọi lifecycle will_delete, chuyển thư mục addon vào trash, redraw danh sách và đánh dấu require_restart=True; không tuyên bố addon đang nạp đã ngừng tức thời
```

## AC-ANKI-086 — Toggle và xung đột khi bật

Nguồn: **US-ANKI-18** · FR: FR-EXT-ADD-001 · BR: BR-ANKI-026 · ERR: —. Loại: **boundary**. Design: **Specified**; approval: Draft.

[docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16).

```gherkin
Scenario: AC-ANKI-086 — Toggle và xung đột khi bật
  Given hai fixture addon QA-A/QA-B có metadata conflicts hợp lệ; QA-B đang bật, QA-A đang tắt; chọn QA-A; bản sao thứ hai chọn addon đang bật để tắt
  When Toggle Enabled rồi đọc metadata và yêu cầu restart
  Then nhánh bật ghi enabled=True cho QA-A và vô hiệu addon xung đột tìm được; nhánh tắt ghi enabled=False cho addon chọn; UI đánh require_restart=True và redraw; không giả định reload code tức thời
```

## Câu hỏi còn mở

Bốn oracle035/067/072/077 đã chốt trong fixture và giới hạn nêu ở từng ca. Còn quyết định To-Be cho discrepancy retention manual/code; caller UI bật ensure_not_empty chưa khảo sát toàn bộ; thông báo/localization lỗi ngoài scope chưa đối chiếu. Mọi runtime/OS/client và NFR cần thực thi riêng; chưa có approval.

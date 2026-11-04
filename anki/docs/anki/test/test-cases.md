---
id: DOC-TC-ANKI-001
title: "Test Cases và RTM Anki Desktop — As-Is"
version: "1.0.1"
phase: Testing
domain: Anki
tags: [anki, as-is, reconstructed, qa, draft]
depends_on: ["DOC-SRS-ANKI-001", "DOC-US-ANKI-001", "DOC-AC-ANKI-001"]
related_diagrams: []
author: BA Agent
last_updated: "2026-11-03"
status: draft
---

# Test Cases và RTM Anki Desktop — As-Is

## Lịch sử sửa đổi

| Phiên bản | Ngày | Tác giả | Nội dung |
|---|---|---|---|
| 1.0.1 | 2026-11-03 | BA Analysis | Làm rõ oracle035/067/072/077 và truy vết liên quan; không thay source hoặc kết quả chạy |
| 1.0.0 | 2026-11-02 | BA Agent | Tái lập As-Is từ SRS v1.0.0; Draft, chưa phê duyệt, chưa thực thi kiểm thử. |

Nguồn: [SRS](../srs/spec.md), [requirements.json](../srs/requirements.json), [backlog](../userstories/backlog.md), [AC](../userstories/acceptance-criteria.md), tất cả version 1.0.1. **Tất cả test Not Run**, chưa build, chạy Anki, chạy upstream test hay thao tác tài khoản thật. Các expected dưới đây là thiết kế; không phải evidence Pass. ERR là nhãn BA không phân loại HTTP.

## 1. Môi trường, fixture và quan sát

- Phiên bản đích: commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`; UI/OS/build hash khi chạy phải ghi vào test run. Harness QA chưa được triển khai trong bộ tài liệu này. Có thể thực thi thủ công UI hoặc dùng entry point backend đã dẫn; không xem mô tả bên dưới là API giả đã tồn tại.
- Mỗi TC tạo thư mục dữ liệu và profile/collection tạm riêng, không chứa dữ liệu cá nhân. Gọi các note/card ID qua factory fixture, không dùng ID thật. File TSV/ảnh/package tạo từ dữ liệu tổng hợp ghi tại Data. Auto-sync tắt; addon tắt trừ TC addon có QA callback cục bộ không network.
- Snapshot trước/sau gồm note fields/tags/GUID, card id/note_id/ordinal/deck/queue/due/interval/reps/lapses, revlog count/rating/time, deck stats, file danh sách/hash theo điều kiện từng TC. Đọc backend hoặc DB snapshot sau khi transaction đóng, không sửa DB đang mở. Các ID BR/ERR nguồn là oracle, không ép UI hiển thị chuỗi mã BA.
- Clock mặc định t0=2026-11-02T00:00:00Z, trừ case ghi clock riêng (như TC-ANKI-067); ghi timezone/rollover riêng cho scheduler. Backup dùng clock SystemTime và metadata file phù hợp OS; nếu không điều khiển được thì **blocked khi thực thi**, không đoán mốc. Mtime đặt t−1/t/t+1 giây. Freeze/seed ngẫu nhiên khi harness hỗ trợ; nếu có fuzz kiểm invariant/next-state theo nguồn, không tự đặt due date cố định.
- Sync dùng hai collection tạm với endpoint self-host/test cô lập, protocol tương thích, không credential production; cần người thực thi cung cấp fixture/harness hợp lệ trước test integration. Blocker môi trường không được biến thành kết quả Pass.
- Từng tổ hợp trong một TC là ví dụ độc lập: restore seed snapshot trước mỗi ví dụ, ghi actual riêng và kết luận cả TC chỉ khi mọi ví dụ có bằng chứng. Cả 86 TC hiện có Design Specified; fixture/harness chưa sẵn sàng là blocker thực thi, không phải bằng chứng Pass.

### Cleanup C0 áp dụng bắt buộc cho từng TC

Trong finally: đóng collection/UI fixture, gỡ callback/addon QA và fault injection, trả clock/timezone/random seed, dừng server/process do chính test khởi tạo, xóa duy nhất thư mục/profile/package/account test do TC tạo sau khi lưu evidence đã redacted. Không xóa user profile hay dùng chung server. Thư mục source upstream không thay đổi. Mỗi test bên dưới nhắc C0 và hạng mục đặc thù.

## 2. Test cases chi tiết

### TC-ANKI-001 — Lưu note hai chiều

- **Truy vết:** US-ANKI-01; AC-ANKI-001; FR FR-CNT-NOTE-001; BR BR-ANKI-001, BR-ANKI-003; ERR —.
- **Loại / entry surface:** happy / Backend note/card + Browser kiểm tra.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** collection tạm có NoteType BasicQA gồm Front/Back và hai template hợp lệ; Front=apple, Back=quả táo; deck QA.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Thêm note và đọc note/card đã lưu.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** một note giữ hai field; hai card có cùng note_id và ordinal khác nhau, mỗi card có lịch riêng.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95).

### TC-ANKI-002 — Sai số field

- **Truy vết:** US-ANKI-01; AC-ANKI-002; FR FR-CNT-NOTE-001; BR BR-ANKI-001; ERR ERR-ANKI-000-01.
- **Loại / entry surface:** negative / Backend note/card + Browser kiểm tra.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** NoteType có hai field; note thử chỉ có một field apple; đã chụp số note/card.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Gọi đường lưu note của backend.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** guard từ chối ERR-ANKI-000-01; note thử không được lưu thành note hợp lệ; không gán HTTP/UI message.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95); [rslib/src/notes/mod.rs:198](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L198).

### TC-ANKI-003 — Chỉ thêm ordinal còn thiếu

- **Truy vết:** US-ANKI-01; AC-ANKI-003; FR FR-CNT-NOTE-001; BR BR-ANKI-003; ERR —.
- **Loại / entry surface:** boundary / Backend note/card + Browser kiểm tra.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** note N có card ordinal 0 và lịch đã học; template ordinal 1 trước rỗng, nay Back được điền quả táo.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Lưu note rồi lưu lại cùng nội dung lần nữa.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** ordinal 1 được thêm đúng một card; ordinal 0 giữ card ID và lịch; lần lưu lặp không tạo card cùng ordinal.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95).

### TC-ANKI-004 — Card rỗng và fallback cấp lõi

- **Truy vết:** US-ANKI-01; AC-ANKI-004; FR FR-CNT-NOTE-001; BR BR-ANKI-003; ERR —.
- **Loại / entry surface:** boundary / Backend note/card + Browser kiểm tra.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** hai fixture riêng: A có card đã học rồi xóa field làm mặt hỏi rỗng; B chưa có card, mọi template rỗng và ensure_not_empty=true.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Lưu A và chạy sinh card cấp lõi B.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** A không bị tự xóa card cũ; B sinh ordinal 0; không suy ra mọi caller UI bật ensure_not_empty.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95); [docs-site/manual/templates/generation.mdx:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/templates/generation.mdx#L25).

### TC-ANKI-005 — NoteType tối thiểu hợp lệ

- **Truy vết:** US-ANKI-02; AC-ANKI-005; FR FR-CNT-TYPE-001; BR BR-ANKI-002, BR-ANKI-003; ERR —.
- **Loại / entry surface:** happy / Backend NoteType/card generation.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** collection tạm chưa có loại QA-Min; tên QA-Min, một field Front, một template hỏi {{Front}} và đáp án {{Front}}.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Thêm NoteType rồi tạo note Front=alpha.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** NoteType được lưu với một field/một template; note sinh card phù hợp.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/notetype/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/mod.rs#L484); [proto/anki/notetypes.proto:102](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/notetypes.proto#L102); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95).

### TC-ANKI-006 — Thiếu cấu trúc bắt buộc

- **Truy vết:** US-ANKI-02; AC-ANKI-006; FR FR-CNT-TYPE-001; BR BR-ANKI-002; ERR ERR-ANKI-000-02.
- **Loại / entry surface:** negative / Backend NoteType/card generation.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** ba fixture NoteType độc lập: không field; không template; tên rỗng tại guard sau bước chuẩn hóa; không dùng UI để suy đoán thông báo.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Gọi validation/lưu tại đúng guard của từng fixture.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** cả ba bị từ chối theo ERR-ANKI-000-02; ghi guard thực tế, không áp mã HTTP.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/notetype/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/mod.rs#L484); [proto/anki/notetypes.proto:102](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/notetypes.proto#L102).

### TC-ANKI-007 — Template override deck

- **Truy vết:** US-ANKI-02; AC-ANKI-007; FR FR-CNT-TYPE-001; BR BR-ANKI-003; ERR —.
- **Loại / entry surface:** boundary / Backend NoteType/card generation.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** note có hai template đều render hỏi; deck chọn QA-A; riêng template 1 override QA-B.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Sinh card cho note.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** card template 0 ở QA-A, template 1 ở QA-B; một note không buộc các card cùng deck.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/notetype/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/mod.rs#L484); [proto/anki/notetypes.proto:102](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/notetypes.proto#L102); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95); [rslib/src/notetype/cardgen.rs:141](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L141).

### TC-ANKI-008 — Hai số cloze tạo hai card

- **Truy vết:** US-ANKI-03; AC-ANKI-008; FR FR-CNT-CLOZ-001; BR BR-ANKI-001, BR-ANKI-004; ERR —.
- **Loại / entry surface:** happy / Add/Cloze + Browser.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** Cloze NoteType đúng số field; Text={{c1::alpha}} và {{c2::beta}}.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Thêm note cloze.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** một note tạo hai card tương ứng c1/c2; cùng dùng template cloze đầu tiên.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/notetype/cardgen.rs:160](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L160); [docs-site/manual/editing.mdx:364](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L364); [rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194).

### TC-ANKI-009 — Cloze không bỏ qua field guard

- **Truy vết:** US-ANKI-03; AC-ANKI-009; FR FR-CNT-CLOZ-001; BR BR-ANKI-001; ERR ERR-ANKI-000-01.
- **Loại / entry surface:** negative / Add/Cloze + Browser.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** Cloze NoteType có hai field; note cloze thử có một field chứa {{c1::alpha}}.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Gọi lưu note qua backend.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** guard ERR-ANKI-000-01 từ chối note có số field sai dù chuỗi cloze hợp lệ.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/notetype/cardgen.rs:160](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L160); [docs-site/manual/editing.mdx:364](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L364); [rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194); [rslib/src/notes/mod.rs:198](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L198).

### TC-ANKI-010 — Nhiều đoạn cùng số

- **Truy vết:** US-ANKI-03; AC-ANKI-010; FR FR-CNT-CLOZ-001; BR BR-ANKI-004; ERR —.
- **Loại / entry surface:** boundary / Add/Cloze + Browser.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** Text={{c1::alpha}} và {{c1::beta}}; các field khác đủ theo NoteType.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Thêm note rồi xem card được sinh.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** chỉ một card cho c1; khi hiện câu hỏi cả hai đoạn c1 được che cùng lượt.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/notetype/cardgen.rs:160](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L160); [docs-site/manual/editing.mdx:364](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L364).

### TC-ANKI-011 — Hai vùng che riêng

- **Truy vết:** US-ANKI-04; AC-ANKI-011; FR FR-CNT-IMGO-001; BR BR-ANKI-005; ERR —.
- **Loại / entry surface:** happy / Editor Image Occlusion + Empty Cards.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** ảnh QA.png tự tạo không dữ liệu cá nhân; hai shape che hai vùng, không group.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Lưu note Image Occlusion.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** một note dùng cấu trúc cloze/image occlusion, sinh card theo hai vùng được đánh số riêng.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/image_occlusion/notetype.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/image_occlusion/notetype.rs#L59); [docs-site/manual/editing.mdx:504](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L504).

### TC-ANKI-012 — Xóa shape không tự xóa card

- **Truy vết:** US-ANKI-04; AC-ANKI-012; FR FR-CNT-IMGO-001; BR BR-ANKI-003, BR-ANKI-005; ERR —.
- **Loại / entry surface:** negative / Editor Image Occlusion + Empty Cards.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** note Image Occlusion có hai shape và hai card; card thứ hai đã có lịch.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Xóa shape thứ hai rồi lưu và mở Empty Cards để kiểm tra, chưa xác nhận xóa.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** card cũ tương ứng không tự bị xóa; Empty Cards cho phép nhận diện card không còn nội dung che.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/image_occlusion/notetype.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/image_occlusion/notetype.rs#L59); [docs-site/manual/editing.mdx:504](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L504); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95); [docs-site/manual/editing.mdx:531](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L531).

### TC-ANKI-013 — Overlay không tăng số card

- **Truy vết:** US-ANKI-04; AC-ANKI-013; FR FR-CNT-IMGO-001; BR BR-ANKI-005; ERR —.
- **Loại / entry surface:** boundary / Editor Image Occlusion + Empty Cards.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** note ảnh có một shape và một card; thêm text overlay QA label.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Lưu lại note.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** vẫn một card do shape; overlay hiển thị nội dung, không sinh card bổ sung.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/image_occlusion/notetype.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/image_occlusion/notetype.rs#L59); [docs-site/manual/editing.mdx:504](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L504); [docs-site/manual/editing.mdx:531](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L531).

### TC-ANKI-014 — Deck cha gồm descendants

- **Truy vết:** US-ANKI-05; AC-ANKI-014; FR FR-ORG-DECK-001; BR BR-ANKI-006, BR-ANKI-012; ERR —.
- **Loại / entry surface:** happy / Deck Browser + scheduler queue.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** QA-Parent có card A; QA-Parent::Child có B; QA-Other có C; cả ba đủ hạn, limit đủ và không bury.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Chọn QA-Parent và xây queue.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** phạm vi lấy A và B; C không thuộc deck được chọn hoặc descendants.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [docs-site/manual/getting-started.mdx:75](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/getting-started.mdx#L75); [rslib/src/scheduler/queue/builder/mod.rs:135](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/mod.rs#L135); [docs-site/manual/studying.mdx:10](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L10); [rslib/src/decks/limits.rs:98](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/decks/limits.rs#L98).

### TC-ANKI-015 — Không kéo sibling ngoài phạm vi

- **Truy vết:** US-ANKI-05; AC-ANKI-015; FR FR-ORG-DECK-001; BR BR-ANKI-006; ERR —.
- **Loại / entry surface:** negative / Deck Browser + scheduler queue.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** hai card A/B chung note; A ở QA-Selected, B ở QA-Other; cả hai đủ hạn, bury siblings tắt.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Chọn học QA-Selected.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** B không vào phạm vi chỉ vì có chung note với A; note không có một deck owner chung.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [docs-site/manual/getting-started.mdx:75](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/getting-started.mdx#L75); [rslib/src/scheduler/queue/builder/mod.rs:135](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/mod.rs#L135); [docs-site/manual/studying.mdx:10](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L10).

### TC-ANKI-016 — Chuyển một sibling

- **Truy vết:** US-ANKI-05; AC-ANKI-016; FR FR-ORG-DECK-001; BR BR-ANKI-006; ERR —.
- **Loại / entry surface:** boundary / Deck Browser + scheduler queue.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** note N có card A/B cùng QA-A; queue chưa xây; QA-B tồn tại.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Chuyển riêng A sang QA-B rồi đọc cả hai card.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** A thuộc QA-B và B vẫn thuộc QA-A; cùng giữ note_id N.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [docs-site/manual/getting-started.mdx:75](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/getting-started.mdx#L75); [rslib/src/scheduler/queue/builder/mod.rs:135](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/mod.rs#L135); [docs-site/manual/studying.mdx:10](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L10); [docs-site/manual/editing.mdx:217](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L217).

### TC-ANKI-017 — Tìm nội dung field

- **Truy vết:** US-ANKI-06; AC-ANKI-017; FR FR-ORG-SRCH-001; BR BR-ANKI-007; ERR —.
- **Loại / entry surface:** happy / Browse Cards/search/tags/flags.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** N1 có Front=alpha, N2 có Front=beta; không field nào khác chứa alpha.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Tìm alpha trong Browse chế độ Cards.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** kết quả là các card của N1; không có card N2.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226).

### TC-ANKI-018 — Text thường không tìm tag

- **Truy vết:** US-ANKI-06; AC-ANKI-018; FR FR-ORG-SRCH-001; BR BR-ANKI-007; ERR —.
- **Loại / entry surface:** negative / Browse Cards/search/tags/flags.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** N1 có tag=needle nhưng field chỉ alpha; N2 có field=needle nhưng không tag đó.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Tìm needle rồi tìm tag:needle trong Browse, dùng snapshot kết quả riêng.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** query needle trả card N2, không N1; query tag:needle trả card N1.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226).

### TC-ANKI-019 — Kết hợp toán tử

- **Truy vết:** US-ANKI-06; AC-ANKI-019; FR FR-ORG-SRCH-001; BR BR-ANKI-007; ERR —.
- **Loại / entry surface:** boundary / Browse Cards/search/tags/flags.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** ba note: N1 field alpha và tag qa; N2 field beta và tag qa; N3 field beta không tag qa.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Tìm (alpha or beta) tag:qa rồi tìm cùng biểu thức với -tag:qa.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** truy vấn đầu trả card N1/N2; truy vấn sau chỉ trả card N3; AND/OR/NOT giữ phạm vi đã mô tả.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226).

### TC-ANKI-020 — Answer sau khi xem đáp án

- **Truy vết:** US-ANKI-07; AC-ANKI-020; FR FR-LRN-REV-001; BR BR-ANKI-006, BR-ANKI-008, BR-ANKI-011; ERR —.
- **Loại / entry surface:** happy / Reviewer UI + backend AnswerCard.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** một card Review tới hạn ở QA; đã ghi current state, reps/lapses, revlog count và deck stats; clock=t0; không addon.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Study Now, Show Answer rồi chọn Good một lần.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** answer hợp lệ commit trạng thái card, một revlog và deck stats tương ứng; Good là phản hồi nhớ được, không xác minh hiểu biết thực tế.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [docs-site/manual/studying.mdx:40](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L40); [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315); [docs-site/manual/studying.mdx:10](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L10); [docs-site/manual/studying.mdx:58](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L58).

### TC-ANKI-021 — Current state đã thay đổi

- **Truy vết:** US-ANKI-07; AC-ANKI-021; FR FR-LRN-REV-001; BR BR-ANKI-011; ERR ERR-ANKI-000-03.
- **Loại / entry surface:** negative / Reviewer UI + backend AnswerCard.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** đã lấy current state S của card; sửa trạng thái nền khiến current state thật khác S ngoài elapsed seconds; chụp lại card/log/stats sau sửa.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Gửi AnswerCard dựa trên S.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** ERR-ANKI-000-03; không thêm revlog hoặc cập nhật card/stats do answer bị từ chối; thay đổi hợp lệ trước answer vẫn còn.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [docs-site/manual/studying.mdx:40](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L40); [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315); [rslib/src/scheduler/answering/mod.rs:335](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L335).

### TC-ANKI-022 — Chưa xem đáp án

- **Truy vết:** US-ANKI-07; AC-ANKI-022; FR FR-LRN-REV-001; BR BR-ANKI-008; ERR —.
- **Loại / entry surface:** boundary / Reviewer UI + backend AnswerCard.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** reviewer đang ở question của card QA, chưa Show Answer; chụp revlog count và card state.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Gửi thao tác rating qua reviewer trước khi vào trạng thái answer.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** reviewer bỏ qua thao tác; không gửi answer hợp lệ và không tạo revlog cho lần nhấn này.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [docs-site/manual/studying.mdx:40](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L40); [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315); [docs-site/manual/studying.mdx:58](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L58); [qt/aqt/reviewer.py:532](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/reviewer.py#L532).

### TC-ANKI-023 — Cap thời gian answer

- **Truy vết:** US-ANKI-07; AC-ANKI-023; FR FR-LRN-REV-001; BR BR-ANKI-011; ERR —.
- **Loại / entry surface:** boundary / Reviewer UI + backend AnswerCard.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** preset cap_answer_time_to_secs=60; ba bản sao card độc lập có elapsed answer 59, 60, 61 giây; đã hiện đáp án.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Gửi Good trên mỗi fixture bằng clock kiểm soát.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** revlog lưu thời gian tương ứng 59, 60, 60 giây; không lưu vượt cap 60.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [docs-site/manual/studying.mdx:40](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L40); [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315); [rslib/src/scheduler/answering/mod.rs:330](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L330).

### TC-ANKI-024 — Learning theo bốn rating

- **Truy vết:** US-ANKI-08; AC-ANKI-024; FR FR-LRN-SCH-001; BR BR-ANKI-009, BR-ANKI-013; ERR —.
- **Loại / entry surface:** happy / Scheduler states/AnswerCard cấp lõi.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** learning steps [1m,10m], legacy, card ở bước đầu; dùng bốn bản sao độc lập cùng cấu hình.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Tính next states rồi chọn lần lượt Again, Hard, Good, Easy trên từng bản sao.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** Again về bước đầu; Hard dùng trung bình hai bước đầu; Good tiến bước; Easy sang Review; không khẳng định due số học nếu fuzz được áp dụng.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [proto/anki/scheduler.proto:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L80); [rslib/src/scheduler/states/review.rs:64](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L64); [rslib/src/scheduler/states/learning.rs:39](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/learning.rs#L39); [rslib/src/scheduler/answering/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L484); [rslib/src/scheduler/states/steps.rs:38](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/steps.rs#L38).

### TC-ANKI-025 — Quên Review và Again khi học lại

- **Truy vết:** US-ANKI-08; AC-ANKI-025; FR FR-LRN-SCH-001; BR BR-ANKI-010; ERR —.
- **Loại / entry surface:** negative / Scheduler states/AnswerCard cấp lõi.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** card Review lapse=2, relearning steps [1m,10m], chưa leech; clock kiểm soát.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Chọn Again ở Review rồi Again trong Relearning.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** lapse tăng thành 3 ở thất bại Review; tiếp tục bằng 3 khi Again trong cùng chuỗi Relearning.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [proto/anki/scheduler.proto:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L80); [rslib/src/scheduler/states/review.rs:64](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L64); [rslib/src/scheduler/states/review.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L95).

### TC-ANKI-026 — Hard với một learning step

- **Truy vết:** US-ANKI-08; AC-ANKI-026; FR FR-LRN-SCH-001; BR BR-ANKI-009; ERR —.
- **Loại / entry surface:** boundary / Scheduler states/AnswerCard cấp lõi.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** legacy learning có đúng một step 10 phút; card tại bước đầu; lấy trạng thái tính toán trước fuzz nếu có.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Tính Hard next state.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** hard delay cơ sở là 15 phút theo 1,5 lần step; không áp công thức trung bình hai step không tồn tại.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [proto/anki/scheduler.proto:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L80); [rslib/src/scheduler/states/review.rs:64](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L64); [rslib/src/scheduler/states/learning.rs:39](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/learning.rs#L39); [rslib/src/scheduler/states/steps.rs:55](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/steps.rs#L55).

### TC-ANKI-027 — Reject state lỗi trước xếp lịch

- **Truy vết:** US-ANKI-08; AC-ANKI-027; FR FR-LRN-SCH-001; BR BR-ANKI-010, BR-ANKI-011; ERR ERR-ANKI-000-03.
- **Loại / entry surface:** negative / Scheduler states/AnswerCard cấp lõi.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** card Review đã được thay current state thực sau khi UI nhận S; không chỉ chênh elapsed seconds.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Gửi Again với current state S.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** ERR-ANKI-000-03; không tăng lapse, không ghi revlog hoặc lịch mới từ answer này.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [proto/anki/scheduler.proto:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L80); [rslib/src/scheduler/states/review.rs:64](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L64); [rslib/src/scheduler/states/review.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L95); [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315); [rslib/src/scheduler/answering/mod.rs:335](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L335).

### TC-ANKI-028 — Ưu tiên today, deck, preset

- **Truy vết:** US-ANKI-09; AC-ANKI-028; FR FR-LRN-LIM-001; BR BR-ANKI-012; ERR —.
- **Loại / entry surface:** happy / Deck Options + queue builder.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** preset new limit=20, deck limit=10, today override=3, đã học new=1; review limit dư; có 30 new đủ điều kiện.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Xây queue hôm nay.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** còn tối đa 2 new theo today override; không chọn mức 10 hoặc 20.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/decks/limits.rs:98](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/decks/limits.rs#L98); [rslib/src/scheduler/queue/builder/gathering.rs:23](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/gathering.rs#L23).

### TC-ANKI-029 — Review limit bằng không

- **Truy vết:** US-ANKI-09; AC-ANKI-029; FR FR-LRN-LIM-001; BR BR-ANKI-012; ERR —.
- **Loại / entry surface:** negative / Deck Options + queue builder.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** hai collection giống nhau có new và due review; review remaining=0, new remaining=5; một tắt và một bật New cards ignore review limit.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Xây queue ở từng collection.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** khi tắt không lấy thêm new do review limit; khi bật có thể lấy new tới new remaining, review vẫn bị chặn.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/decks/limits.rs:98](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/decks/limits.rs#L98); [rslib/src/scheduler/queue/builder/gathering.rs:23](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/gathering.rs#L23).

### TC-ANKI-030 — Intraday khác interday

- **Truy vết:** US-ANKI-09; AC-ANKI-030; FR FR-LRN-LIM-001; BR BR-ANKI-012; ERR —.
- **Loại / entry surface:** boundary / Deck Options + queue builder.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** review remaining=0; có một intraday learning đã đến giờ và một interday learning đã tới ngày; không giới hạn khác.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Xây queue tại clock t0.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** intraday vẫn đủ điều kiện; interday chịu review limit và không được lấy trong fixture này.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/decks/limits.rs:98](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/decks/limits.rs#L98); [rslib/src/scheduler/queue/builder/gathering.rs:23](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/gathering.rs#L23).

### TC-ANKI-031 — Giới hạn cây deck

- **Truy vết:** US-ANKI-09; AC-ANKI-031; FR FR-LRN-LIM-001; BR BR-ANKI-006, BR-ANKI-012; ERR —.
- **Loại / entry surface:** boundary / Deck Options + queue builder.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** QA-P limit tổng=3; QA-P::A limit=2 và QA-P::B limit=2; mỗi con có 4 card đủ điều kiện; các counts bằng 0.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Chọn QA-P xây queue; lặp trên fixture mới với card count đã học bằng limit.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** tổng các con không vượt 3 và từng con không vượt 2; khi đã học đúng limit không còn quota tương ứng; kiểm riêng cờ Limits start from top khi chọn con.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/decks/limits.rs:98](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/decks/limits.rs#L98); [rslib/src/scheduler/queue/builder/gathering.rs:23](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/gathering.rs#L23); [docs-site/manual/studying.mdx:10](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L10); [rslib/src/scheduler/queue/builder/mod.rs:130](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/mod.rs#L130).

### TC-ANKI-032 — FSRS ở phạm vi collection

- **Truy vết:** US-ANKI-10; AC-ANKI-032; FR FR-LRN-FSRS-001; BR BR-ANKI-013, BR-ANKI-014; ERR —.
- **Loại / entry surface:** happy / Deck Options/FSRS backend.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** hai deck dùng hai preset trong cùng collection; có lịch sử nhân tạo; cấu hình retention/params hợp lệ.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Bật FSRS và đọc cấu hình cùng next states của card thuộc cả hai preset.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** cờ bật áp dụng toàn collection; next states theo nhánh FSRS dùng memory state/retention/params, không còn diễn giải bằng công thức ease SM-2.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/scheduler/answering/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L484); [docs-site/manual/deck-options.mdx:406](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L406); [docs-site/manual/deck-options.mdx:500](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L500).

### TC-ANKI-033 — Không reschedule khi tùy chọn tắt

- **Truy vết:** US-ANKI-10; AC-ANKI-033; FR FR-LRN-FSRS-001; BR BR-ANKI-014; ERR —.
- **Loại / entry surface:** negative / Deck Options/FSRS backend.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** FSRS đang bật; card đã có due D; dùng bản sao collection và chụp due trước sửa; reschedule on change tắt.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Đổi desired retention hợp lệ rồi lưu mà không học card.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** không tự tính lại toàn bộ due cũ; card fixture giữ D do thao tác đổi cấu hình này.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/scheduler/answering/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L484); [docs-site/manual/deck-options.mdx:406](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L406); [docs-site/manual/deck-options.mdx:500](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L500).

### TC-ANKI-034 — Reschedule là lựa chọn riêng

- **Truy vết:** US-ANKI-10; AC-ANKI-034; FR FR-LRN-FSRS-001; BR BR-ANKI-014; ERR —.
- **Loại / entry surface:** boundary / Deck Options/FSRS backend.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** hai bản sao cùng card/history và cấu hình; cùng thay retention; một bật và một tắt reschedule on change.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Lưu cấu hình ở từng bản sao rồi kiểm tra tác vụ reschedule và due.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** nhánh bật thực hiện tính lại lịch cho scope bị ảnh hưởng; nhánh tắt không thực hiện đợt reschedule; không bắt buộc mọi card đều có ngày mới khác ngày cũ.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/scheduler/answering/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L484); [docs-site/manual/deck-options.mdx:406](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L406); [docs-site/manual/deck-options.mdx:500](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L500).

### TC-ANKI-035 — Optimize không có lịch sử giữ nguyên tham số

- **Truy vết:** US-ANKI-10; AC-ANKI-035; FR FR-LRN-FSRS-001; BR BR-ANKI-014; ERR —.
- **Loại / entry surface:** boundary / Deck Options Optimize current preset và ComputeFsrsParams nội bộ.
- **Preconditions:** môi trường cô lập ở mục 1, locale English để đối chiếu FTL; đã lưu FSRS/preset trước snapshot; không add-on hoặc sync song song; harness quan sát backend và UI thật, không dùng response giả để chứng minh backend
- **Data / trạng thái đầu:** collection tạm F035-empty có 0 note/card/revlog; deck D035 dùng preset P035 đã lưu, FSRS bật, fsrs_params_4/5/6 đều []; search và ignore-before date rỗng, relearnSteps=[10], healthCheck=false, reschedule=false; mở lại Deck Options, không có assignment chưa lưu hoặc tác vụ đang chạy.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.



**Steps**

1. Dựng F035-empty, lưu rồi mở lại Deck Options; chụp counts và các mảng params trong form/preset.
2. Bấm Optimize current preset một lần; kiểm request search preset:"P035" -is:suspended, current_params=[], ignore_revlogs_before_ms=0, num_of_relearning_steps=1, health_check=false.
3. Đọc response thành công: params=[], fsrs_items=0, optional health_check_passed vắng mặt.
4. Chờ alert theo sự kiện UI; đối chiếu khóa deck-config-fsrs-params-no-reviews trong FTL English, đóng alert; kiểm computingParams=false và params form vẫn [].
5. So snapshot trước/sau Optimize, trước Save: preset params và counts không đổi; lưu actual riêng từng lớp quan sát rồi cleanup C0.

**Expected:** backend trả thành công params=[], fsrs_items=0, health_check_passed absent (không phải false); UI hiện khóa deck-config-fsrs-params-no-reviews; tham số form và preset đã lưu không đổi, counts note/card/revlog vẫn 0/0/0; computingParams trở về false.

**Giới hạn oracle:** 0 training item là nhánh return sớm, không phải lỗi thiếu 400/1000 reviews và không có mô hình cá nhân hóa mới. Không áp oracle này cho Optimize All hoặc preset assignment chưa lưu. Nếu chỉ quan sát UI thì lớp response backend vẫn chưa được kiểm thử. Source tĩnh, chưa chạy test.

**Cleanup:** C0; đóng collection/preset test, trả locale và clock, giữ evidence trước khi xóa duy nhất thư mục F035-empty.

**Nguồn oracle:** [ts/routes/deck-options/FsrsOptions.svelte:200](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L200); [ts/routes/deck-options/FsrsOptions.svelte:225](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L225); [ts/routes/deck-options/FsrsOptions.svelte:235](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L235); [rslib/src/scheduler/service/mod.rs:264](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/service/mod.rs#L264); [rslib/src/scheduler/fsrs/params.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L95); [proto/anki/scheduler.proto:357](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L357); [ftl/core/deck-config.ftl:495](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ftl/core/deck-config.ftl#L495).

### TC-ANKI-036 — Bury và unbury thủ công

- **Truy vết:** US-ANKI-11; AC-ANKI-036; FR FR-LRN-HIDE-001; BR BR-ANKI-015; ERR —.
- **Loại / entry surface:** happy / Browser/reviewer + scheduler clock.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** card A đang Review đủ hạn, có interval/lapse đã chụp, chưa suspended.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Bury A rồi unbury thủ công.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** A rời queue khi buried rồi có thể trở lại theo due/limit sau unbury; interval/lapse nền không bị biến thành một giai đoạn trí nhớ mới.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/scheduler/bury_and_suspend.rs:32](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L32); [rslib/src/scheduler/answering/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L194).

### TC-ANKI-037 — Không bury card suspended

- **Truy vết:** US-ANKI-11; AC-ANKI-037; FR FR-LRN-HIDE-001; BR BR-ANKI-015; ERR —.
- **Loại / entry surface:** negative / Browser/reviewer + scheduler clock.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** card A đã suspended; ghi queue và lịch nền.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Gọi bury A rồi xây queue.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** A vẫn suspended và không được biến thành buried; không được đưa lại vào queue.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/scheduler/bury_and_suspend.rs:32](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L32); [rslib/src/scheduler/answering/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L194).

### TC-ANKI-038 — Rollover khác ngày lịch máy

- **Truy vết:** US-ANKI-11; AC-ANKI-038; FR FR-LRN-HIDE-001; BR BR-ANKI-015; ERR —.
- **Loại / entry surface:** boundary / Browser/reviewer + scheduler clock.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** A buried, B suspended; clock scheduler có rollover R xác định; ba bản sao ở R−1s, R, R+1s.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Mở/xây lại queue để scheduler chạy xử lý ngày tại từng mốc.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** trước R A còn buried; tại/sau R A được unbury theo ngày scheduler; B vẫn suspended ở cả ba mốc.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/scheduler/bury_and_suspend.rs:32](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L32); [rslib/src/scheduler/answering/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L194).

### TC-ANKI-039 — Mốc leech dương và bằng không

- **Truy vết:** US-ANKI-11; AC-ANKI-039; FR FR-LRN-HIDE-001; BR BR-ANKI-016; ERR —.
- **Loại / entry surface:** boundary / Browser/reviewer + scheduler clock.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** fixture ngưỡng 8 có lapse sau answer lần lượt 7,8,9,11,12; fixture khác threshold=0; action Tag Only; dùng bản sao độc lập.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Tính trạng thái leech sau Review Again và commit answer khi phù hợp.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** phát leech ở 8 và 12, không phát mới ở 7/9/11; threshold=0 không kích hoạt; tag leech thuộc note; không tự xóa tag cũ khi không phát mới.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/scheduler/bury_and_suspend.rs:32](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L32); [rslib/src/scheduler/answering/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L194); [rslib/src/scheduler/states/review.rs:292](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L292).

### TC-ANKI-040 — Tag only khác Suspend

- **Truy vết:** US-ANKI-11; AC-ANKI-040; FR FR-LRN-HIDE-001; BR BR-ANKI-016; ERR —.
- **Loại / entry surface:** boundary / Browser/reviewer + scheduler clock.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** hai bản sao note có siblings A/B; A đang Review, lapse sắp chạm threshold; một action Tag Only, một action Suspend.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Trả lời Again cho A tại threshold.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** cả hai note có tag leech; Tag Only không suspend A, Suspend làm A suspended; không tự suy ra sibling B cũng suspended.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/scheduler/bury_and_suspend.rs:32](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L32); [rslib/src/scheduler/answering/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L194); [rslib/src/scheduler/states/review.rs:292](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L292).

### TC-ANKI-041 — Build rồi Empty không copy card

- **Truy vết:** US-ANKI-12; AC-ANKI-041; FR FR-LRN-FILT-001; BR BR-ANKI-017; ERR —.
- **Loại / entry surface:** happy / Filtered deck + scheduler states.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** QA-Home có hai card hợp query tag:qa; filtered QA-F có limit=2; chụp card IDs.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Build QA-F rồi Empty.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** hai card tạm thuộc QA-F và giữ home deck; Empty trả về QA-Home với cùng IDs, không xóa hoặc tạo bản sao.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/scheduler/filtered/mod.rs:123](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L123); [rslib/src/scheduler/states/preview_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/preview_filter.rs#L25).

### TC-ANKI-042 — Không có card được phép lấy

- **Truy vết:** US-ANKI-12; AC-ANKI-042; FR FR-LRN-FILT-001; BR BR-ANKI-017; ERR ERR-ANKI-000-04.
- **Loại / entry surface:** negative / Filtered deck + scheduler states.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** query tag:qa chỉ khớp card suspended, buried hoặc đã thuộc filtered khác; allow_empty=false.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Build filtered mới.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** trả ERR-ANKI-000-04 / SearchReturnedNoCards; không lấy các card bị loại để làm đầy filtered.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/scheduler/filtered/mod.rs:123](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L123); [rslib/src/scheduler/states/preview_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/preview_filter.rs#L25); [rslib/src/scheduler/filtered/mod.rs:178](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L178).

### TC-ANKI-043 — Limit một và Rebuild

- **Truy vết:** US-ANKI-12; AC-ANKI-043; FR FR-LRN-FILT-001; BR BR-ANKI-017; ERR —.
- **Loại / entry surface:** boundary / Filtered deck + scheduler states.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** QA-F limit=1 có card cũ A; search mới chỉ khớp B/C, order xác định đưa B trước C.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Rebuild QA-F.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** A được trả home; chỉ B vào QA-F, C không được lấy vượt limit; toàn collection không tăng card count.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/scheduler/filtered/mod.rs:123](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L123); [rslib/src/scheduler/states/preview_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/preview_filter.rs#L25).

### TC-ANKI-044 — Reschedule dùng home deck

- **Truy vết:** US-ANKI-12; AC-ANKI-044; FR FR-LRN-FILT-001; BR BR-ANKI-018; ERR —.
- **Loại / entry surface:** happy / Filtered deck + scheduler states.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** filtered bật reschedule; home deck có preset P; hai bản sao card Review: Good về Review, Again vào Relearning có steps.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Trả lời trên từng bản sao theo next states từ home preset.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** Good chuyển Review và trả home; Again ở Relearning còn trong filtered; lịch thay đổi theo home settings.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/scheduler/filtered/mod.rs:123](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L123); [rslib/src/scheduler/states/preview_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/preview_filter.rs#L25); [rslib/src/scheduler/states/rescheduling_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/rescheduling_filter.rs#L25).

### TC-ANKI-045 — Preview delay bằng không

- **Truy vết:** US-ANKI-12; AC-ANKI-045; FR FR-LRN-FILT-001; BR BR-ANKI-019; ERR —.
- **Loại / entry surface:** boundary / Filtered deck + scheduler states.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** reschedule tắt; ba fixture độc lập: Good delay=0, Good delay=60s, Easy; giữ last_review_time trước học.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Trả lời rồi đọc card, home/queue và revlog.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** Good delay=0 và Easy kết thúc và phục hồi home/queue; Good 60s tiếp tục preview; có revlog nhưng last_review_time không cập nhật như normal study.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/scheduler/filtered/mod.rs:123](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L123); [rslib/src/scheduler/states/preview_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/preview_filter.rs#L25); [rslib/src/scheduler/answering/preview.rs:17](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/preview.rs#L17); [rslib/src/scheduler/answering/mod.rs:341](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L341).

### TC-ANKI-046 — Text update giữ lịch

- **Truy vết:** US-ANKI-13; AC-ANKI-046; FR FR-DAT-TEXT-001; BR BR-ANKI-001, BR-ANKI-020; ERR —.
- **Loại / entry surface:** happy / Text Import + row log.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** note BasicQA GUID=gQA, Front=alpha, Back=old có card đã học ở QA-A; UTF-8 TSV GUID=gQA, Front=alpha, Back=new; mapping đúng và Update.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Nhập TSV rồi đọc note/card.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** Back thành new; card hiện có giữ ID, deck, due/interval và lịch; không tạo note thứ hai cho GUID đó.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/import_export/text/import.rs:250](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L250); [rslib/src/import_export/text/import.rs:318](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L318); [rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194).

### TC-ANKI-047 — First field rỗng không chặn hàng sau

- **Truy vết:** US-ANKI-13; AC-ANKI-047; FR FR-DAT-TEXT-001; BR BR-ANKI-020; ERR ERR-ANKI-000-05.
- **Loại / entry surface:** negative / Text Import + row log.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** UTF-8 TSV gồm dòng 1 first field rỗng, dòng 2 Front=valid; NoteType/deck hợp lệ và mapping đủ.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Import file rồi đọc log và note count.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** dòng 1 thuộc log.empty_first_field theo ERR-ANKI-000-05; dòng 2 vẫn được xử lý; không tạo note hợp lệ từ dòng 1.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/import_export/text/import.rs:250](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L250); [rslib/src/import_export/text/import.rs:318](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L318); [rslib/src/import_export/text/import.rs:252](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L252).

### TC-ANKI-048 — Không resolve NoteType/deck

- **Truy vết:** US-ANKI-13; AC-ANKI-048; FR FR-DAT-TEXT-001; BR BR-ANKI-020; ERR ERR-ANKI-000-06.
- **Loại / entry surface:** negative / Text Import + row log.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** hai hàng có first field hợp lệ; hàng A tham chiếu NoteType ID không tồn tại; hàng B có NoteType hợp lệ nhưng deck ID không tồn tại; dùng ID, không tên deck mới.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Import rồi đọc row log.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** A thuộc missing_notetype, B thuộc missing_deck theo ERR-ANKI-000-06; không nhập hai hàng như added.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/import_export/text/import.rs:250](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L250); [rslib/src/import_export/text/import.rs:318](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L318); [rslib/src/import_export/text/import.rs:266](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L266).

### TC-ANKI-049 — GUID trùng nhưng type xung đột

- **Truy vết:** US-ANKI-13; AC-ANKI-049; FR FR-DAT-TEXT-001; BR BR-ANKI-020; ERR ERR-ANKI-000-07.
- **Loại / entry surface:** negative / Text Import + row log.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** note hiện có GUID=gQA kiểu BasicQA; hàng nhập GUID=gQA nhưng NoteType khác không tương thích, first field không rỗng.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Import với Update.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** row log conflicting theo ERR-ANKI-000-07; note hiện có không được cập nhật như một match hợp lệ.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/import_export/text/import.rs:250](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L250); [rslib/src/import_export/text/import.rs:318](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L318); [rslib/src/import_export/text/import.rs:401](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L401).

### TC-ANKI-050 — Duplicate policy và ưu tiên GUID

- **Truy vết:** US-ANKI-13; AC-ANKI-050; FR FR-DAT-TEXT-001; BR BR-ANKI-020; ERR —.
- **Loại / entry surface:** boundary / Text Import + row log.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** các bản sao collection có một note alpha/BasicQA; các hàng lần lượt không GUID cùng first field, và GUID=gQA đã tồn tại; chọn từng policy Update/Preserve/Duplicate.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Nhập từng tổ hợp vào bản sao độc lập.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** không GUID áp policy first-field/NoteType: cập nhật, giữ hoặc thêm bản sao; có GUID đã tồn tại không tạo bản sao mới dù Duplicate; chụp log từng nhánh.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/import_export/text/import.rs:250](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L250); [rslib/src/import_export/text/import.rs:318](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L318).

### TC-ANKI-051 — apkg giữ lịch card cũ

- **Truy vết:** US-ANKI-14; AC-ANKI-051; FR FR-DAT-PKG-001; BR BR-ANKI-021; ERR —.
- **Loại / entry surface:** happy / Package import/export + collection snapshot.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** collection có note GUID=gQA card ordinal 0 đã học; apkg có note cùng GUID mới hơn, ordinal 0 lịch khác và ordinal 1 mới với log có ID duy nhất; cùng NoteType Normal schema hai template; IfNewer.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Import apkg.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** note được cập nhật; card ordinal 0 giữ lịch hiện tại và không nhập log của card đó từ gói; ordinal 1 được thêm và log duy nhất của card mới được nhập.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/import_export/package/apkg/import/notes.rs:333](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L333); [rslib/src/import_export/package/apkg/import/cards.rs:99](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/cards.rs#L99); [rslib/src/import_export/package/colpkg/import.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/colpkg/import.rs#L31).

### TC-ANKI-052 — Không merge Normal và Cloze

- **Truy vết:** US-ANKI-14; AC-ANKI-052; FR FR-DAT-PKG-001; BR BR-ANKI-021; ERR ERR-ANKI-000-08.
- **Loại / entry surface:** negative / Package import/export + collection snapshot.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** collection có NoteType Normal; apkg yêu cầu merge NoteType tương ứng nhưng loại Cloze; bật merge.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Import apkg qua đường merge NoteType.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** trả ERR-ANKI-000-08 / ImportError::NotetypeKindMergeConflict; không báo merge Normal/Cloze thành công.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/import_export/package/apkg/import/notes.rs:333](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L333); [rslib/src/import_export/package/apkg/import/cards.rs:99](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/cards.rs#L99); [rslib/src/import_export/package/colpkg/import.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/colpkg/import.rs#L31); [rslib/src/import_export/package/apkg/import/notes.rs:234](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L234).

### TC-ANKI-053 — Ranh giới mtime và policy

- **Truy vết:** US-ANKI-14; AC-ANKI-053; FR FR-DAT-PKG-001; BR BR-ANKI-021; ERR —.
- **Loại / entry surface:** boundary / Package import/export + collection snapshot.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** note local mtime=t; các apkg cùng GUID với mtime=t−1,t,t+1 và nội dung khác; thử IfNewer/Always/Never trên bản sao độc lập.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Import mỗi tổ hợp và so nội dung note.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** IfNewer chỉ cập nhật t+1; Always cập nhật khi mtime khác t nhưng bỏ t; Never không cập nhật note cũ; đây là As-Is source, không diễn giải Always vô điều kiện.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/import_export/package/apkg/import/notes.rs:333](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L333); [rslib/src/import_export/package/apkg/import/cards.rs:99](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/cards.rs#L99); [rslib/src/import_export/package/colpkg/import.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/colpkg/import.rs#L31); [rslib/src/import_export/package/apkg/import/notes.rs:521](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L521).

### TC-ANKI-054 — colpkg thay collection nhưng giữ media ngoài gói

- **Truy vết:** US-ANKI-14; AC-ANKI-054; FR FR-DAT-PKG-001; BR BR-ANKI-022; ERR —.
- **Loại / entry surface:** happy / Package import/export + collection snapshot.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** profile tạm có note LOCAL-ONLY và media orphan-old.png; colpkg QA gồm note SNAPSHOT, scheduling và new.png; bật media khi export.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Import colpkg vào profile tạm.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** collection trở thành nội dung gói gồm SNAPSHOT và scheduling; LOCAL-ONLY không còn như merge apkg; orphan-old.png không bị xóa chỉ vì ngoài package.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/import_export/package/apkg/import/notes.rs:333](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L333); [rslib/src/import_export/package/apkg/import/cards.rs:99](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/cards.rs#L99); [rslib/src/import_export/package/colpkg/import.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/colpkg/import.rs#L31); [docs-site/manual/exporting.mdx:34](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/exporting.mdx#L34).

### TC-ANKI-055 — Export không scheduling

- **Truy vết:** US-ANKI-14; AC-ANKI-055; FR FR-DAT-PKG-001; BR BR-ANKI-022; ERR —.
- **Loại / entry surface:** boundary / Package import/export + collection snapshot.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** note có tags marked/leech/qa, card đã học; export apkg với scheduling tắt; profile nhận rỗng.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Import bản export vào profile nhận và so với bản gốc.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** bản chia sẻ không mang scheduling cũ và không mang marked/leech; dữ liệu gốc vẫn giữ lịch/tag; scope media theo tùy chọn export.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/import_export/package/apkg/import/notes.rs:333](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L333); [rslib/src/import_export/package/apkg/import/cards.rs:99](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/cards.rs#L99); [rslib/src/import_export/package/colpkg/import.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/colpkg/import.rs#L31); [docs-site/manual/exporting.mdx:34](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/exporting.mdx#L34); [docs-site/manual/exporting.mdx:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/exporting.mdx#L80).

### TC-ANKI-056 — Remote mới hơn thay toàn record

- **Truy vết:** US-ANKI-15; AC-ANKI-056; FR FR-DAT-SYNC-001; BR BR-ANKI-023; ERR —.
- **Loại / entry surface:** happy / Sync chunk harness hoặc self-host server test tương thích.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** hai collection fixture cùng note_id và GUID; local pending với fields [localA,oldB], mtime=t; remote [oldA,remoteB], mtime=t+1; endpoint thử nghiệm cô lập.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Áp chunk sync note/card theo protocol tương thích.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** record remote thắng theo mtime; không ghép thành [localA,remoteB]; revlog hợp lệ được nhập theo nhánh riêng.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Dừng endpoint test nếu TC đã khởi tạo; xóa media test sau khi thu hash.

**Nguồn oracle:** [rslib/src/sync/collection/chunks.rs:162](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/chunks.rs#L162); [rslib/src/sync/collection/meta.rs:65](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L65).

### TC-ANKI-057 — Remote không mới hơn local pending

- **Truy vết:** US-ANKI-15; AC-ANKI-057; FR FR-DAT-SYNC-001; BR BR-ANKI-023; ERR —.
- **Loại / entry surface:** negative / Sync chunk harness hoặc self-host server test tương thích.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** hai bản sao fixture: local pending mtime=t; remote mtime=t−1 hoặc t; nội dung khác.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Áp incoming chunk của từng fixture.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** remote không thay local tại bước áp chunk này; không suy ra toàn bộ sync luôn giữ cả hai chỉnh sửa.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Dừng endpoint test nếu TC đã khởi tạo; xóa media test sau khi thu hash.

**Nguồn oracle:** [rslib/src/sync/collection/chunks.rs:162](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/chunks.rs#L162); [rslib/src/sync/collection/meta.rs:65](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L65).

### TC-ANKI-058 — Local không pending

- **Truy vết:** US-ANKI-15; AC-ANKI-058; FR FR-DAT-SYNC-001; BR BR-ANKI-023; ERR —.
- **Loại / entry surface:** boundary / Sync chunk harness hoặc self-host server test tương thích.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** local record không pending sync, mtime=t; incoming remote hợp lệ mtime=t−1.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Áp incoming chunk.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** điều kiện không pending cho phép nhận remote dù timestamp không lớn hơn local; kiểm tra đúng branch thay record.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Dừng endpoint test nếu TC đã khởi tạo; xóa media test sau khi thu hash.

**Nguồn oracle:** [rslib/src/sync/collection/chunks.rs:162](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/chunks.rs#L162); [rslib/src/sync/collection/meta.rs:65](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L65).

### TC-ANKI-059 — Full sync theo chiều và media riêng

- **Truy vết:** US-ANKI-15; AC-ANKI-059; FR FR-DAT-SYNC-001; BR BR-ANKI-023, BR-ANKI-028; ERR —.
- **Loại / entry surface:** boundary / Sync chunk harness hoặc self-host server test tương thích.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** hai bản sao local/remote có schema khác; LOCAL-ONLY và REMOTE-ONLY phân biệt rõ; media có file riêng mỗi phía.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Thực hiện Upload trên fixture thứ nhất và Download trên fixture thứ hai bằng server test cô lập.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** Upload chọn collection local làm phía gửi; Download thay local bằng remote; không dùng lựa chọn collection một chiều để kết luận media đã xong hoặc bị thay một chiều.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Dừng endpoint test nếu TC đã khởi tạo; xóa media test sau khi thu hash.

**Nguồn oracle:** [rslib/src/sync/collection/chunks.rs:162](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/chunks.rs#L162); [rslib/src/sync/collection/meta.rs:65](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L65); [docs-site/manual/media.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/media.mdx#L24).

### TC-ANKI-060 — Restore snapshot

- **Truy vết:** US-ANKI-16; AC-ANKI-060; FR FR-DAT-BACK-001; BR BR-ANKI-024; ERR —.
- **Loại / entry surface:** happy / Backup/restore trên profile riêng + filesystem clock.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** profile tạm có snapshot gồm note S và card lịch D; sau snapshot thêm note L và sửa D; backup tự động không media.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Restore snapshot rồi kiểm tra collection và mở lại ứng dụng trong môi trường test.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** note S và lịch tại snapshot được phục hồi; thay đổi sau snapshot như L không còn; auto-sync/backup tạm dừng đến khi mở lại theo manual.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/collection/backup.rs:28](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/collection/backup.rs#L28); [docs-site/manual/backups.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L7); [docs-site/manual/backups.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L24).

### TC-ANKI-061 — Force không vượt guard không thay đổi

- **Truy vết:** US-ANKI-16; AC-ANKI-061; FR FR-DAT-BACK-001; BR BR-ANKI-024; ERR —.
- **Loại / entry surface:** negative / Backup/restore trên profile riêng + filesystem clock.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** collection chưa đổi từ lần backup gần nhất; ghi danh sách file backup; force=true.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Gọi maybe_backup và chờ kết quả nếu có handle.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** không tạo backup mới; trả None ở guard changed_since_last_backup trước kiểm tra interval.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/collection/backup.rs:28](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/collection/backup.rs#L28); [docs-site/manual/backups.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L7); [docs-site/manual/backups.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L24).

### TC-ANKI-062 — Ngay trước, tại và sau interval backup

- **Truy vết:** US-ANKI-16; AC-ANKI-062; FR FR-DAT-BACK-001; BR BR-ANKI-024; ERR —.
- **Loại / entry surface:** boundary / Backup/restore trên profile riêng + filesystem clock.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** ba fixture collection đã đổi; minimum_interval_mins=30; backup gần nhất tại t0; clock filesystem/SystemTime có thể kiểm soát t0+1799s,1800s,1801s; force=false.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Gọi maybe_backup mỗi mốc với thư mục backup riêng.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** 1799s bị skip do còn recent; tại 1800s và 1801s không còn recent nên có thể tạo backup; chờ writer hoàn tất và kiểm file thuộc fixture.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/collection/backup.rs:28](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/collection/backup.rs#L28); [docs-site/manual/backups.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L7); [docs-site/manual/backups.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L24); [rslib/src/collection/backup.rs:62](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/collection/backup.rs#L62).

### TC-ANKI-063 — Media phải backup bằng colpkg

- **Truy vết:** US-ANKI-16; AC-ANKI-063; FR FR-DAT-BACK-001; BR BR-ANKI-022, BR-ANKI-024; ERR —.
- **Loại / entry surface:** boundary / Backup/restore trên profile riêng + filesystem clock.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** profile fixture có note tham chiếu QA.png; tạo một backup tự động và một export colpkg Include Media; hai profile nhận rỗng.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Restore/import từng gói vào profile nhận tương ứng.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** backup tự động phục hồi text/scheduling nhưng không khôi phục QA.png ở profile rỗng; colpkg Include Media mang cả asset đã xuất.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/collection/backup.rs:28](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/collection/backup.rs#L28); [docs-site/manual/backups.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L7); [docs-site/manual/backups.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L24); [docs-site/manual/exporting.mdx:34](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/exporting.mdx#L34); [docs-site/manual/backups.mdx:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L59).

### TC-ANKI-064 — Today đếm lượt, không card duy nhất

- **Truy vết:** US-ANKI-17; AC-ANKI-064; FR FR-RPT-STAT-001; BR BR-ANKI-025; ERR —.
- **Loại / entry surface:** happy / Statistics aggregation từ revlog fixture.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** cùng card có hai log học hôm nay: Again rồi Good; không log khác; clock/day range cố định.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Tính Today statistics.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** hai lượt trả lời được đếm, một lượt đúng; không rút thành một card hay kết luận card đã nhớ hoàn toàn.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/stats/graphs/today.rs:17](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/today.rs#L17); [rslib/src/stats/graphs/retention.rs:53](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L53).

### TC-ANKI-065 — Loại log thao tác thủ công

- **Truy vết:** US-ANKI-17; AC-ANKI-065; FR FR-RPT-STAT-001; BR BR-ANKI-025; ERR —.
- **Loại / entry surface:** negative / Statistics aggregation từ revlog fixture.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** fixture cùng phạm vi có hai log Manual/Rescheduled và một log Review Hard hợp lệ.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Tính Today statistics.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** Manual/Rescheduled không được tính vào số lượt trả lời Today; Hard hợp lệ được tính đúng.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/stats/graphs/today.rs:17](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/today.rs#L17); [rslib/src/stats/graphs/retention.rs:53](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L53).

### TC-ANKI-066 — Mature theo interval trước

- **Truy vết:** US-ANKI-17; AC-ANKI-066; FR FR-RPT-STAT-001; BR BR-ANKI-025; ERR —.
- **Loại / entry surface:** boundary / Statistics aggregation từ revlog fixture.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** ba Review log hợp lệ có last_interval 20,21,22 ngày; cùng rating Good và cùng khoảng thời gian.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Tính thống kê mature.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** 20 là young; 21 và 22 là mature; không dùng interval mới thay last_interval.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [rslib/src/stats/graphs/today.rs:17](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/today.rs#L17); [rslib/src/stats/graphs/retention.rs:53](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L53).

### TC-ANKI-067 — True retention đếm cả hai lượt cùng card trong ngày

- **Truy vết:** US-ANKI-17; AC-ANKI-067; FR FR-RPT-STAT-001; BR BR-ANKI-025; ERR —.
- **Loại / entry surface:** boundary / GraphData/TrueRetention qua storage → aggregation → UI.
- **Preconditions:** collection disposable, không sync/add-on; harness cố định clock/offset/rollover trước khi tạo/mở collection và chèn raw revlog; xác nhận next_day_at thật, không ghi DB khi app đang giữ transaction; fixture này kiểm aggregation, không giả định hai log được sinh bằng chuỗi answer UI
- **Data / trạng thái đầu:** fixture F067-min có đúng một card cid=1001 và hai revlog: id=1793682000000/ease=1 rồi id=1793685600000/ease=3; cả hai type=Review(1), lastIvl=20, factor=2500, ivl=1, usn=-1, time=1000; không có log khác; clock=2026-11-03T12:00:00Z, offset UTC, rollover 04:00, next_day_at=1793764800; search="", days=0 và locale en-US.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.



**Steps**

1. Dựng F067-min; đọc lại đúng hai row cùng cid, rating 1 và 3, cùng lastIvl=20; xác nhận next_day_at=1793764800.
2. Gọi graph data search rỗng, days=0; đối chiếu bốn counter ở cả sáu cửa sổ như Expected.
3. Mở True retention Young/Mature/All; đối chiếu Count và tỷ lệ, dùng tổng pass chia tổng mẫu, không lấy trung bình tỷ lệ các nhóm.
4. Đổi search thành cid:1001, days=0; xác nhận hai log vẫn được lấy, Today Count=2 và 50.0%, Yesterday Count=0 và N/A.
5. Lưu response/UI và môi trường khi thực thi; trả clock/timezone rồi cleanup C0.

**Expected:** today/week/month/year/allTime đều có young_passed=1, young_failed=1, mature_passed=0, mature_failed=0; Count=2, Young và Total=50.0%, Mature=N/A; yesterday có bốn counter=0, Count=0 và các tỷ lệ N/A; search cid:1001 không đổi kết quả; không bỏ lượt Good thứ hai cùng ngày.

**Giới hạn oracle:** Oracle As-Is theo pipeline source đếm từng log đủ điều kiện, khác manual first review/card/day. Chỉ giải quyết kết quả hiện hành; quyết định sửa manual hay đổi sản phẩm còn mở. Fixture tối thiểu này không chứng minh mọi bộ lọc/biên; fixture mở rộng 22 row nằm trong báo cáo retention riêng, chưa thực thi.

**Cleanup:** C0; đóng và xóa riêng collection/card/revlog test sau khi lưu evidence; trả clock, UTC offset, rollover và locale.

**Nguồn oracle:** [rslib/src/storage/revlog/get.sql:1](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/get.sql#L1); [rslib/src/storage/revlog/mod.rs:122](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/mod.rs#L122); [rslib/src/storage/revlog/mod.rs:175](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/mod.rs#L175); [rslib/src/stats/graphs/mod.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/mod.rs#L31); [rslib/src/stats/graphs/retention.rs:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L16); [rslib/src/stats/graphs/retention.rs:53](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L53); [rslib/src/revlog/mod.rs:107](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/revlog/mod.rs#L107); [ts/routes/graphs/true-retention.ts:105](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/graphs/true-retention.ts#L105); [docs-site/manual/stats.mdx:229](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/stats.mdx#L229).

### TC-ANKI-068 — Hook Add và filter trả giá trị

- **Truy vết:** US-ANKI-18; AC-ANKI-068; FR FR-EXT-ADD-001; BR BR-ANKI-026; ERR —.
- **Loại / entry surface:** happy / Tools Add-ons + package/metadata QA + hook trace.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** profile thử nghiệm chỉ cài addon QA cục bộ không network: hook note_will_be_added ghi counter, filter card_will_show nối QA_SUFFIX vào text rồi trả text; collection rỗng.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Thêm note bằng Add screen rồi hiện câu hỏi card trong reviewer.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** hook Add được gọi; filter card_will_show nhận kind=reviewQuestion và trả text có QA_SUFFIX, reviewer nhận text đã đổi.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Gỡ callback A/B và QA addon khỏi thư mục profile thử.

**Nguồn oracle:** [docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16); [qt/tools/genhooks_gui.py:313](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/tools/genhooks_gui.py#L313); [qt/aqt/reviewer.py:391](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/reviewer.py#L391).

### TC-ANKI-069 — Hook Add không chặn import

- **Truy vết:** US-ANKI-18; AC-ANKI-069; FR FR-EXT-ADD-001; BR BR-ANKI-026; ERR —.
- **Loại / entry surface:** negative / Tools Add-ons + package/metadata QA + hook trace.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** cùng addon QA ghi counter note_will_be_added; trước import reset counter=0; file text hợp lệ.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Import file text.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** note_will_be_added không được gọi do import; counter vẫn 0; không xem hook này là policy cho mọi đường nhập.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Gỡ callback A/B và QA addon khỏi thư mục profile thử.

**Nguồn oracle:** [docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16).

### TC-ANKI-070 — Nhiều addon và profile

- **Truy vết:** US-ANKI-18; AC-ANKI-070; FR FR-EXT-ADD-001; BR BR-ANKI-026, BR-ANKI-027; ERR —.
- **Loại / entry surface:** boundary / Tools Add-ons + package/metadata QA + hook trace.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** hai callback QA đăng ký reviewer_did_show_question theo thứ tự A rồi B, mỗi callback ghi vào log fixture; hai profile tạm dùng chung thư mục addon.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Hiện câu hỏi ở profile thứ nhất rồi chuyển profile thứ hai có card fixture và hiện câu hỏi.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** callback được gọi tuần tự theo contract hooks; addon cùng được dùng giữa profile; không suy ra collection của hai profile là chung.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Gỡ callback A/B và QA addon khỏi thư mục profile thử.

**Nguồn oracle:** [docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16); [docs-site/manual/profiles.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/profiles.mdx#L5); [docs-site/addons/hooks-and-filters.mdx:49](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L49).

### TC-ANKI-071 — Hai collection riêng

- **Truy vết:** US-ANKI-19; AC-ANKI-071; FR FR-SYS-PROF-001; BR BR-ANKI-027; ERR —.
- **Loại / entry surface:** happy / Switch Profile với auto-sync tắt.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** profile QA-A có note ALPHA; QA-B mới rỗng; auto-sync tắt ở cả hai.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Chuyển QA-A sang QA-B rồi trở lại QA-A.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** QA-B không có ALPHA; QA-A vẫn có ALPHA trong collection riêng; thiết lập thuộc profile được đọc theo profile hiện hành.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [docs-site/manual/profiles.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/profiles.mdx#L5).

### TC-ANKI-072 — Hai profile cùng account và lựa chọn full sync

- **Truy vết:** US-ANKI-19; AC-ANKI-072; FR FR-SYS-PROF-001; BR BR-ANKI-027; ERR —.
- **Loại / entry surface:** negative / Switch Profile + auth theo profile + UI full collection sync với SimpleServer cô lập.
- **Preconditions:** server test cùng commit, user test riêng, endpoint loopback explicit; không dùng TEST_ENDPOINT ambient hoặc account production; mọi collection integrity hợp lệ, request thành công; tắt media sync; đo scm/mod và nonempty trước mỗi nhánh, không suy từ tên profile hoặc thời gian tạo; snapshot sau chuẩn bị A upload; client và server test dùng cùng clock t0, xác nhận timestamp đồng bộ trước request để không rẽ nhánh clock-off
- **Data / trạng thái đầu:** F072 có hai profile tạm A/B, collection path riêng; cùng auth của một user SimpleServer đúng commit, auto-sync/media/add-on tắt; A có một note/card ONLY_A, B có một note/card ONLY_B với ID/GUID khác; server đã nhận full upload A; B và server đều có card, B.scm khác S.scm và B.mod khác S.mod; snapshot từng nhánh độc lập.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.



**Steps**

1. Dựng F072 và auth cùng user cho A/B; xác nhận paths khác nhau. Nếu dùng login qua nút Sync, callback sẽ tiếp tục sync, phải quan sát prompt thay vì coi login chỉ lưu cấu hình.
2. Đọc metadata B/server: cả hai nonempty, scm khác và mod khác; lưu tập note/card IDs, fields, scheduling và revlog của A/B/server.
3. Nhánh Cancel: B bấm Sync, kiểm full-choice prompt, chọn Cancel; không có full transfer, nội dung A/B/server giữ như trước.
4. Restore F072 và server; nhánh Download: B chọn Download, quan sát yêu cầu backup, chờ download/reopen xong; B có dữ liệu server A, không merge phần chỉ có ở B; không khẳng định backup đã bị xóa.
5. Restore F072 và server; nhánh Upload: B chọn Upload, chờ xong; server có ONLY_B và không có ONLY_A, B giữ B, A local vẫn A vì chưa sync A.
6. Ghi actual riêng từng nhánh, auth/path và prompt; cleanup C0 cùng server/process/account test do TC tạo.

**Expected:** không có chặn trùng account trong caller đã khảo sát; Cancel không gọi full upload/download và giữ ONLY_B ở B, ONLY_A ở server/A; Download thay active B bằng snapshot A từ server, ONLY_B không còn ở active B; Upload thay active server bằng B nhưng A local vẫn giữ ONLY_A vì chưa sync tiếp; collection paths vẫn riêng và không có namespace server riêng theo tên profile.

**Giới hạn oracle:** Oracle cho SimpleServer và caller desktop tại commit. Khi mod bằng nhau có thể NoChanges trước khi xét schema; khi schema chung có thể normal merge. B rỗng/server nonempty chỉ cho Download. Không suy thành mọi lần trùng account đều full-sync, mất dữ liệu ngay hoặc server hosted có cùng implementation. Cancel chỉ cam kết nội dung collection, không cam kết byte-identical metadata/profile.

**Cleanup:** C0; dừng server test do TC khởi tạo; xóa riêng profiles A/B, server user/data và backups test sau khi lưu evidence redacted; không đụng tài khoản thật.

**Nguồn oracle:** [qt/aqt/profiles.py:212](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L212); [qt/aqt/profiles.py:659](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L659); [qt/aqt/profiles.py:681](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L681); [qt/aqt/sync.py:307](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L307); [rslib/src/sync/http_server/mod.rs:122](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/http_server/mod.rs#L122); [rslib/src/sync/collection/meta.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L59); [qt/aqt/sync.py:138](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L138); [rslib/src/sync/collection/download.rs:35](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/download.rs#L35); [rslib/src/sync/collection/upload.rs:79](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/upload.rs#L79); [rslib/src/sync/collection/tests.rs:591](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/tests.rs#L591); [docs-site/manual/profiles.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/profiles.mdx#L5).

### TC-ANKI-073 — Addon dùng chung giữa profile

- **Truy vết:** US-ANKI-19; AC-ANKI-073; FR FR-SYS-PROF-001; BR BR-ANKI-027; ERR —.
- **Loại / entry surface:** boundary / Switch Profile với auto-sync tắt.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** profile QA-A/QA-B collection riêng; addon QA cục bộ được cài một lần, không lưu thông tin cá nhân.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Mở lần lượt hai profile và quan sát danh sách/lifecycle addon.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** cùng addon dùng được ở cả hai profile; sự riêng biệt collection không tạo sandbox addon theo từng profile.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [docs-site/manual/profiles.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/profiles.mdx#L5).

### TC-ANKI-074 — Check Media phân biệt thiếu và không dùng

- **Truy vết:** US-ANKI-20; AC-ANKI-074; FR FR-DAT-MEDI-001; BR BR-ANKI-028; ERR —.
- **Loại / entry surface:** happy / Check Media + thư mục media tạm.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** note tham chiếu exists.png và missing.png; thư mục chỉ có exists.png và orphan.png; không file/template khác.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Chạy Check Media trên profile tạm.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** missing.png thuộc tham chiếu thiếu; orphan.png thuộc file không dùng; exists.png không thuộc hai nhóm đó.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Dừng endpoint test nếu TC đã khởi tạo; xóa media test sau khi thu hash.

**Nguồn oracle:** [docs-site/manual/media.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/media.mdx#L24); [docs-site/manual/syncing.mdx:54](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/syncing.mdx#L54).

### TC-ANKI-075 — Template media không được quét như field

- **Truy vết:** US-ANKI-20; AC-ANKI-075; FR FR-DAT-MEDI-001; BR BR-ANKI-028; ERR —.
- **Loại / entry surface:** negative / Check Media + thư mục media tạm.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** template tham chiếu logo.png; không note field nào tham chiếu; logo.png có trong media và không có tiền tố _.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Chạy Check Media, chỉ xem kết quả không xác nhận xóa.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** không coi tham chiếu template là bằng chứng file đang dùng trong phép quét; logo.png được báo unused trong fixture này.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Dừng endpoint test nếu TC đã khởi tạo; xóa media test sau khi thu hash.

**Nguồn oracle:** [docs-site/manual/media.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/media.mdx#L24); [docs-site/manual/syncing.mdx:54](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/syncing.mdx#L54).

### TC-ANKI-076 — Tiền tố underscore cho static media

- **Truy vết:** US-ANKI-20; AC-ANKI-076; FR FR-DAT-MEDI-001; BR BR-ANKI-028; ERR —.
- **Loại / entry surface:** boundary / Check Media + thư mục media tạm.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** template tham chiếu _logo.png có trong media; không field nào tham chiếu; một file logo.png thường cũng tồn tại không dùng.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Chạy Check Media.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** _logo.png được bảo vệ bởi quy ước static media; logo.png thường được xét unused; không tự xóa file trong test.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Dừng endpoint test nếu TC đã khởi tạo; xóa media test sau khi thu hash.

**Nguồn oracle:** [docs-site/manual/media.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/media.mdx#L24); [docs-site/manual/syncing.mdx:54](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/syncing.mdx#L54).

### TC-ANKI-077 — Media cùng tên khác hash với thứ tự sync xác định

- **Truy vết:** US-ANKI-20; AC-ANKI-077; FR FR-DAT-MEDI-001; BR BR-ANKI-028; ERR —.
- **Loại / entry surface:** boundary / MediaSyncer/backend RPC + status completion + media filesystem/DB và SimpleServer test.
- **Preconditions:** endpoint/user cô lập đúng commit; chỉ media sync, không Check Media hoặc collection sync; filename ASCII/NFC shared.png hợp lệ; payloads khác hash; mỗi nhánh restore dữ liệu/cursor và đảm bảo ChangeTracker thấy thay đổi. RPC start không được coi là sync hoàn tất
- **Data / trạng thái đầu:** F077 có C1/C2 và SimpleServer S cùng user test, media DB/folder riêng, cursors=0 và S trống USN0; C1 thêm shared.png=A và C2 thêm shared.png=B qua add_file ở folder trống, hai entry dirty=true; A/B là PNG 1×1/69byte có bytes PNG trong mục dữ liệu TC-ANKI-077, SHA1 A=2732f12a8f18d27cf0fa78ef41091bfa1ccec9ce, B=3b37538efb87e9eb1c6d547562f499932b894f17; không sửa đồng thời.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**PNG fixture (Base64, giải mã thành đúng 69 byte):**

A: `iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC`

B: `iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGNgYPgPAAEDAQAIicLsAAAAAElFTkSuQmCC`

**Steps**

1. Giải mã hai PNG ở fixture_details hoặc dùng evidence/fixtures/media-a.png và media-b.png; kiểm byte length và SHA1, tạo hai folders trống rồi add_file với cùng tên shared.png. Xác nhận dirty/cursors/server USN đúng F077.
2. Sync C1 và poll status tới inactive, không lỗi. Xác nhận S shared.png hash A, USN1, C1 clean/cursor1.
3. Sync C2 tới completion: quan sát fetch shared.png/USN1/hash A trước upload; kiểm C2 bytes A, dirty=false/cursor1, không còn pending B và S.USN không tăng do B. Sync C1 lại, xác nhận tất cả hash A/count1 và không có file suffix/trash B.
4. Restore F077; chạy C2→C1→C2; xác nhận tất cả hash B/count1, server USN1.
5. Restore trạng thái ba bên A/USN1; đổi file C2 thành B, đảm bảo folder/file mtime được nhận diện và xác nhận dirty B bằng tracker/harness trước network (không sleep rồi đoán). S vẫn USN1. Sync C2 rồi C1: S lên USN2, các bên B/clean.
6. Lưu before/after hashes, cursor/dirty/USN và thứ tự request cho từng nhánh; cleanup C0.

**Expected:** thứ tự C1→C2: C2 fetch server USN1 và download A dù B local dirty, ghi đè shared.png, DB clean và không upload B; C1/C2/S đều hash A, server vẫn USN1 và có một filename; không tạo hash-suffix hay bản B trong media.trash. Đảo thứ tự cho hash B. Nhánh sửa sau đồng nhất: C2 dirty B với cursor1=S.USN1 sẽ upload B lên S.USN2, rồi C1 fetch B; các bên hash B. Không dùng file mtime để chọn winner.

**Giới hạn oracle:** Server-favors yêu cầu remote change chưa được client nhận; local dirty một mình không bảo vệ file trước nhánh download. Hai upload in-flight chưa có thứ tự thì không có winner duy nhất; server self-host nhận upload khác hash sau có thể thay nội dung. Local add_file vào folder đã có tên dùng hash-suffix là luồng khác. Không khẳng định rollback filesystem khi I/O/network lỗi hoặc hosted AnkiWeb đã được kiểm thử.

**Cleanup:** C0; đóng clients, dừng server test và xóa riêng media folders/DB/trash/payloads test sau khi lưu hashes và evidence; giữ source/collection người dùng nguyên vẹn.

**Nguồn oracle:** [rslib/src/sync/media/syncer.rs:60](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/syncer.rs#L60); [rslib/src/sync/media/changes.rs:44](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/changes.rs#L44); [rslib/src/media/files.rs:403](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L403); [rslib/src/sync/media/database/client/mod.rs:206](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/client/mod.rs#L206); [rslib/src/sync/media/database/server/entry/upload.rs:35](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/server/entry/upload.rs#L35); [rslib/src/sync/media/tests.rs:278](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/tests.rs#L278); [rslib/src/backend/sync.rs:188](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/backend/sync.rs#L188); [rslib/src/sync/media/database/client/changetracker.rs:56](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/client/changetracker.rs#L56); [rslib/src/media/files.rs:165](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L165).

### TC-ANKI-078 — Thêm/gỡ tag ở cấp note

- **Truy vết:** US-ANKI-06; AC-ANKI-078; FR FR-ORG-SRCH-001; BR BR-ANKI-007; ERR —.
- **Loại / entry surface:** happy / Browse Cards/search/tags/flags.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** note N có siblings A/B, note M có card C; cả hai chưa có tag qa; chỉ chọn A trong Browse Cards.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Add Tags qa rồi kiểm tra, sau đó Remove Tags qa trên cùng lựa chọn.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** tag qa được thêm rồi gỡ trên note N nên cả A/B phản ánh thay đổi; note M/card C không nhận hoặc mất tag do thao tác này.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226).

### TC-ANKI-079 — Một flag trên một card

- **Truy vết:** US-ANKI-06; AC-ANKI-079; FR FR-ORG-SRCH-001; BR BR-ANKI-007; ERR —.
- **Loại / entry surface:** boundary / Browse Cards/search/tags/flags.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** siblings A/B cùng note; A chưa flag, B flag=3; chỉ chọn A; note tags đã chụp.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Đặt flag 1 cho A, thay bằng flag 2, rồi chọn flag 2 lần nữa để gỡ.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** A lần lượt flag 1, flag 2, không flag; không đồng thời giữ hai flag; B vẫn flag 3 và note tags không đổi.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226).

### TC-ANKI-080 — Đổi tên tag đang dùng

- **Truy vết:** US-ANKI-06; AC-ANKI-080; FR FR-ORG-SRCH-001; BR BR-ANKI-007; ERR —.
- **Loại / entry surface:** boundary / Browse Cards/search/tags/flags.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** note N có tag qa_old, note M có tag unrelated; không tag qa_new tồn tại.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Đổi tên qa_old thành qa_new trong Browser rồi tìm tag:qa_new.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** N có qa_new và truy vấn trả siblings của N; qa_old không còn là tag của N; M giữ unrelated.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau.

**Nguồn oracle:** [docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226).

### TC-ANKI-081 — Cài addon local hợp lệ

- **Truy vết:** US-ANKI-18; AC-ANKI-081; FR FR-EXT-ADD-001; BR BR-ANKI-026; ERR —.
- **Loại / entry surface:** happy / Tools Add-ons + package/metadata QA + hook trace.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** profile thử nghiệm chỉ có thư mục addon QA; package ZIP tự tạo chứa `__init__.py` không side effect và manifest hợp schema với package=qa_fixture, name=QA Fixture; chưa có package đó.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Install from file với force_enable=True rồi đọc metadata/files và danh sách addon.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** cài file vào addon folder qa_fixture, metadata name tương ứng và disabled=False; danh sách được redraw; chưa coi code addon đã nạp cho đến lifecycle restart.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Gỡ callback A/B và QA addon khỏi thư mục profile thử.

**Nguồn oracle:** [docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16); [qt/aqt/addons.py:1025](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1025).

### TC-ANKI-082 — Hủy hoặc sai mã Get Add-ons

- **Truy vết:** US-ANKI-18; AC-ANKI-082; FR FR-EXT-ADD-001; BR BR-ANKI-026; ERR —.
- **Loại / entry surface:** negative / Tools Add-ons + package/metadata QA + hook trace.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** hai fixture dialog riêng: A nhập not-a-number, B đóng Cancel; instrumentation chỉ đếm download dispatch, không gọi AnkiWeb thật.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Bấm OK ở A và Cancel ở B.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** A hiển thị cảnh báo invalid code và không accept; B không có IDs; cả hai không phát lệnh tải addon; không gán ERR/HTTP chưa có trong SRS.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Gỡ callback A/B và QA addon khỏi thư mục profile thử.

**Nguồn oracle:** [docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16); [qt/aqt/addons.py:1091](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1091).

### TC-ANKI-083 — Get IDs và kiểm tra cập nhật

- **Truy vết:** US-ANKI-18; AC-ANKI-083; FR FR-EXT-ADD-001; BR BR-ANKI-026; ERR —.
- **Loại / entry surface:** boundary / Tools Add-ons + package/metadata QA + hook trace.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** dialog Get Add-ons có chuỗi 123 456 hoặc URL https://ankiweb.net/shared/info/123; dùng hai fixture độc lập; dispatcher được quan sát trước network; mọi addon giả lập ở thư mục test.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Accept Get Add-ons rồi riêng biệt nhấn Check for Updates.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** IDs được parse thành integer theo input và chuyển tới download_addons với force_enable=True; Check for Updates gọi check_and_prompt_for_updates và callback after_downloading; chưa khẳng định ID ví dụ tồn tại hoặc tải/cập nhật thành công trên AnkiWeb.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Gỡ callback A/B và QA addon khỏi thư mục profile thử.

**Nguồn oracle:** [docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16); [qt/aqt/addons.py:1091](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1091).

### TC-ANKI-084 — Delete hủy hoặc không chọn addon

- **Truy vết:** US-ANKI-18; AC-ANKI-084; FR FR-EXT-ADD-001; BR BR-ANKI-026; ERR —.
- **Loại / entry surface:** negative / Tools Add-ons + package/metadata QA + hook trace.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** hai fixture có addon QA đã cài: A không chọn hàng; B chọn addon QA nhưng chọn No ở xác nhận; ghi hash thư mục và metadata trước.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Nhấn Delete theo từng fixture.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** A không xóa và không hỏi xác nhận; B dừng sau No; cả hai giữ thư mục/metadata addon QA, không phát lifecycle will_delete.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Gỡ callback A/B và QA addon khỏi thư mục profile thử.

**Nguồn oracle:** [docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16).

### TC-ANKI-085 — Delete addon bật sau xác nhận

- **Truy vết:** US-ANKI-18; AC-ANKI-085; FR FR-EXT-ADD-001; BR BR-ANKI-026; ERR —.
- **Loại / entry surface:** happy / Tools Add-ons + package/metadata QA + hook trace.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** addon qa_fixture đang enabled trong profile test; chọn riêng addon đó; trash chỉ chứa dữ liệu test; không có addon thật.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Nhấn Delete và xác nhận Yes.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** gọi lifecycle will_delete, chuyển thư mục addon vào trash, redraw danh sách và đánh dấu require_restart=True; không tuyên bố addon đang nạp đã ngừng tức thời.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Gỡ callback A/B và QA addon khỏi thư mục profile thử.

**Nguồn oracle:** [docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16); [qt/aqt/addons.py:526](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L526).

### TC-ANKI-086 — Toggle và xung đột khi bật

- **Truy vết:** US-ANKI-18; AC-ANKI-086; FR FR-EXT-ADD-001; BR BR-ANKI-026; ERR —.
- **Loại / entry surface:** boundary / Tools Add-ons + package/metadata QA + hook trace.
- **Preconditions:** môi trường và fixture cô lập ở mục 1; đủ năng lực đọc snapshot backend; không có thao tác song song ngoài sự kiện nêu trong Data.
- **Data / trạng thái đầu:** hai fixture addon QA-A/QA-B có metadata conflicts hợp lệ; QA-B đang bật, QA-A đang tắt; chọn QA-A; bản sao thứ hai chọn addon đang bật để tắt.
- **Design:** Specified. **Status:** Not Run. **Actual result:** Not Run. Evidence/run date/tester: chưa có.

**Steps**

1. Tạo snapshot fixture đúng Data, ghi cấu hình/clock, số note/card/log và trạng thái có liên quan; nếu nhiều tổ hợp, tạo snapshot mới cho từng tổ hợp.
2. Toggle Enabled rồi đọc metadata và yêu cầu restart.
3. Chờ thao tác/transaction hoàn tất; đọc phản hồi và snapshot sau, so từng kết quả Expected; với case lỗi kiểm trạng thái không đổi được nêu.
4. Lưu actual/evidence riêng từng tổ hợp khi thực thi, rồi thực hiện cleanup; hiện chưa có kết quả chạy.

**Expected:** nhánh bật ghi enabled=True cho QA-A và vô hiệu addon xung đột tìm được; nhánh tắt ghi enabled=False cho addon chọn; UI đánh require_restart=True và redraw; không giả định reload code tức thời.

**Cleanup:** C0; hủy snapshot/collection và mọi file tổng hợp của riêng TC; không giữ thay đổi cho TC sau. Gỡ callback A/B và QA addon khỏi thư mục profile thử.

**Nguồn oracle:** [docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16).

## 3. RTM chuẩn

Bảng này là RTM canonical. [CSV](traceability.csv) là bản xuất cùng dữ liệu, không là baseline riêng. [Catalog JSON](qa-catalog.json) phục vụ kiểm tra ID/mapping; thay đổi phải đồng bộ ba hình thức. Design Blocked có hàng truy vết nhưng **không được tính là test có oracle hợp lệ**.

| FR ID | Story ID | AC ID | Test Case ID | BR ID | ERR ID | Loại | Design | Trạng thái chạy |
|---|---|---|---|---|---|---|---|---|
| FR-CNT-NOTE-001 | US-ANKI-01 | AC-ANKI-001 | TC-ANKI-001 | BR-ANKI-001, BR-ANKI-003 | — | happy | Specified | Not Run |
| FR-CNT-NOTE-001 | US-ANKI-01 | AC-ANKI-002 | TC-ANKI-002 | BR-ANKI-001 | ERR-ANKI-000-01 | negative | Specified | Not Run |
| FR-CNT-NOTE-001 | US-ANKI-01 | AC-ANKI-003 | TC-ANKI-003 | BR-ANKI-003 | — | boundary | Specified | Not Run |
| FR-CNT-NOTE-001 | US-ANKI-01 | AC-ANKI-004 | TC-ANKI-004 | BR-ANKI-003 | — | boundary | Specified | Not Run |
| FR-CNT-TYPE-001 | US-ANKI-02 | AC-ANKI-005 | TC-ANKI-005 | BR-ANKI-002, BR-ANKI-003 | — | happy | Specified | Not Run |
| FR-CNT-TYPE-001 | US-ANKI-02 | AC-ANKI-006 | TC-ANKI-006 | BR-ANKI-002 | ERR-ANKI-000-02 | negative | Specified | Not Run |
| FR-CNT-TYPE-001 | US-ANKI-02 | AC-ANKI-007 | TC-ANKI-007 | BR-ANKI-003 | — | boundary | Specified | Not Run |
| FR-CNT-CLOZ-001 | US-ANKI-03 | AC-ANKI-008 | TC-ANKI-008 | BR-ANKI-001, BR-ANKI-004 | — | happy | Specified | Not Run |
| FR-CNT-CLOZ-001 | US-ANKI-03 | AC-ANKI-009 | TC-ANKI-009 | BR-ANKI-001 | ERR-ANKI-000-01 | negative | Specified | Not Run |
| FR-CNT-CLOZ-001 | US-ANKI-03 | AC-ANKI-010 | TC-ANKI-010 | BR-ANKI-004 | — | boundary | Specified | Not Run |
| FR-CNT-IMGO-001 | US-ANKI-04 | AC-ANKI-011 | TC-ANKI-011 | BR-ANKI-005 | — | happy | Specified | Not Run |
| FR-CNT-IMGO-001 | US-ANKI-04 | AC-ANKI-012 | TC-ANKI-012 | BR-ANKI-003, BR-ANKI-005 | — | negative | Specified | Not Run |
| FR-CNT-IMGO-001 | US-ANKI-04 | AC-ANKI-013 | TC-ANKI-013 | BR-ANKI-005 | — | boundary | Specified | Not Run |
| FR-ORG-DECK-001 | US-ANKI-05 | AC-ANKI-014 | TC-ANKI-014 | BR-ANKI-006, BR-ANKI-012 | — | happy | Specified | Not Run |
| FR-ORG-DECK-001 | US-ANKI-05 | AC-ANKI-015 | TC-ANKI-015 | BR-ANKI-006 | — | negative | Specified | Not Run |
| FR-ORG-DECK-001 | US-ANKI-05 | AC-ANKI-016 | TC-ANKI-016 | BR-ANKI-006 | — | boundary | Specified | Not Run |
| FR-ORG-SRCH-001 | US-ANKI-06 | AC-ANKI-017 | TC-ANKI-017 | BR-ANKI-007 | — | happy | Specified | Not Run |
| FR-ORG-SRCH-001 | US-ANKI-06 | AC-ANKI-018 | TC-ANKI-018 | BR-ANKI-007 | — | negative | Specified | Not Run |
| FR-ORG-SRCH-001 | US-ANKI-06 | AC-ANKI-019 | TC-ANKI-019 | BR-ANKI-007 | — | boundary | Specified | Not Run |
| FR-LRN-REV-001 | US-ANKI-07 | AC-ANKI-020 | TC-ANKI-020 | BR-ANKI-006, BR-ANKI-008, BR-ANKI-011 | — | happy | Specified | Not Run |
| FR-LRN-REV-001 | US-ANKI-07 | AC-ANKI-021 | TC-ANKI-021 | BR-ANKI-011 | ERR-ANKI-000-03 | negative | Specified | Not Run |
| FR-LRN-REV-001 | US-ANKI-07 | AC-ANKI-022 | TC-ANKI-022 | BR-ANKI-008 | — | boundary | Specified | Not Run |
| FR-LRN-REV-001 | US-ANKI-07 | AC-ANKI-023 | TC-ANKI-023 | BR-ANKI-011 | — | boundary | Specified | Not Run |
| FR-LRN-SCH-001 | US-ANKI-08 | AC-ANKI-024 | TC-ANKI-024 | BR-ANKI-009, BR-ANKI-013 | — | happy | Specified | Not Run |
| FR-LRN-SCH-001 | US-ANKI-08 | AC-ANKI-025 | TC-ANKI-025 | BR-ANKI-010 | — | negative | Specified | Not Run |
| FR-LRN-SCH-001 | US-ANKI-08 | AC-ANKI-026 | TC-ANKI-026 | BR-ANKI-009 | — | boundary | Specified | Not Run |
| FR-LRN-SCH-001 | US-ANKI-08 | AC-ANKI-027 | TC-ANKI-027 | BR-ANKI-010, BR-ANKI-011 | ERR-ANKI-000-03 | negative | Specified | Not Run |
| FR-LRN-LIM-001 | US-ANKI-09 | AC-ANKI-028 | TC-ANKI-028 | BR-ANKI-012 | — | happy | Specified | Not Run |
| FR-LRN-LIM-001 | US-ANKI-09 | AC-ANKI-029 | TC-ANKI-029 | BR-ANKI-012 | — | negative | Specified | Not Run |
| FR-LRN-LIM-001 | US-ANKI-09 | AC-ANKI-030 | TC-ANKI-030 | BR-ANKI-012 | — | boundary | Specified | Not Run |
| FR-LRN-LIM-001 | US-ANKI-09 | AC-ANKI-031 | TC-ANKI-031 | BR-ANKI-006, BR-ANKI-012 | — | boundary | Specified | Not Run |
| FR-LRN-FSRS-001 | US-ANKI-10 | AC-ANKI-032 | TC-ANKI-032 | BR-ANKI-013, BR-ANKI-014 | — | happy | Specified | Not Run |
| FR-LRN-FSRS-001 | US-ANKI-10 | AC-ANKI-033 | TC-ANKI-033 | BR-ANKI-014 | — | negative | Specified | Not Run |
| FR-LRN-FSRS-001 | US-ANKI-10 | AC-ANKI-034 | TC-ANKI-034 | BR-ANKI-014 | — | boundary | Specified | Not Run |
| FR-LRN-FSRS-001 | US-ANKI-10 | AC-ANKI-035 | TC-ANKI-035 | BR-ANKI-014 | — | boundary | Specified | Not Run |
| FR-LRN-HIDE-001 | US-ANKI-11 | AC-ANKI-036 | TC-ANKI-036 | BR-ANKI-015 | — | happy | Specified | Not Run |
| FR-LRN-HIDE-001 | US-ANKI-11 | AC-ANKI-037 | TC-ANKI-037 | BR-ANKI-015 | — | negative | Specified | Not Run |
| FR-LRN-HIDE-001 | US-ANKI-11 | AC-ANKI-038 | TC-ANKI-038 | BR-ANKI-015 | — | boundary | Specified | Not Run |
| FR-LRN-HIDE-001 | US-ANKI-11 | AC-ANKI-039 | TC-ANKI-039 | BR-ANKI-016 | — | boundary | Specified | Not Run |
| FR-LRN-HIDE-001 | US-ANKI-11 | AC-ANKI-040 | TC-ANKI-040 | BR-ANKI-016 | — | boundary | Specified | Not Run |
| FR-LRN-FILT-001 | US-ANKI-12 | AC-ANKI-041 | TC-ANKI-041 | BR-ANKI-017 | — | happy | Specified | Not Run |
| FR-LRN-FILT-001 | US-ANKI-12 | AC-ANKI-042 | TC-ANKI-042 | BR-ANKI-017 | ERR-ANKI-000-04 | negative | Specified | Not Run |
| FR-LRN-FILT-001 | US-ANKI-12 | AC-ANKI-043 | TC-ANKI-043 | BR-ANKI-017 | — | boundary | Specified | Not Run |
| FR-LRN-FILT-001 | US-ANKI-12 | AC-ANKI-044 | TC-ANKI-044 | BR-ANKI-018 | — | happy | Specified | Not Run |
| FR-LRN-FILT-001 | US-ANKI-12 | AC-ANKI-045 | TC-ANKI-045 | BR-ANKI-019 | — | boundary | Specified | Not Run |
| FR-DAT-TEXT-001 | US-ANKI-13 | AC-ANKI-046 | TC-ANKI-046 | BR-ANKI-001, BR-ANKI-020 | — | happy | Specified | Not Run |
| FR-DAT-TEXT-001 | US-ANKI-13 | AC-ANKI-047 | TC-ANKI-047 | BR-ANKI-020 | ERR-ANKI-000-05 | negative | Specified | Not Run |
| FR-DAT-TEXT-001 | US-ANKI-13 | AC-ANKI-048 | TC-ANKI-048 | BR-ANKI-020 | ERR-ANKI-000-06 | negative | Specified | Not Run |
| FR-DAT-TEXT-001 | US-ANKI-13 | AC-ANKI-049 | TC-ANKI-049 | BR-ANKI-020 | ERR-ANKI-000-07 | negative | Specified | Not Run |
| FR-DAT-TEXT-001 | US-ANKI-13 | AC-ANKI-050 | TC-ANKI-050 | BR-ANKI-020 | — | boundary | Specified | Not Run |
| FR-DAT-PKG-001 | US-ANKI-14 | AC-ANKI-051 | TC-ANKI-051 | BR-ANKI-021 | — | happy | Specified | Not Run |
| FR-DAT-PKG-001 | US-ANKI-14 | AC-ANKI-052 | TC-ANKI-052 | BR-ANKI-021 | ERR-ANKI-000-08 | negative | Specified | Not Run |
| FR-DAT-PKG-001 | US-ANKI-14 | AC-ANKI-053 | TC-ANKI-053 | BR-ANKI-021 | — | boundary | Specified | Not Run |
| FR-DAT-PKG-001 | US-ANKI-14 | AC-ANKI-054 | TC-ANKI-054 | BR-ANKI-022 | — | happy | Specified | Not Run |
| FR-DAT-PKG-001 | US-ANKI-14 | AC-ANKI-055 | TC-ANKI-055 | BR-ANKI-022 | — | boundary | Specified | Not Run |
| FR-DAT-SYNC-001 | US-ANKI-15 | AC-ANKI-056 | TC-ANKI-056 | BR-ANKI-023 | — | happy | Specified | Not Run |
| FR-DAT-SYNC-001 | US-ANKI-15 | AC-ANKI-057 | TC-ANKI-057 | BR-ANKI-023 | — | negative | Specified | Not Run |
| FR-DAT-SYNC-001 | US-ANKI-15 | AC-ANKI-058 | TC-ANKI-058 | BR-ANKI-023 | — | boundary | Specified | Not Run |
| FR-DAT-SYNC-001 | US-ANKI-15 | AC-ANKI-059 | TC-ANKI-059 | BR-ANKI-023, BR-ANKI-028 | — | boundary | Specified | Not Run |
| FR-DAT-BACK-001 | US-ANKI-16 | AC-ANKI-060 | TC-ANKI-060 | BR-ANKI-024 | — | happy | Specified | Not Run |
| FR-DAT-BACK-001 | US-ANKI-16 | AC-ANKI-061 | TC-ANKI-061 | BR-ANKI-024 | — | negative | Specified | Not Run |
| FR-DAT-BACK-001 | US-ANKI-16 | AC-ANKI-062 | TC-ANKI-062 | BR-ANKI-024 | — | boundary | Specified | Not Run |
| FR-DAT-BACK-001 | US-ANKI-16 | AC-ANKI-063 | TC-ANKI-063 | BR-ANKI-022, BR-ANKI-024 | — | boundary | Specified | Not Run |
| FR-RPT-STAT-001 | US-ANKI-17 | AC-ANKI-064 | TC-ANKI-064 | BR-ANKI-025 | — | happy | Specified | Not Run |
| FR-RPT-STAT-001 | US-ANKI-17 | AC-ANKI-065 | TC-ANKI-065 | BR-ANKI-025 | — | negative | Specified | Not Run |
| FR-RPT-STAT-001 | US-ANKI-17 | AC-ANKI-066 | TC-ANKI-066 | BR-ANKI-025 | — | boundary | Specified | Not Run |
| FR-RPT-STAT-001 | US-ANKI-17 | AC-ANKI-067 | TC-ANKI-067 | BR-ANKI-025 | — | boundary | Specified | Not Run |
| FR-EXT-ADD-001 | US-ANKI-18 | AC-ANKI-068 | TC-ANKI-068 | BR-ANKI-026 | — | happy | Specified | Not Run |
| FR-EXT-ADD-001 | US-ANKI-18 | AC-ANKI-069 | TC-ANKI-069 | BR-ANKI-026 | — | negative | Specified | Not Run |
| FR-EXT-ADD-001 | US-ANKI-18 | AC-ANKI-070 | TC-ANKI-070 | BR-ANKI-026, BR-ANKI-027 | — | boundary | Specified | Not Run |
| FR-SYS-PROF-001 | US-ANKI-19 | AC-ANKI-071 | TC-ANKI-071 | BR-ANKI-027 | — | happy | Specified | Not Run |
| FR-SYS-PROF-001 | US-ANKI-19 | AC-ANKI-072 | TC-ANKI-072 | BR-ANKI-027 | — | negative | Specified | Not Run |
| FR-SYS-PROF-001 | US-ANKI-19 | AC-ANKI-073 | TC-ANKI-073 | BR-ANKI-027 | — | boundary | Specified | Not Run |
| FR-DAT-MEDI-001 | US-ANKI-20 | AC-ANKI-074 | TC-ANKI-074 | BR-ANKI-028 | — | happy | Specified | Not Run |
| FR-DAT-MEDI-001 | US-ANKI-20 | AC-ANKI-075 | TC-ANKI-075 | BR-ANKI-028 | — | negative | Specified | Not Run |
| FR-DAT-MEDI-001 | US-ANKI-20 | AC-ANKI-076 | TC-ANKI-076 | BR-ANKI-028 | — | boundary | Specified | Not Run |
| FR-DAT-MEDI-001 | US-ANKI-20 | AC-ANKI-077 | TC-ANKI-077 | BR-ANKI-028 | — | boundary | Specified | Not Run |
| FR-ORG-SRCH-001 | US-ANKI-06 | AC-ANKI-078 | TC-ANKI-078 | BR-ANKI-007 | — | happy | Specified | Not Run |
| FR-ORG-SRCH-001 | US-ANKI-06 | AC-ANKI-079 | TC-ANKI-079 | BR-ANKI-007 | — | boundary | Specified | Not Run |
| FR-ORG-SRCH-001 | US-ANKI-06 | AC-ANKI-080 | TC-ANKI-080 | BR-ANKI-007 | — | boundary | Specified | Not Run |
| FR-EXT-ADD-001 | US-ANKI-18 | AC-ANKI-081 | TC-ANKI-081 | BR-ANKI-026 | — | happy | Specified | Not Run |
| FR-EXT-ADD-001 | US-ANKI-18 | AC-ANKI-082 | TC-ANKI-082 | BR-ANKI-026 | — | negative | Specified | Not Run |
| FR-EXT-ADD-001 | US-ANKI-18 | AC-ANKI-083 | TC-ANKI-083 | BR-ANKI-026 | — | boundary | Specified | Not Run |
| FR-EXT-ADD-001 | US-ANKI-18 | AC-ANKI-084 | TC-ANKI-084 | BR-ANKI-026 | — | negative | Specified | Not Run |
| FR-EXT-ADD-001 | US-ANKI-18 | AC-ANKI-085 | TC-ANKI-085 | BR-ANKI-026 | — | happy | Specified | Not Run |
| FR-EXT-ADD-001 | US-ANKI-18 | AC-ANKI-086 | TC-ANKI-086 | BR-ANKI-026 | — | boundary | Specified | Not Run |

## 4. Độ phủ thiết kế và giới hạn

Công thức: số **ID phân biệt có ít nhất một TC với oracle Specified** / tổng ID trong scope của SRS hoặc AC. Đếm ID không đo số nhánh, chất lượng oracle, approval hoặc thành công runtime. Một BR có scenario đã đặc tả và scenario blocked vẫn được đếm ID đã chạm; phần chưa rõ vẫn liệt kê dưới đây.

| Tập | Có TC hợp lệ / trong scope | ID thiếu | Evidence thực thi |
|---|---|---|---|
| FR | 20/20 | — | Không có; Not Run |
| BR | 28/28 | — | Không có; Not Run |
| ERR | 8/8 | — | Không có; Not Run |
| AC | 86/86 | — | Không có; Not Run |

Tổng 86 TC: 86 Specified, 0 Design Blocked; **0/86 thực thi**. FR/BR/ERR đủ ID không chứng minh toàn bộ nhánh và toàn bộ lỗi Anki được phủ. Denominator ERR chỉ là 8 lỗi đã tái lập trong SRS.

### Kết quả làm rõ oracle và khoảng trống còn lại

035: zero-item giữ params, báo no reviews. 067: hai lượt cùng card/ngày đều tính. 072: fixture full-sync theo Cancel/Download/Upload trên server test. 077: filename chuẩn theo cursor/dirty/thứ tự request. Tất cả đã chốt thiết kế từ source; thực thi vẫn Not Run. Bằng chứng và phạm vi tại [hồ sơ phân tích](../governance/evidence-and-scope.md).

- Các nhánh chưa thiết kế đủ: optimize FSRS với đủ lịch sử/các lỗi tham số; tổ hợp FSRS short-term/steps rỗng; mọi phép đổi field/template; merge NoteType phức tạp; lỗi network/auth/disk/file hỏng/cancel; media deletion retry; network/download update hoàn chỉnh và lỗi addon ngoài guard đã nêu. ID coverage không che những nhánh này.
- Retry AnswerCard stale và equal-mtime sync/package đã có oracle; chưa có cam kết idempotency cho mọi thao tác hay concurrency xuyên thiết bị. Cần fault injection/transaction tests riêng trước khi kết luận toàn bộ NFR nguyên tử.
- Một số fixture cần cấp lõi (số field sai, state cũ, ensure_not_empty); không tuyên bố có cách tạo mọi trạng thái qua UI. UI caller fallback và localization message vẫn cần khảo sát.
- Story US-ANKI-19 có negative scenario về nguy cơ dùng chung account với oracle cụ thể; không kỳ vọng một mã lỗi trùng account chưa có trong caller. Việc thông qua thiết kế không xác nhận môi trường/harness đã hoạt động.

## 5. NFR — quản lý riêng, chưa nghiệm thu

Không cộng NFR vào denominator FR/BR/ERR. Bảng dưới là phương pháp cần chuẩn bị, chưa là test suite NFR hoàn chỉnh. Không tự đặt SLA, RPO/RTO, WCAG level hoặc ngưỡng hiệu năng.

| NFR | Cách kiểm chứng / fixture | Trạng thái và khoảng trống |
|---|---|---|
| NFR-ANKI-001 — Tính nguyên tử khi trả lời | Fault injection tại các bước AnswerCard; xác nhận card/revlog/stats cùng rollback hoặc cùng commit; fixture collection tạm; nguồn answering/mod.rs:315. | Not Run. Code observed; runtime Not Run |
| NFR-ANKI-002 — Bảo toàn lịch card cũ khi nhập apkg | Nhập gói có GUID/card ordinal cũ và mới vào fixture; so due/interval/revlog trước-sau; nguồn apkg/import/cards.rs:99. | Not Run. Code observed; runtime Not Run |
| NFR-ANKI-003 — Khả năng khôi phục | Restore backup text/scheduling và colpkg có media trên profile tạm; so số note/card và asset; đo thời gian theo kích thước thực, chưa đặt SLA; nguồn backups.mdx:7. | Not Run. As-Is scope observed; RPO/RTO TBD owner vận hành |
| NFR-ANKI-004 — Hiệu năng queue/search/import | Chọn bộ dữ liệu đại diện và máy/OS cố định; đo p50/p95, memory, số card, thời gian cold/warm; chỉ chốt ngưỡng sau bằng chứng. | Not Run. TBD owner sản phẩm/kỹ thuật; chưa benchmark |
| NFR-ANKI-005 — Tương thích giao thức và dữ liệu | Kiểm thử round-trip apkg/colpkg và sync với từng version được owner chọn; source desktop không chứng minh hành vi mobile; nguồn README.md:9 và manual/sync-server.mdx:7. | Not Run. Doc observed; matrix client/version TBD |
| NFR-ANKI-006 — Khả dụng và thao tác bàn phím | Thử Study Now/Show Answer/rating bằng bàn phím, focus và trình đọc màn hình; chưa cam kết WCAG; nguồn studying.mdx:216. | Not Run. Doc observed; accessibility audit Not Run |
| NFR-ANKI-007 — Bảo mật dữ liệu và extension | Xác lập threat model local collection/account/addons; rà credential storage, transport, log redaction, mã addon theo deployment thật; không gán encryption at rest/TLS version chưa thấy. | Not Run. TBD owner bảo mật; chưa audit |
| NFR-ANKI-008 — Tính truy vết dữ liệu học | So rating/time/type ở revlog với thao tác thực; kiểm tra cap timer, preview và manual/reschedule exclusions; nguồn answering/mod.rs:330 và stats/graphs/today.rs:17. | Not Run. Code observed; runtime Not Run |

## 6. Bàn giao, execution và CR

QA ghi môi trường, phiên bản, tester, ngày chạy, actual và evidence đã redacted khi thực thi. Chỉ đổi status sau chạy; blocked oracle phải được owner giải quyết trước khi chấp nhận kết quả. Khi CR thay quy tắc, tra RTM theo FR/BR/ERR rồi cập nhật AC/TC, giữ ID nếu cùng nghĩa, tăng version theo ảnh hưởng và trả test bị tác động về Not Run. SRS chỉ liên kết bảng RTM này.

## Câu hỏi còn mở

1. QA/dev: OS/build, clock harness và endpoint server test nào sẽ dùng khi thực thi? Bốn oracle thiết kế đã chốt, execution vẫn Not Run.
2. Owner thống kê/sản phẩm: sửa manual hay đổi implementation để xử lý discrepancy first review/day? Oracle As-Is vẫn theo code.
3. Stakeholder: ai review/duyệt bộ Draft, NFR và phạm vi hosted/mobile? Các nhánh ngoài fixture được ghi ở phần khoảng trống.

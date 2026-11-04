---
id: DOC-SRS-ANKI-001
title: "SRS As-Is tái lập Anki Desktop"
version: "1.0.1"
phase: Specification
domain: Anki
tags: [anki, as-is, reconstructed, srs]
depends_on: [DOC-BRD-ANKI-001, DOC-PRD-ANKI-001, DOC-EVID-ANKI-001]
related_diagrams: [DIAG-ERD-ANKI-001, DIAG-STATE-ANKI-001, DIAG-STATE-ANKI-002]
author: BA Agent
last_updated: "2026-11-03"
status: draft
---

# Đặc tả yêu cầu phần mềm Anki Desktop — As-Is

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---|---|---|---|
| 1.0.1 | 2026-11-03 | BA Analysis | Làm rõ oracle035/067/072/077 và truy vết liên quan; không thay source hoặc kết quả chạy |
| 1.0.0 | 2026-11-02 | BA Agent | Tái lập draft từ source/manual; 20 FR, 28 BR, 8 ERR và 8 NFR; chưa duyệt, chưa kiểm thử runtime. |

## 1. Giới thiệu

### 1.1 Mục đích

Mô tả hành vi Anki Desktop đã quan sát trong source/manual để thống nhất trao đổi BA/dev/QA. Đây là **SRS As-Is tái lập, draft**; không phải yêu cầu chính thức từ Ankitects, cam kết triển khai mới hoặc chứng nhận ứng dụng đang chạy đúng. Người dùng đã yêu cầu tạo bộ tài liệu, chưa có bằng chứng phê duyệt từng quy tắc. Ưu tiên P0/P1/P2 đều là **BA proposed**, không phải roadmap đã duyệt.

### 1.2 Phạm vi

20 năng lực: nội dung note/type/cloze/image occlusion; deck/search; review/scheduler/limits/FSRS/bury/suspend/filtered; text/package import-export; sync/backup/media; thống kê; add-on hooks; profile. Snapshot commit [`136bd42bfbd356fc756b6d3e28cc77b02da11ea7`](https://github.com/ankitects/anki/tree/136bd42bfbd356fc756b6d3e28cc77b02da11ea7); .version 26.09.3 là nhãn trong source, không chứng nhận release tương ứng.

Ngoài phạm vi chứng minh: implementation AnkiMobile/AnkiDroid, toàn bộ hosted AnkiWeb, hiệu quả ghi nhớ thực nghiệm, doanh thu, bảo mật/SLA production, hành vi addon bên thứ ba. Không xây chức năng, không sửa upstream, không chạy build/test/UI.

### 1.3 Thuật ngữ

| Thuật ngữ | Nghĩa sử dụng |
|---|---|
| Note / Card | Note giữ nội dung, tags và NoteType; Card là đơn vị ôn có deck/state/schedule riêng. |
| NoteType / Template | Cấu trúc field và mẫu sinh card; một template gồm định dạng hỏi/đáp. |
| Deck / Preset | Deck nhóm card; preset chia sẻ cấu hình học giữa deck. |
| New / Learning / Review / Relearning | Giai đoạn lịch học trong normal scheduling; Bury/Suspend là queue overlay. |
| Home deck / Filtered | Deck gốc và tập card tạm theo truy vấn; không tạo bản sao card. |
| FSRS / SM-2 | Thuật toán lập lịch mới và legacy, dùng đầu vào và công thức khác nhau. |
| Lapse / Leech | Quên card Review / card vượt ngưỡng lapse theo cấu hình. |
| Revlog / Retention | Lịch sử thao tác review / tỷ lệ nhớ theo định nghĩa chỉ số. |
| Code / Doc / Suy luận BA | Đọc implementation / đọc manual cùng commit / diễn giải cần xác nhận. |

### 1.4 Tài liệu tham chiếu

- [Danh mục nguồn và đối chiếu code](code-derived-spec.md), DOC-CODE-ANKI-001 v1.0.1.
- [Dữ liệu yêu cầu chuẩn](requirements.json), v1.0.1; đây là bản máy đọc của danh mục trong tài liệu này, không phải input ứng dụng.
- [Báo cáo học](../../../plans/reports/learning-business.md), DOC-ANALYSIS-ANKI-LEARNING-001 v1.0.1.
- [Báo cáo nội dung/dữ liệu](../../../plans/reports/content-business.md), khảo sát ngày 2026-11-02, không có version metadata.
- [Phân tích tổng hợp](../../anki-business-analysis.md), khảo sát ngày 2026-11-02.
- Source được dẫn bằng URL cố định commit và dòng ngay dưới FR/BR/ERR. Bằng chứng runtime chưa có. Không suy ra quyết định stakeholder từ báo cáo nghiên cứu.

## 2. Mô tả tổng quan

### 2.1 Bối cảnh

Vòng nghiệp vụ: soạn kiến thức → sinh card → tự kiểm tra → rating → lịch tiếp theo → theo dõi/điều chỉnh. Desktop là ứng dụng dữ liệu cá nhân; tài liệu không giả định mô hình lớp học/LMS, tenant hoặc vai trò giáo viên/admin. Repo xác nhận phạm vi computer version tại [README.md:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/README.md#L9).

### 2.2 Phân hệ

Content tạo nội dung; Organization xác định phạm vi; Learning quyết định card và lịch; Data giữ khả năng trao đổi/khôi phục; Reporting tổng hợp lịch sử; System/Extension quản lý môi trường và mở rộng. Hợp đồng chính Note → nhiều Card; sửa Note không đồng nhất lịch các sibling.

### 2.3 Người dùng

Người học, người soạn/chia sẻ bộ thẻ và người dùng nâng cao/addon author là các vai trò công việc có thể trùng nhau, không phải role phân quyền được chứng minh. Scheduler là thành phần nội bộ; dịch vụ sync là hệ thống hỗ trợ bên ngoài khi xét ranh giới desktop. Người học tự chấm độ nhớ; phần mềm không tự xác thực tri thức ngoài rating.

### 2.4 Môi trường

Lớp Rust lõi, Python bridge, PyQt GUI và TypeScript/Svelte theo [CLAUDE.md:10](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/CLAUDE.md#L10). Collection/media cục bộ; sync tới AnkiWeb hoặc endpoint self-host khi cấu hình tương thích. UI/OS/client version cụ thể để chạy nghiệm thu còn TBD; chưa đặt ma trận hỗ trợ từ suy đoán.

### 2.5 Ràng buộc

Bám commit, giữ phân biệt API desktop với HTTP service. Quy tắc có nhãn Doc chưa được coi là code/runtime verified. Không chuyển ví dụ skill thành SLA, quyền truy cập, thông báo localization hoặc chính sách mới. Mọi test downstream mặc định Not Run. Các sự kiện tranh chấp state/record được mô tả theo source, không hứa serializability xuyên thiết bị.

### 2.6 Giả định và phụ thuộc

Fixture kiểm thử cần profile/collection tạm, đồng hồ và cấu hình rõ ràng. Sync integration cần server/account thử nghiệm và ít nhất hai client; không dùng dữ liệu thật mặc định. Addon tùy biến có thể đổi đường mặc định. Source/manual mâu thuẫn phải được giữ visible; owner sản phẩm/kỹ thuật cần xác nhận trước khi biến thành baseline được duyệt.

## 3. Yêu cầu chi tiết

### 3.1 Danh mục chức năng

Tất cả FR dưới đây mô tả As-Is. P0 = vòng học hoặc bảo toàn dữ liệu, P1 = khả năng hỗ trợ, P2 = mở rộng; toàn bộ ưu tiên là BA proposed. ERR rỗng nghĩa chưa lập danh mục lỗi có đủ chứng cứ cho năng lực đó, **không có nghĩa không thể lỗi**.

#### FR-CNT-NOTE-001 — Soạn và sửa note

- **Ưu tiên:** P0 (BA proposed).
- **Input:** NoteType, field values, tags, deck đích.
- **Processing:** Kiểm tra số field, chuẩn hóa và lưu note; sinh card phù hợp, giữ lịch của card hiện có.
- **Output:** Note và card có thể học; lỗi khi cấu trúc không hợp lệ.
- **BR:** BR-ANKI-001, BR-ANKI-003.
- **ERR:** ERR-ANKI-000-01.
- **Nguồn:** [rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95).

#### FR-CNT-TYPE-001 — Quản lý NoteType, field và template

- **Ưu tiên:** P0 (BA proposed).
- **Input:** Tên, field definitions, question/answer templates.
- **Processing:** Validate cấu trúc tối thiểu; chuẩn hóa tên và cập nhật template khi đổi field.
- **Output:** NoteType cập nhật trong collection; card sinh theo cấu hình.
- **BR:** BR-ANKI-002, BR-ANKI-003.
- **ERR:** ERR-ANKI-000-02.
- **Nguồn:** [rslib/src/notetype/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/mod.rs#L484); [proto/anki/notetypes.proto:102](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/notetypes.proto#L102).

#### FR-CNT-CLOZ-001 — Tạo thẻ cloze

- **Ưu tiên:** P1 (BA proposed).
- **Input:** Note chứa c1/c2… và cloze NoteType.
- **Processing:** Trích số cloze, dùng template cloze, tạo ordinal còn thiếu.
- **Output:** Card tương ứng từng số cloze, nhiều đoạn cùng số che cùng lượt.
- **BR:** BR-ANKI-001, BR-ANKI-004.
- **ERR:** ERR-ANKI-000-01.
- **Nguồn:** [rslib/src/notetype/cardgen.rs:160](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L160); [docs-site/manual/editing.mdx:364](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L364).

#### FR-CNT-IMGO-001 — Tạo image occlusion

- **Ưu tiên:** P1 (BA proposed).
- **Input:** Ảnh, shapes/groups, header/back extra.
- **Processing:** Lưu cấu trúc occlusion kiểu cloze; tạo card theo shape/group; overlay chỉ hiển thị.
- **Output:** Note ảnh với card che vùng; xóa shape cần kiểm tra Empty Cards.
- **BR:** BR-ANKI-003, BR-ANKI-005.
- **ERR:** Chưa có entry được xác minh trong danh mục này.
- **Nguồn:** [rslib/src/image_occlusion/notetype.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/image_occlusion/notetype.rs#L59); [docs-site/manual/editing.mdx:504](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L504).

#### FR-ORG-DECK-001 — Tổ chức deck và subdeck

- **Ưu tiên:** P0 (BA proposed).
- **Input:** Deck, tên phân cấp, card cần chuyển, preset.
- **Processing:** Tổ chức card theo deck; học deck gồm descendants; card siblings có thể khác deck.
- **Output:** Cây deck và phạm vi học xác định.
- **BR:** BR-ANKI-006, BR-ANKI-012.
- **ERR:** Chưa có entry được xác minh trong danh mục này.
- **Nguồn:** [docs-site/manual/getting-started.mdx:75](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/getting-started.mdx#L75); [rslib/src/scheduler/queue/builder/mod.rs:135](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/mod.rs#L135).

#### FR-ORG-SRCH-001 — Tìm kiếm và quản lý tags/flags

- **Ưu tiên:** P0 (BA proposed).
- **Input:** Chuỗi search field/tag/flag/deck/state và toán tử; tập note/card được chọn; thao tác thêm, gỡ, đổi tên hoặc tổ chức tag; flag được chọn.
- **Processing:** Áp cú pháp search chung Browse/filtered; tìm văn bản trong field, không mặc định tags. Thêm/gỡ tag trên notes được chọn, đổi tên/tổ chức tags theo Browser; tag ở note nên siblings cùng nhận. Đặt/gỡ flag trên cards được chọn, mỗi card tối đa một flag, không thay flag siblings khác.
- **Output:** Tập note/card khớp; tags hoặc flags cập nhật đúng cấp và phạm vi lựa chọn; truy vấn đơn thuần không sửa dữ liệu.
- **BR:** BR-ANKI-007.
- **ERR:** Chưa có entry được xác minh trong danh mục này.
- **Nguồn:** [docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226).

#### FR-LRN-REV-001 — Học và tự đánh giá card

- **Ưu tiên:** P0 (BA proposed).
- **Input:** Deck, card được chọn, rating, thời gian.
- **Processing:** Hiện hỏi rồi đáp án; nhận tự chấm; commit AnswerCard sau kiểm tra state; lặp theo queue.
- **Output:** Card cập nhật, revlog, thống kê và card tiếp hoặc thông tin hết phiên.
- **BR:** BR-ANKI-006, BR-ANKI-008, BR-ANKI-011.
- **ERR:** ERR-ANKI-000-03.
- **Nguồn:** [docs-site/manual/studying.mdx:40](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L40); [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315).

#### FR-LRN-SCH-001 — Chuyển trạng thái và xếp lịch

- **Ưu tiên:** P0 (BA proposed).
- **Input:** Current state, rating, steps và cấu hình thuật toán.
- **Processing:** Tính bốn next states; áp learning/relearning/review, interval có fuzz và giới hạn.
- **Output:** Due/state mới; lapse khi thất bại Review.
- **BR:** BR-ANKI-009, BR-ANKI-010, BR-ANKI-011, BR-ANKI-013.
- **ERR:** ERR-ANKI-000-03.
- **Nguồn:** [proto/anki/scheduler.proto:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L80); [rslib/src/scheduler/states/review.rs:64](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L64).

#### FR-LRN-LIM-001 — Giới hạn khối lượng học

- **Ưu tiên:** P0 (BA proposed).
- **Input:** Preset, override deck/today, counts, cờ limits.
- **Processing:** Tính giới hạn còn lại và cây deck; gom learning/new/review theo điều kiện.
- **Output:** Queue và counts bị giới hạn; intraday vẫn có thể tiếp tục.
- **BR:** BR-ANKI-006, BR-ANKI-012.
- **ERR:** Chưa có entry được xác minh trong danh mục này.
- **Nguồn:** [rslib/src/decks/limits.rs:98](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/decks/limits.rs#L98); [rslib/src/scheduler/queue/builder/gathering.rs:23](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/gathering.rs#L23).

#### FR-LRN-FSRS-001 — Cấu hình và tối ưu FSRS

- **Ưu tiên:** P1 (BA proposed).
- **Input:** Cờ FSRS, desired retention, params, review history, reschedule choice.
- **Processing:** Bật toàn cục; tối ưu từ history theo scope; 0 training item trả nguyên params/count0/health absent; UI current preset báo không có reviews; reschedule theo lựa chọn.
- **Output:** Tham số và lịch theo nhánh; zero-item không tạo tham số cá nhân hóa mới; không cam kết đạt retention thực tế.
- **BR:** BR-ANKI-013, BR-ANKI-014.
- **ERR:** Chưa có entry được xác minh trong danh mục này.
- **Nguồn:** [rslib/src/scheduler/answering/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L484); [docs-site/manual/deck-options.mdx:406](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L406); [docs-site/manual/deck-options.mdx:500](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L500); [ts/routes/deck-options/FsrsOptions.svelte:200](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L200); [ts/routes/deck-options/FsrsOptions.svelte:225](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L225); [ts/routes/deck-options/FsrsOptions.svelte:235](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L235); [rslib/src/scheduler/service/mod.rs:264](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/service/mod.rs#L264); [rslib/src/scheduler/fsrs/params.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L95); [proto/anki/scheduler.proto:357](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L357); [ftl/core/deck-config.ftl:495](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ftl/core/deck-config.ftl#L495).

#### FR-LRN-HIDE-001 — Bury, suspend và xử lý leech

- **Ưu tiên:** P0 (BA proposed).
- **Input:** Card/note IDs, mode, sibling options, leech threshold/action.
- **Processing:** Ẩn theo mode; unbury qua rollover/manual; phát leech và tag note/suspend card theo cấu hình.
- **Output:** Card được loại/phục hồi queue; trạng thái trí nhớ nền bảo toàn.
- **BR:** BR-ANKI-015, BR-ANKI-016.
- **ERR:** Chưa có entry được xác minh trong danh mục này.
- **Nguồn:** [rslib/src/scheduler/bury_and_suspend.rs:32](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L32); [rslib/src/scheduler/answering/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L194).

#### FR-LRN-FILT-001 — Học tập mục tiêu qua filtered deck

- **Ưu tiên:** P1 (BA proposed).
- **Input:** Search/order/limit, reschedule flag, preview delays.
- **Processing:** Build tập hợp lệ; dùng home deck hoặc preview; Empty/Rebuild phục hồi rồi xây lại.
- **Output:** Deck tạm, card học và trả home; lịch đổi chỉ theo chế độ.
- **BR:** BR-ANKI-017, BR-ANKI-018, BR-ANKI-019.
- **ERR:** ERR-ANKI-000-04.
- **Nguồn:** [rslib/src/scheduler/filtered/mod.rs:123](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L123); [rslib/src/scheduler/states/preview_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/preview_filter.rs#L25).

#### FR-DAT-TEXT-001 — Nhập dữ liệu text

- **Ưu tiên:** P0 (BA proposed).
- **Input:** UTF-8 file, delimiter/mapping, GUID hoặc first field, duplicate policy.
- **Processing:** Đọc hàng; resolve type/deck; đối chiếu GUID/first field; thêm, giữ, cập nhật hoặc báo lỗi hàng.
- **Output:** Notes/cards nhập, kết quả added/updated/conflict/error; card cũ giữ lịch khi update.
- **BR:** BR-ANKI-001, BR-ANKI-020.
- **ERR:** ERR-ANKI-000-05, ERR-ANKI-000-06, ERR-ANKI-000-07.
- **Nguồn:** [rslib/src/import_export/text/import.rs:250](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L250); [rslib/src/import_export/text/import.rs:318](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L318).

#### FR-DAT-PKG-001 — Trao đổi deck/collection package

- **Ưu tiên:** P0 (BA proposed).
- **Input:** apkg/colpkg, update/merge policy, scheduling/media options.
- **Processing:** apkg merge note GUID và thêm card thiếu; colpkg thay collection; export chọn phạm vi và media.
- **Output:** Package hoặc collection cập nhật; khác biệt lịch/media theo loại gói.
- **BR:** BR-ANKI-021, BR-ANKI-022.
- **ERR:** ERR-ANKI-000-08.
- **Nguồn:** [rslib/src/import_export/package/apkg/import/notes.rs:333](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L333); [rslib/src/import_export/package/apkg/import/cards.rs:99](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/cards.rs#L99); [rslib/src/import_export/package/colpkg/import.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/colpkg/import.rs#L31).

#### FR-DAT-SYNC-001 — Đồng bộ collection

- **Ưu tiên:** P0 (BA proposed).
- **Input:** Local/remote changes, metadata/schema, tài khoản/endpoint, lựa chọn full sync.
- **Processing:** Merge record theo mtime/pending; nhập revlog; full upload/download khi cần; media riêng.
- **Output:** Collection đồng bộ theo nhánh; không hòa giải từng field.
- **BR:** BR-ANKI-023, BR-ANKI-028.
- **ERR:** Chưa có entry được xác minh trong danh mục này.
- **Nguồn:** [rslib/src/sync/collection/chunks.rs:162](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/chunks.rs#L162); [rslib/src/sync/collection/meta.rs:65](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L65).

#### FR-DAT-BACK-001 — Sao lưu và phục hồi

- **Ưu tiên:** P0 (BA proposed).
- **Input:** Collection thay đổi, lịch backup hoặc snapshot chọn restore.
- **Processing:** Tạo backup khi đủ điều kiện; restore thay dữ liệu; xuất colpkg media cho backup đầy đủ.
- **Output:** Snapshot/collection phục hồi; mất thay đổi sau snapshot; auto backup không media.
- **BR:** BR-ANKI-022, BR-ANKI-024.
- **ERR:** Chưa có entry được xác minh trong danh mục này.
- **Nguồn:** [rslib/src/collection/backup.rs:28](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/collection/backup.rs#L28); [docs-site/manual/backups.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L7); [docs-site/manual/backups.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L24).

#### FR-RPT-STAT-001 — Xem lịch sử và thống kê học

- **Ưu tiên:** P1 (BA proposed).
- **Input:** Review logs, card states, phạm vi deck/search và thời gian.
- **Processing:** Tổng hợp Today, đúng/sai, mature, retention và lịch tới hạn theo định nghĩa từng chỉ số.
- **Output:** True retention As-Is cộng từng revlog đủ điều kiện trong cửa sổ scheduler; cùng card/ngày có thể đóng góp nhiều lượt; discrepancy manual được ghi nhận.
- **BR:** BR-ANKI-025.
- **ERR:** Chưa có entry được xác minh trong danh mục này.
- **Nguồn:** [rslib/src/stats/graphs/today.rs:17](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/today.rs#L17); [rslib/src/stats/graphs/retention.rs:53](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L53); [rslib/src/storage/revlog/get.sql:1](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/get.sql#L1); [rslib/src/storage/revlog/mod.rs:122](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/mod.rs#L122); [rslib/src/storage/revlog/mod.rs:175](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/mod.rs#L175); [rslib/src/stats/graphs/mod.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/mod.rs#L31); [rslib/src/stats/graphs/retention.rs:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L16); [rslib/src/revlog/mod.rs:107](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/revlog/mod.rs#L107); [ts/routes/graphs/true-retention.ts:105](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/graphs/true-retention.ts#L105); [docs-site/manual/stats.mdx:229](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/stats.mdx#L229).

#### FR-EXT-ADD-001 — Quản lý add-on và mở rộng hooks/filters

- **Ưu tiên:** P2 (BA proposed).
- **Input:** Addon IDs hoặc package, danh sách addon chọn, yêu cầu tải/cài từ file/kiểm tra cập nhật/bật/tắt/xóa; callback hooks/filters và sự kiện ứng dụng.
- **Processing:** Tools Add-ons tải/cài package và kiểm tra cập nhật; bật/tắt ghi metadata, xử lý addon xung đột khi bật; xóa yêu cầu xác nhận. Ghi yêu cầu restart khi toggle hoặc xóa addon đang bật. Khi addon được nạp, gọi hooks/filters theo lifecycle đã định nghĩa; addon dùng chung profile.
- **Output:** Danh sách, metadata và trạng thái addon cập nhật theo kết quả; thông tin tải/cài/cập nhật/lỗi và restart khi được yêu cầu; callback chỉ tác động đúng lifecycle, không mặc nhiên mọi đường nhập.
- **BR:** BR-ANKI-026, BR-ANKI-027.
- **ERR:** Chưa có entry được xác minh trong danh mục này.
- **Nguồn:** [docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29).

#### FR-SYS-PROF-001 — Quản lý profile cục bộ

- **Ưu tiên:** P1 (BA proposed).
- **Input:** Profile được tạo/chọn và tài khoản sync tương ứng.
- **Processing:** Mở collection/settings/auth theo profile; addon dùng chung. Cùng account không được caller khảo sát bảo vệ bằng uniqueness; trên server test cùng user dùng chung remote collection, sync theo mod/schema và hướng được chọn.
- **Output:** Local paths riêng; Cancel/full Download/full Upload có kết quả dữ liệu riêng theo fixture; không phải tenant/RBAC.
- **BR:** BR-ANKI-027.
- **ERR:** Chưa có entry được xác minh trong danh mục này.
- **Nguồn:** [docs-site/manual/profiles.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/profiles.mdx#L5); [qt/aqt/profiles.py:212](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L212); [qt/aqt/profiles.py:659](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L659); [qt/aqt/profiles.py:681](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L681); [qt/aqt/sync.py:307](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L307); [rslib/src/sync/http_server/mod.rs:122](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/http_server/mod.rs#L122); [rslib/src/sync/collection/meta.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L59); [qt/aqt/sync.py:138](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L138); [rslib/src/sync/collection/download.rs:35](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/download.rs#L35); [rslib/src/sync/collection/upload.rs:79](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/upload.rs#L79); [rslib/src/sync/collection/tests.rs:591](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/tests.rs#L591).

#### FR-DAT-MEDI-001 — Quản lý và kiểm tra media

- **Ưu tiên:** P0 (BA proposed).
- **Input:** Tham chiếu media, collection.media, trạng thái sync.
- **Processing:** Check thiếu/không dùng; sync media fetch remote trước upload pending, xử lý checksum/dirty/cursor; static template media dùng _.
- **Output:** Danh sách vấn đề và dữ liệu media theo nhánh; cùng filename chuẩn/khác hash có oracle xác định khi cố định cursor, dirty và thứ tự sync.
- **BR:** BR-ANKI-028.
- **ERR:** Chưa có entry được xác minh trong danh mục này.
- **Nguồn:** [docs-site/manual/media.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/media.mdx#L24); [docs-site/manual/syncing.mdx:54](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/syncing.mdx#L54); [rslib/src/sync/media/syncer.rs:60](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/syncer.rs#L60); [rslib/src/sync/media/changes.rs:44](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/changes.rs#L44); [rslib/src/media/files.rs:403](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L403); [rslib/src/sync/media/database/client/mod.rs:206](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/client/mod.rs#L206); [rslib/src/sync/media/database/server/entry/upload.rs:35](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/server/entry/upload.rs#L35); [rslib/src/sync/media/tests.rs:278](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/tests.rs#L278); [rslib/src/backend/sync.rs:188](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/backend/sync.rs#L188); [rslib/src/sync/media/database/client/changetracker.rs:56](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/client/changetracker.rs#L56); [rslib/src/media/files.rs:165](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L165).

### 3.2 Quy tắc nghiệp vụ

Các BR là ID BA mới của bộ SRS, không phải enum/runtime ID. Bảng ánh xạ nhãn báo cáo cũ ở code-derived-spec; giữ nguyên báo cáo lịch sử. Từ WHEN/THEN/UNLESS để chỉ điều kiện/hành vi/ngoại lệ, không chứng minh ngưỡng đã được stakeholder phê duyệt.

#### BR-ANKI-001 — Cấu trúc note hợp lệ

- **WHEN:** Lưu note với NoteType.
- **THEN:** Số field values bằng số field NoteType; nội dung/tags ở note, lịch ở card.
- **UNLESS / giới hạn:** Không suy ra note thuộc đúng một deck.
- **Nguồn:** [rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194).

#### BR-ANKI-002 — NoteType tối thiểu

- **WHEN:** Thêm/cập nhật NoteType.
- **THEN:** Có ít nhất một field, một template và tên không rỗng.
- **UNLESS / giới hạn:** Các bước chuẩn hóa tên được áp dụng trước/sau guard tương ứng; không suy ra UI trả nguyên thông báo kỹ thuật.
- **Nguồn:** [rslib/src/notetype/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/mod.rs#L484).

#### BR-ANKI-003 — Sinh card theo nội dung

- **WHEN:** Sinh card normal.
- **THEN:** Chỉ thêm ordinal chưa có với mặt hỏi render được; template có thể override deck.
- **UNLESS / giới hạn:** ensure_not_empty có fallback ordinal 0; card trở thành rỗng không tự bị xóa ngay.
- **Nguồn:** [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95).

#### BR-ANKI-004 — Sinh cloze

- **WHEN:** Note có cloze numbers.
- **THEN:** Các số cloze khác nhau sinh card khác nhau; cùng số dùng cùng card, template đầu tiên.
- **UNLESS / giới hạn:** Không coi mỗi vùng văn bản là một note.
- **Nguồn:** [rslib/src/notetype/cardgen.rs:160](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L160).

#### BR-ANKI-005 — Image occlusion

- **WHEN:** Tạo shape/group trên ảnh.
- **THEN:** Shape hoặc nhóm có thể tạo card cloze; text overlay không tạo card.
- **UNLESS / giới hạn:** Xóa shape không tự xóa card cũ; dùng Empty Cards.
- **Nguồn:** [docs-site/manual/editing.mdx:504](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L504).

#### BR-ANKI-006 — Phạm vi deck

- **WHEN:** Chọn deck học.
- **THEN:** Lấy card deck được chọn và descendants; card có một deck hiện tại.
- **UNLESS / giới hạn:** Siblings có thể nằm khác deck; filtered giữ home deck riêng.
- **Nguồn:** [docs-site/manual/studying.mdx:10](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L10).

#### BR-ANKI-007 — Tìm kiếm và cấp tác động tags/flags

- **WHEN:** Tìm trong Browse/filtered hoặc quản lý tags/flags trên tập được chọn.
- **THEN:** Search field trả card/note khớp theo chế độ; AND/OR/NOT và tag/flag/deck filters giới hạn tập. Thêm/gỡ/đổi tên/tổ chức tags tác động note; siblings cùng note chia sẻ tag. Flag tác động card được chọn, tối đa một flag tại một thời điểm.
- **UNLESS / giới hạn:** Văn bản đơn không tự tìm tags; tìm kiếm không sửa dữ liệu; đặt flag một card không đổi flag sibling khác; phạm vi rename/organize tag theo Browser khác với thêm/gỡ trên selection.
- **Nguồn:** [docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226).

#### BR-ANKI-008 — Ý nghĩa rating

- **WHEN:** Người học xem đáp án và đánh giá.
- **THEN:** Again là không nhớ/sai; Hard, Good, Easy là nhớ với mức nỗ lực khác nhau.
- **UNLESS / giới hạn:** Hard không thay Again khi quên; không đo được hiểu biết ngoài tín hiệu tự chấm.
- **Nguồn:** [docs-site/manual/studying.mdx:58](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L58).

#### BR-ANKI-009 — Chuyển learning

- **WHEN:** Card New/Learning có steps.
- **THEN:** Again về bước đầu; Good tiến; Hard lặp bước với công thức riêng ở bước đầu; Easy sang Review.
- **UNLESS / giới hạn:** Steps rỗng hoặc FSRS short-term có nhánh khác; không ép mọi card đi qua số bước cố định.
- **Nguồn:** [rslib/src/scheduler/states/learning.rs:39](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/learning.rs#L39).

#### BR-ANKI-010 — Lapse và relearning

- **WHEN:** Card Review nhận Again.
- **THEN:** Tăng lapse, tính lịch mới và vào Relearning nếu có steps; trả lời đúng tiếp tục Review.
- **UNLESS / giới hạn:** Again trong Relearning không tự tăng lapse lần nữa; không steps có thể về thẳng Review.
- **Nguồn:** [rslib/src/scheduler/states/review.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L95).

#### BR-ANKI-011 — Ghi answer nguyên tử

- **WHEN:** Nhận AnswerCard.
- **THEN:** So current state sau hiệu chỉnh elapsed seconds; trong transaction áp dụng state, revlog, stats, bury và lưu card.
- **UNLESS / giới hạn:** State khác bị từ chối; cap thời gian theo preset; không tuyên bố xử lý mọi xung đột client.
- **Nguồn:** [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315).

#### BR-ANKI-012 — Hạn mức học

- **WHEN:** Xây queue hôm nay.
- **THEN:** Ưu tiên mức today rồi deck rồi preset, trừ số đã học; mặc định new cũng tiêu thụ review limit.
- **UNLESS / giới hạn:** New cards ignore review limit tách new; parent limits áp dụng theo cờ; intraday learning không bị review limit chặn như interday.
- **Nguồn:** [rslib/src/decks/limits.rs:98](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/decks/limits.rs#L98).

#### BR-ANKI-013 — FSRS và SM-2

- **WHEN:** Tính next states.
- **THEN:** FSRS dùng memory state, retention, elapsed days, tham số; legacy dùng interval/ease/multiplier.
- **UNLESS / giới hạn:** Không sử dụng công thức ease SM-2 giải thích interval FSRS.
- **Nguồn:** [rslib/src/scheduler/answering/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L484).

#### BR-ANKI-014 — Cấu hình FSRS

- **WHEN:** Bật FSRS hoặc đổi tham số/retention.
- **THEN:** FSRS bật toàn cục; optimize từ lịch sử; reschedule on change quyết định cập nhật due cũ. Optimize current preset có 0 training item trả nguyên current_params, fsrs_items=0, health_check_passed absent; UI báo deck-config-fsrs-params-no-reviews và không gán params mới.
- **UNLESS / giới hạn:** Không đồng nhất raw revlog count với training items; không áp nhánh này cho Optimize All hoặc assignment chưa lưu. Retention là mục tiêu, không bảo đảm kết quả; runtime chưa chạy.
- **Nguồn:** [docs-site/manual/deck-options.mdx:406](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L406); [ts/routes/deck-options/FsrsOptions.svelte:200](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L200); [ts/routes/deck-options/FsrsOptions.svelte:225](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L225); [ts/routes/deck-options/FsrsOptions.svelte:235](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L235); [rslib/src/scheduler/service/mod.rs:264](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/service/mod.rs#L264); [rslib/src/scheduler/fsrs/params.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L95); [proto/anki/scheduler.proto:357](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L357); [ftl/core/deck-config.ftl:495](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ftl/core/deck-config.ftl#L495).

#### BR-ANKI-015 — Bury và suspend

- **WHEN:** Ẩn card khỏi queue.
- **THEN:** Bury được phục hồi khi rollover ngày hoặc unbury; suspend tới khi unsuspend; không bury card suspended.
- **UNLESS / giới hạn:** Có tùy chọn bury interday learning; manual studying diễn đạt cũ không đủ phân biệt intraday/interday.
- **Nguồn:** [rslib/src/scheduler/bury_and_suspend.rs:32](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L32).

#### BR-ANKI-016 — Leech

- **WHEN:** Review lapse đạt threshold dương.
- **THEN:** Đánh dấu tại threshold rồi mỗi ceil(threshold/2); tag leech ở note; suspend nếu cấu hình yêu cầu.
- **UNLESS / giới hạn:** Threshold 0 không kích hoạt; leech action có thể chỉ tag.
- **Nguồn:** [rslib/src/scheduler/states/review.rs:292](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L292).

#### BR-ANKI-017 — Tập filtered

- **WHEN:** Build/Rebuild filtered deck.
- **THEN:** Search/order/limit lấy card, loại suspended/buried/đang filtered; rebuild trả thẻ cũ về rồi tìm lại.
- **UNLESS / giới hạn:** Zero result không được phép rỗng trả lỗi; đây là card tạm di chuyển, không copy.
- **Nguồn:** [rslib/src/scheduler/filtered/mod.rs:123](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L123).

#### BR-ANKI-018 — Filtered reschedule

- **WHEN:** Học filtered với reschedule bật.
- **THEN:** Dùng home deck settings; chuyển Review thì trả home, learning/relearning còn trong filtered.
- **UNLESS / giới hạn:** Review trước hạn có thuật toán riêng; không hứa lùi thêm nguyên interval.
- **Nguồn:** [rslib/src/scheduler/states/rescheduling_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/rescheduling_filter.rs#L25).

#### BR-ANKI-019 — Filtered preview

- **WHEN:** Học filtered với reschedule tắt.
- **THEN:** Again/Hard/Good dùng delay; Easy hoặc bất kỳ delay=0 kết thúc, phục hồi home/queue.
- **UNLESS / giới hạn:** Vẫn có revlog; last_review_time không cập nhật như normal study.
- **Nguồn:** [rslib/src/scheduler/states/preview_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/preview_filter.rs#L25).

#### BR-ANKI-020 — Text import định danh

- **WHEN:** Nhập hàng text.
- **THEN:** Có GUID ưu tiên GUID; không GUID dùng first field và NoteType, có thể giới hạn deck; chọn update/preserve/duplicate.
- **UNLESS / giới hạn:** GUID có sẵn không tạo duplicate; NoteType xung đột ghi conflicting; first field rỗng/missing deck/type ghi lỗi hàng.
- **Nguồn:** [rslib/src/import_export/text/import.rs:318](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L318).

#### BR-ANKI-021 — Package merge và lịch cũ

- **WHEN:** Nhập apkg.
- **THEN:** Nhận diện note bằng GUID; policy IfNewer/Always/Never; card cũ theo note/template giữ lịch, chỉ nhập log card mới.
- **UNLESS / giới hạn:** Always vẫn bỏ khi mtime bằng nhau; không merge Normal/Cloze.
- **Nguồn:** [rslib/src/import_export/package/apkg/import/notes.rs:333](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L333).

#### BR-ANKI-022 — Phạm vi package

- **WHEN:** Export/import apkg hoặc colpkg.
- **THEN:** apkg bổ sung/cập nhật; colpkg thay collection và mang scheduling; tùy chọn media khi xuất.
- **UNLESS / giới hạn:** Import colpkg không xóa media cũ ngoài package; không có scheduling thì bản chia sẻ loại dữ liệu scheduling và marked/leech.
- **Nguồn:** [docs-site/manual/exporting.mdx:34](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/exporting.mdx#L34).

#### BR-ANKI-023 — Sync record và full sync

- **WHEN:** Đồng bộ collection.
- **THEN:** Note/Card remote thay local khi local không pending hoặc remote mtime lớn hơn; revlog được nhập; khác schema yêu cầu full sync.
- **UNLESS / giới hạn:** Không merge từng field; cùng mtime với local pending không thay local tại bước đó; upload/download chọn một phía collection.
- **Nguồn:** [rslib/src/sync/collection/chunks.rs:162](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/chunks.rs#L162).

#### BR-ANKI-024 — Backup và phục hồi

- **WHEN:** Tạo backup tự động hoặc restore.
- **THEN:** Backup tự động giữ text/scheduling, không media; restore quay về snapshot và mất thay đổi sau đó.
- **UNLESS / giới hạn:** Không đổi collection thì bỏ backup kể cả force; muốn có media xuất colpkg Include Media.
- **Nguồn:** [rslib/src/collection/backup.rs:28](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/collection/backup.rs#L28).

#### BR-ANKI-025 — Đơn vị thống kê

- **WHEN:** Tổng hợp Today và retention.
- **THEN:** Today đếm lượt trả lời, Hard/Good/Easy là đúng; bỏ Manual/Rescheduled; mature theo interval trước >=21 ngày. True retention đếm mỗi revlog qua ease>0 và không phải Filtered factor=0, đồng thời type=Review hoặc lastIvl<=-86400 hoặc lastIvl>=1. Không dedup card/ngày; raw lastIvl>=21 là mature; Again fail, Hard/Good/Easy pass. Mỗi cửa sổ tính [start,end) theo next_day_at.
- **UNLESS / giới hạn:** Manual mô tả first review/card/day nhưng pipeline code không thực hiện; discrepancy còn cần quyết định To-Be. Search/days giới hạn dữ liệu trước tổng hợp; oracle toàn lịch sử dùng days=0. Retention và Today có predicate riêng.
- **Nguồn:** [rslib/src/stats/graphs/today.rs:17](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/today.rs#L17); [rslib/src/storage/revlog/get.sql:1](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/get.sql#L1); [rslib/src/storage/revlog/mod.rs:122](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/mod.rs#L122); [rslib/src/storage/revlog/mod.rs:175](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/mod.rs#L175); [rslib/src/stats/graphs/mod.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/mod.rs#L31); [rslib/src/stats/graphs/retention.rs:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L16); [rslib/src/stats/graphs/retention.rs:53](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L53); [rslib/src/revlog/mod.rs:107](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/revlog/mod.rs#L107); [ts/routes/graphs/true-retention.ts:105](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/graphs/true-retention.ts#L105); [docs-site/manual/stats.mdx:229](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/stats.mdx#L229).

#### BR-ANKI-026 — Quản lý addon và phạm vi hook

- **WHEN:** Người dùng quản lý addon hoặc addon đăng ký hooks/filters.
- **THEN:** Manager nhận ID/package, cài/kiểm tra cập nhật, bật/tắt và xóa addon được chọn; bật ghi metadata và xử lý xung đột; xóa cần xác nhận; toggle hoặc xóa addon đang bật yêu cầu restart. Hook/filter chạy theo lifecycle, nhiều addon gọi tuần tự.
- **UNLESS / giới hạn:** Không suy ra mọi thay đổi có hiệu lực tức thì trước restart; hủy xác nhận xóa không xóa addon; note_will_be_added không chạy khi import; sync_did_finish không bảo đảm media hoàn tất; tương thích addon phụ thuộc phiên bản và chưa kiểm thử bên thứ ba.
- **Nguồn:** [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29); [docs-site/manual/addons.mdx:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L16).

#### BR-ANKI-027 — Cách ly profile

- **WHEN:** Chuyển/tạo profile.
- **THEN:** Mỗi profile giữ collection/settings và sync auth riêng, addon dùng chung. Caller khảo sát không reject account trùng profile; cùng user SimpleServer dẫn tới cùng server collection. Với local/remote nonempty, mod khác và schema khác: cho Upload/Download; Cancel không transfer, Download thay local, Upload thay server; profile local khác chưa sync không tự thay đổi.
- **UNLESS / giới hạn:** Manual khuyến cáo một account cho một profile để tránh ghi đè, không phải guard uniqueness đã quan sát. Mod bằng có thể NoChanges; schema chung có thể normal merge. Không coi profile là tenant/RBAC. Hosted implementation chưa xác minh.
- **Nguồn:** [docs-site/manual/profiles.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/profiles.mdx#L5); [qt/aqt/profiles.py:212](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L212); [qt/aqt/profiles.py:659](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L659); [qt/aqt/profiles.py:681](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L681); [qt/aqt/sync.py:307](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L307); [rslib/src/sync/http_server/mod.rs:122](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/http_server/mod.rs#L122); [rslib/src/sync/collection/meta.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L59); [qt/aqt/sync.py:138](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L138); [rslib/src/sync/collection/download.rs:35](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/download.rs#L35); [rslib/src/sync/collection/upload.rs:79](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/upload.rs#L79); [rslib/src/sync/collection/tests.rs:591](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/tests.rs#L591).

#### BR-ANKI-028 — Media độc lập

- **WHEN:** Sync hoặc Check Media.
- **THEN:** Media sync riêng với collection; check tìm file thiếu/không dùng. Sync đăng ký thay đổi local, fetch remote mới trước upload pending. Tên chuẩn trùng nhưng hash khác: remote change chưa nhận làm download ghi đè dù local dirty rồi đánh clean. Nếu cursor đã bằng server và chỉ local dirty, upload thay server; winner phụ thuộc thứ tự request và cursor.
- **UNLESS / giới hạn:** Không quét tham chiếu trong template; static media dùng _. Sequential từ nền trống C1→C2 nhận nội dung C1; không suy thành quy tắc first/last writer cho mọi race. Local add_file collision/filename normalization là nhánh khác; không bảo đảm rollback filesystem khi lỗi; oracle server test cùng commit.
- **Nguồn:** [docs-site/manual/media.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/media.mdx#L24); [rslib/src/sync/media/syncer.rs:60](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/syncer.rs#L60); [rslib/src/sync/media/changes.rs:44](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/changes.rs#L44); [rslib/src/media/files.rs:403](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L403); [rslib/src/sync/media/database/client/mod.rs:206](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/client/mod.rs#L206); [rslib/src/sync/media/database/server/entry/upload.rs:35](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/server/entry/upload.rs#L35); [rslib/src/sync/media/tests.rs:278](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/tests.rs#L278); [rslib/src/backend/sync.rs:188](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/backend/sync.rs#L188); [rslib/src/sync/media/database/client/changetracker.rs:56](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/client/changetracker.rs#L56); [rslib/src/media/files.rs:165](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L165).

### 3.3 Giao diện ngoài

| Giao diện | Input/output và ranh giới |
|---|---|
| UI | Deck overview, editor, reviewer, Browser, Deck Options, import/export, sync/backup và stats; đường user-facing được mô tả trong FR. |
| Scheduler RPC | GetQueuedCards trả card/state/count; AnswerCard nhận current/new state và rating. Protobuf là contract giữa lớp ứng dụng, không mặc định REST API công khai. [proto/anki/scheduler.proto:17](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L17); [proto/anki/scheduler.proto:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L80). |
| File | Text UTF-8 với mapping; apkg/colpkg khác phạm vi thay dữ liệu; media là file tham chiếu. FR-DAT-TEXT/PKG/MEDI và BR-020–028 điều chỉnh. |
| Sync | Client/server trao collection changes; schema có thể buộc full sync; media riêng. Không mô tả nội bộ hosted AnkiWeb. [rslib/src/sync/collection/meta.rs:65](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L65). |
| Addon | Python hooks/filters; callback chỉ chạy ở lifecycle được định nghĩa. [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7). |
| Thiết bị | Bàn phím/chuột, âm thanh/hình theo UI và media; không có yêu cầu phần cứng tối thiểu được xác nhận trong nghiên cứu. |

### 3.4 Phi chức năng

ISO/IEC 25010 dùng như khung phân loại; không tuyên bố chứng nhận. Không có SLA, P95, uptime, RPO/RTO, TLS version hoặc encryption-at-rest nào được tự đặt. Mục TBD là yêu cầu cần khảo sát/chốt, không phải hành vi hiện tại đã xác minh.

| ID | Nội dung | Trạng thái | Điều kiện/phương pháp kiểm chứng |
|---|---|---|---|
| NFR-ANKI-001 | Tính nguyên tử khi trả lời | Code observed; runtime Not Run | Fault injection tại các bước AnswerCard; xác nhận card/revlog/stats cùng rollback hoặc cùng commit; fixture collection tạm; nguồn answering/mod.rs:315. |
| NFR-ANKI-002 | Bảo toàn lịch card cũ khi nhập apkg | Code observed; runtime Not Run | Nhập gói có GUID/card ordinal cũ và mới vào fixture; so due/interval/revlog trước-sau; nguồn apkg/import/cards.rs:99. |
| NFR-ANKI-003 | Khả năng khôi phục | As-Is scope observed; RPO/RTO TBD owner vận hành | Restore backup text/scheduling và colpkg có media trên profile tạm; so số note/card và asset; đo thời gian theo kích thước thực, chưa đặt SLA; nguồn backups.mdx:7. |
| NFR-ANKI-004 | Hiệu năng queue/search/import | TBD owner sản phẩm/kỹ thuật; chưa benchmark | Chọn bộ dữ liệu đại diện và máy/OS cố định; đo p50/p95, memory, số card, thời gian cold/warm; chỉ chốt ngưỡng sau bằng chứng. |
| NFR-ANKI-005 | Tương thích giao thức và dữ liệu | Doc observed; matrix client/version TBD | Kiểm thử round-trip apkg/colpkg và sync với từng version được owner chọn; source desktop không chứng minh hành vi mobile; nguồn README.md:9 và manual/sync-server.mdx:7. |
| NFR-ANKI-006 | Khả dụng và thao tác bàn phím | Doc observed; accessibility audit Not Run | Thử Study Now/Show Answer/rating bằng bàn phím, focus và trình đọc màn hình; chưa cam kết WCAG; nguồn studying.mdx:216. |
| NFR-ANKI-007 | Bảo mật dữ liệu và extension | TBD owner bảo mật; chưa audit | Xác lập threat model local collection/account/addons; rà credential storage, transport, log redaction, mã addon theo deployment thật; không gán encryption at rest/TLS version chưa thấy. |
| NFR-ANKI-008 | Tính truy vết dữ liệu học | Code observed; runtime Not Run | So rating/time/type ở revlog với thao tác thực; kiểm tra cap timer, preview và manual/reschedule exclusions; nguồn answering/mod.rs:330 và stats/graphs/today.rs:17. |

Nguồn neo của các invariant NFR: [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315); [rslib/src/import_export/package/apkg/import/cards.rs:99](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/cards.rs#L99); [docs-site/manual/backups.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L7); [docs-site/manual/studying.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L216); [rslib/src/stats/graphs/today.rs:17](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/today.rs#L17).

### 3.5 Ma trận lỗi

**Quy ước dự án:** `ERR-ANKI-000-xx` là nhãn phân tích; `000` nghĩa **không phân loại HTTP**, HTTP luôn N/A trong bảng. Không tuyên bố đây là mã do Anki trả. Trường observed symbol là log/enum/guard thấy trong mã, không phải localization key. Các câu UI tiếng Việt là mô tả BA về phản hồi cần hiểu, chưa xác minh wording giao diện; không sao chép thành localization ứng dụng.

| ID | HTTP | Trigger | Kết quả kỹ thuật được quan sát | Localization key | Diễn giải UI (BA, chưa xác minh) | Severity (BA) | Next action (BA) |
|---|---|---|---|---|---|---|---|
| ERR-ANKI-000-01 | N/A | Note có số field values khác NoteType | Từ chối lưu qua guard; UI/localization chưa truy vết | Chưa xác minh | Cấu trúc note không phù hợp NoteType | Medium | Kiểm tra mapping/NoteType trước khi lưu lại |
| ERR-ANKI-000-02 | N/A | NoteType thiếu field/template hoặc tên rỗng | Từ chối ở guard tương ứng; không giả định HTTP | Chưa xác minh | NoteType cần tên, field và template hợp lệ | Medium | Bổ sung cấu trúc thiếu |
| ERR-ANKI-000-03 | N/A | AnswerCard gửi current state không còn khớp | Từ chối với invalid input sau hiệu chỉnh elapsed seconds; UI key chưa xác minh | Chưa xác minh | Card đã thay đổi, cần tải lại trạng thái | High | Tải lại card trước khi đánh giá lại |
| ERR-ANKI-000-04 | N/A | Build filtered không tìm thấy card và allow_empty=false | SearchReturnedNoCards, không chấp nhận kết quả thao tác | Chưa xác minh | Không có card phù hợp để tạo filtered deck | Medium | Kiểm tra query và card bị loại |
| ERR-ANKI-000-05 | N/A | Text row có first field rỗng | Đưa vào log.empty_first_field và tiếp tục các hàng khác | Chưa xác minh | Hàng nhập thiếu field đầu | Medium | Sửa hàng rồi nhập lại |
| ERR-ANKI-000-06 | N/A | Text row không giải được deck hoặc NoteType | Ghi missing_deck hoặc missing_notetype trong kết quả hàng | Chưa xác minh | Không tìm thấy deck/NoteType cho hàng | Medium | Sửa mapping hoặc định danh |
| ERR-ANKI-000-07 | N/A | Note import đối chiếu GUID nhưng NoteType không tương thích | Ghi conflicting, không cập nhật note như một match hợp lệ | Chưa xác minh | Nội dung trùng có NoteType không tương thích | Medium | Chọn NoteType đúng hoặc quy trình import phù hợp |
| ERR-ANKI-000-08 | N/A | Merge NoteType Normal với Cloze trong package | Trả ImportError::NotetypeKindMergeConflict | Chưa xác minh | Không thể gộp hai loại NoteType | High | Giữ riêng NoteType hoặc chọn cách nhập khác |

- ERR-ANKI-000-01: [rslib/src/notes/mod.rs:198](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L198).
- ERR-ANKI-000-02: [rslib/src/notetype/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/mod.rs#L484).
- ERR-ANKI-000-03: [rslib/src/scheduler/answering/mod.rs:335](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L335).
- ERR-ANKI-000-04: [rslib/src/scheduler/filtered/mod.rs:178](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L178).
- ERR-ANKI-000-05: [rslib/src/import_export/text/import.rs:252](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L252).
- ERR-ANKI-000-06: [rslib/src/import_export/text/import.rs:266](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L266).
- ERR-ANKI-000-07: [rslib/src/import_export/text/import.rs:401](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L401).
- ERR-ANKI-000-08: [rslib/src/import_export/package/apkg/import/notes.rs:234](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L234).

Lỗi mạng, authentication, file hỏng, hết dung lượng, hủy thao tác và lỗi addon chưa có danh mục đầy đủ. Không dùng 8 entry này để tuyên bố error coverage toàn ứng dụng. Text import là kết quả từng hàng; không đồng nhất row failure với rollback toàn file. Trình tự validation cụ thể đã đọc ở nguồn FR-DAT-TEXT-001 và BR-011 cho AnswerCard.

## 4. Phụ lục

### 4.1 Mô hình và sơ đồ

Normal states: New → Learning → Review; Review + Again → Relearning nếu có steps; Easy có thể bỏ qua steps; FSRS short-term có ngoại lệ. Filtered gồm Preview hoặc Rescheduling; Bury/Suspend là queue overlay. Contract [proto/anki/scheduler.proto:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L80) là nguồn cấu trúc. Sơ đồ và ERD downstream đang được quản lý riêng; không cấp diagram ID trước khi file tồn tại.

### 4.2 Truy vết

20 FR / 28 BR / 8 ERR / 8 NFR định nghĩa tại đây và requirements.json. [Code-derived matrix](code-derived-spec.md) nối FR với nguồn và phân loại chứng cứ. QA sở hữu RTM tại `docs/anki/test/test-cases.md`; không sao chép một RTM khác ở SRS.

| Tài liệu downstream dự kiến | ID dự kiến do controller cấp | Trạng thái tại lúc tạo SRS |
|---|---|---|
| userstories/backlog.md | DOC-US-ANKI-001 | Draft v1.0.1; đã tạo và đối chiếu ID |
| userstories/acceptance-criteria.md | DOC-AC-ANKI-001 | Draft v1.0.1; đã tạo và đối chiếu ID |
| test/test-cases.md | DOC-TC-ANKI-001 | Draft v1.0.1; RTM 86 test, 86 oracle đã đặc tả, 0 design blocker; tất cả Not Run |

Không có tuyên bố coverage runtime. Coverage thiết kế downstream phải tính ID riêng biệt và công bố tử/mẫu; NFR và unknowns được theo dõi riêng.

### 4.3 Câu hỏi mở và quyết định cần xác nhận

| Điểm | Chứng cứ/giới hạn | Owner cần xác nhận |
|---|---|---|
| Bury interday learning | studying.mdx:208 diễn đạt chỉ new/review, nhưng deck-options.mdx:334 và burying.rs:62 hỗ trợ interday. SRS theo code hiện tại, phân biệt intraday. | Chủ tài liệu/scheduler |
| True retention first/day | Đã chốt As-Is: SQL → Rust → UI đếm mọi log đủ điều kiện; AC/TC-067 có oracle 2 lượt, 50.0%. Manual first/day khác code; quyết định sửa tài liệu hay sản phẩm còn mở. | Chủ chỉ số/QA |
| Package Always | notes.rs:521 dùng mtime khác nhau, không cập nhật khi bằng nhau; cần xác nhận intent/UI. | Import maintainer |
| Fallback card rỗng | cardgen.rs:107 có ensure_not_empty; chưa xác định toàn bộ caller UI/API. | Content maintainer |
| Media filename conflict | Đã chốt AC/TC-077 cho tên chuẩn, dirty/cursor và thứ tự sync xác định; fetch remote trước upload. Race không cố định lịch và hosted implementation ngoài oracle này. | Sync maintainer |
| Runtime và NFR | Chưa chạy ứng dụng/tests, chưa có benchmark/threat model/client matrix. | QA/kỹ thuật/sản phẩm |
| Phê duyệt | Chưa có người/thời điểm phê duyệt nội dung hoặc priority; tài liệu giữ draft. | Stakeholder |

Nguồn các chênh lệch: [docs-site/manual/studying.mdx:208](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L208); [docs-site/manual/deck-options.mdx:334](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L334); [rslib/src/scheduler/queue/builder/burying.rs:62](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/burying.rs#L62); [docs-site/manual/stats.mdx:229](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/stats.mdx#L229); [rslib/src/stats/graphs/retention.rs:53](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L53); [rslib/src/import_export/package/apkg/import/notes.rs:521](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L521); [rslib/src/notetype/cardgen.rs:107](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L107).


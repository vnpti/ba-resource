---
id: DOC-US-ANKI-001
title: "Backlog User Story Anki Desktop — As-Is"
version: "1.0.1"
phase: Backlog
domain: Anki
tags: [anki, as-is, reconstructed, qa, draft]
depends_on: ["DOC-SRS-ANKI-001"]
related_diagrams: []
author: BA Agent
last_updated: "2026-11-03"
status: draft
---

# Backlog User Story Anki Desktop — As-Is

## Lịch sử sửa đổi

| Phiên bản | Ngày | Tác giả | Nội dung |
|---|---|---|---|
| 1.0.1 | 2026-11-03 | BA Analysis | Làm rõ oracle035/067/072/077 và truy vết liên quan; không thay source hoặc kết quả chạy |
| 1.0.0 | 2026-11-02 | BA Agent | Tái lập As-Is từ SRS v1.0.0; Draft, chưa phê duyệt, chưa thực thi kiểm thử. |

Nguồn: [SRS](../srs/spec.md) (DOC-SRS-ANKI-001 v1.0.1), [requirements.json](../srs/requirements.json) v1.0.1. 20 story theo đúng thứ tự 20 FR; không phải đề xuất xây lại toàn bộ Anki. Actor là vai trò công việc, không phải role phân quyền. Toàn bộ **Draft**, story points **TBD**, priority **BA proposed**. Chưa có người/thời điểm duyệt; không story nào được gọi Ready hoặc Done.

## Danh mục

| Story | Nội dung | FR | Ưu tiên | Points | AC | Trạng thái |
|---|---|---|---|---|---|---|
| [US-ANKI-01](#us-anki-01) | Soạn và sửa note | FR-CNT-NOTE-001 | P0 (BA proposed) | TBD | AC-ANKI-001, AC-ANKI-002, AC-ANKI-003, AC-ANKI-004 | Draft |
| [US-ANKI-02](#us-anki-02) | Quản lý NoteType, field và template | FR-CNT-TYPE-001 | P0 (BA proposed) | TBD | AC-ANKI-005, AC-ANKI-006, AC-ANKI-007 | Draft |
| [US-ANKI-03](#us-anki-03) | Tạo thẻ cloze | FR-CNT-CLOZ-001 | P1 (BA proposed) | TBD | AC-ANKI-008, AC-ANKI-009, AC-ANKI-010 | Draft |
| [US-ANKI-04](#us-anki-04) | Tạo image occlusion | FR-CNT-IMGO-001 | P1 (BA proposed) | TBD | AC-ANKI-011, AC-ANKI-012, AC-ANKI-013 | Draft |
| [US-ANKI-05](#us-anki-05) | Tổ chức deck và subdeck | FR-ORG-DECK-001 | P0 (BA proposed) | TBD | AC-ANKI-014, AC-ANKI-015, AC-ANKI-016 | Draft |
| [US-ANKI-06](#us-anki-06) | Tìm kiếm và quản lý tags/flags | FR-ORG-SRCH-001 | P0 (BA proposed) | TBD | AC-ANKI-017, AC-ANKI-018, AC-ANKI-019, AC-ANKI-078, AC-ANKI-079, AC-ANKI-080 | Draft |
| [US-ANKI-07](#us-anki-07) | Học và tự đánh giá card | FR-LRN-REV-001 | P0 (BA proposed) | TBD | AC-ANKI-020, AC-ANKI-021, AC-ANKI-022, AC-ANKI-023 | Draft |
| [US-ANKI-08](#us-anki-08) | Chuyển trạng thái và xếp lịch | FR-LRN-SCH-001 | P0 (BA proposed) | TBD | AC-ANKI-024, AC-ANKI-025, AC-ANKI-026, AC-ANKI-027 | Draft |
| [US-ANKI-09](#us-anki-09) | Giới hạn khối lượng học | FR-LRN-LIM-001 | P0 (BA proposed) | TBD | AC-ANKI-028, AC-ANKI-029, AC-ANKI-030, AC-ANKI-031 | Draft |
| [US-ANKI-10](#us-anki-10) | Cấu hình và tối ưu FSRS | FR-LRN-FSRS-001 | P1 (BA proposed) | TBD | AC-ANKI-032, AC-ANKI-033, AC-ANKI-034, AC-ANKI-035 | Draft |
| [US-ANKI-11](#us-anki-11) | Bury, suspend và xử lý leech | FR-LRN-HIDE-001 | P0 (BA proposed) | TBD | AC-ANKI-036, AC-ANKI-037, AC-ANKI-038, AC-ANKI-039, AC-ANKI-040 | Draft |
| [US-ANKI-12](#us-anki-12) | Học tập mục tiêu qua filtered deck | FR-LRN-FILT-001 | P1 (BA proposed) | TBD | AC-ANKI-041, AC-ANKI-042, AC-ANKI-043, AC-ANKI-044, AC-ANKI-045 | Draft |
| [US-ANKI-13](#us-anki-13) | Nhập dữ liệu text | FR-DAT-TEXT-001 | P0 (BA proposed) | TBD | AC-ANKI-046, AC-ANKI-047, AC-ANKI-048, AC-ANKI-049, AC-ANKI-050 | Draft |
| [US-ANKI-14](#us-anki-14) | Trao đổi deck/collection package | FR-DAT-PKG-001 | P0 (BA proposed) | TBD | AC-ANKI-051, AC-ANKI-052, AC-ANKI-053, AC-ANKI-054, AC-ANKI-055 | Draft |
| [US-ANKI-15](#us-anki-15) | Đồng bộ collection | FR-DAT-SYNC-001 | P0 (BA proposed) | TBD | AC-ANKI-056, AC-ANKI-057, AC-ANKI-058, AC-ANKI-059 | Draft |
| [US-ANKI-16](#us-anki-16) | Sao lưu và phục hồi | FR-DAT-BACK-001 | P0 (BA proposed) | TBD | AC-ANKI-060, AC-ANKI-061, AC-ANKI-062, AC-ANKI-063 | Draft |
| [US-ANKI-17](#us-anki-17) | Xem lịch sử và thống kê học | FR-RPT-STAT-001 | P1 (BA proposed) | TBD | AC-ANKI-064, AC-ANKI-065, AC-ANKI-066, AC-ANKI-067 | Draft |
| [US-ANKI-18](#us-anki-18) | Quản lý add-on và mở rộng hooks/filters | FR-EXT-ADD-001 | P2 (BA proposed) | TBD | AC-ANKI-068, AC-ANKI-069, AC-ANKI-070, AC-ANKI-081, AC-ANKI-082, AC-ANKI-083, AC-ANKI-084, AC-ANKI-085, AC-ANKI-086 | Draft |
| [US-ANKI-19](#us-anki-19) | Quản lý profile cục bộ | FR-SYS-PROF-001 | P1 (BA proposed) | TBD | AC-ANKI-071, AC-ANKI-072, AC-ANKI-073 | Draft |
| [US-ANKI-20](#us-anki-20) | Quản lý và kiểm tra media | FR-DAT-MEDI-001 | P0 (BA proposed) | TBD | AC-ANKI-074, AC-ANKI-075, AC-ANKI-076, AC-ANKI-077 | Draft |

## Chi tiết và kiểm định INVEST

INVEST là đánh giá sơ bộ của BA, chưa là tiêu chí nhận vào sprint. Một FR rộng vẫn cần refinement trước khi có thể cam kết một sprint. Tách story phải giữ truy vết và không làm mất nhánh nghiệp vụ.

<a id="us-anki-01"></a>
### US-ANKI-01 — Soạn và sửa note

Là một **người soạn thẻ**, tôi muốn **soạn và sửa note** để **cập nhật kiến thức mà giữ lịch học của card hiện có**.

- Nguồn: FR-CNT-NOTE-001; BR: BR-ANKI-001, BR-ANKI-003; ERR: ERR-ANKI-000-01. [rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95).
- Đầu vào / tiền điều kiện nghiệp vụ: NoteType, field values, tags, deck đích. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Kiểm tra số field, chuẩn hóa và lưu note; sinh card phù hợp, giữ lịch của card hiện có → Note và card có thể học; lỗi khi cấu trúc không hợp lệ.
- AC: AC-ANKI-001, AC-ANKI-002, AC-ANKI-003, AC-ANKI-004; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: —. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-01 |
|---|---|
| Independent | Có thể chuẩn bị fixture riêng; vẫn cần hợp đồng NoteType/card của collection, không mặc định độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Cập nhật kiến thức mà giữ lịch học của card hiện có. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 4 AC; 4 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-02"></a>
### US-ANKI-02 — Quản lý NoteType, field và template

Là một **người soạn thẻ**, tôi muốn **quản lý notetype, field và template** để **tái sử dụng một cấu trúc nội dung và cách hỏi nhất quán**.

- Nguồn: FR-CNT-TYPE-001; BR: BR-ANKI-002, BR-ANKI-003; ERR: ERR-ANKI-000-02. [rslib/src/notetype/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/mod.rs#L484); [proto/anki/notetypes.proto:102](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/notetypes.proto#L102).
- Đầu vào / tiền điều kiện nghiệp vụ: Tên, field definitions, question/answer templates. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Validate cấu trúc tối thiểu; chuẩn hóa tên và cập nhật template khi đổi field → NoteType cập nhật trong collection; card sinh theo cấu hình.
- AC: AC-ANKI-005, AC-ANKI-006, AC-ANKI-007; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-01. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-02 |
|---|---|
| Independent | Partial: cần capability US-ANKI-01; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Tái sử dụng một cấu trúc nội dung và cách hỏi nhất quán. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 3 AC; 3 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-03"></a>
### US-ANKI-03 — Tạo thẻ cloze

Là một **người học**, tôi muốn **tạo thẻ cloze** để **tự kiểm tra từng phần kiến thức trong cùng ngữ cảnh**.

- Nguồn: FR-CNT-CLOZ-001; BR: BR-ANKI-001, BR-ANKI-004; ERR: ERR-ANKI-000-01. [rslib/src/notetype/cardgen.rs:160](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L160); [docs-site/manual/editing.mdx:364](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L364).
- Đầu vào / tiền điều kiện nghiệp vụ: Note chứa c1/c2… và cloze NoteType. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Trích số cloze, dùng template cloze, tạo ordinal còn thiếu → Card tương ứng từng số cloze, nhiều đoạn cùng số che cùng lượt.
- AC: AC-ANKI-008, AC-ANKI-009, AC-ANKI-010; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-01, US-ANKI-02. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-03 |
|---|---|
| Independent | Partial: cần capability US-ANKI-01, US-ANKI-02; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Tự kiểm tra từng phần kiến thức trong cùng ngữ cảnh. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 3 AC; 3 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-04"></a>
### US-ANKI-04 — Tạo image occlusion

Là một **người học**, tôi muốn **tạo image occlusion** để **ghi nhớ vị trí và nội dung trên hình ảnh**.

- Nguồn: FR-CNT-IMGO-001; BR: BR-ANKI-003, BR-ANKI-005; ERR: —. [rslib/src/image_occlusion/notetype.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/image_occlusion/notetype.rs#L59); [docs-site/manual/editing.mdx:504](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L504).
- Đầu vào / tiền điều kiện nghiệp vụ: Ảnh, shapes/groups, header/back extra. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Lưu cấu trúc occlusion kiểu cloze; tạo card theo shape/group; overlay chỉ hiển thị → Note ảnh với card che vùng; xóa shape cần kiểm tra Empty Cards.
- AC: AC-ANKI-011, AC-ANKI-012, AC-ANKI-013; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-01, US-ANKI-02. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-04 |
|---|---|
| Independent | Partial: cần capability US-ANKI-01, US-ANKI-02; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Ghi nhớ vị trí và nội dung trên hình ảnh. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 3 AC; 3 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-05"></a>
### US-ANKI-05 — Tổ chức deck và subdeck

Là một **người học**, tôi muốn **tổ chức deck và subdeck** để **chọn đúng phạm vi học mà vẫn quản lý card theo deck**.

- Nguồn: FR-ORG-DECK-001; BR: BR-ANKI-006, BR-ANKI-012; ERR: —. [docs-site/manual/getting-started.mdx:75](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/getting-started.mdx#L75); [rslib/src/scheduler/queue/builder/mod.rs:135](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/mod.rs#L135).
- Đầu vào / tiền điều kiện nghiệp vụ: Deck, tên phân cấp, card cần chuyển, preset. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Tổ chức card theo deck; học deck gồm descendants; card siblings có thể khác deck → Cây deck và phạm vi học xác định.
- AC: AC-ANKI-014, AC-ANKI-015, AC-ANKI-016; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-01. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-05 |
|---|---|
| Independent | Partial: cần capability US-ANKI-01; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Chọn đúng phạm vi học mà vẫn quản lý card theo deck. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 3 AC; 3 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-06"></a>
### US-ANKI-06 — Tìm kiếm và quản lý tags/flags

Là một **người học**, tôi muốn **tìm kiếm và quản lý tags/flags** để **tìm và phân loại đúng tập note/card trước khi học hoặc chỉnh sửa**.

- Nguồn: FR-ORG-SRCH-001; BR: BR-ANKI-007; ERR: —. [docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226).
- Đầu vào / tiền điều kiện nghiệp vụ: Chuỗi search field/tag/flag/deck/state và toán tử; tập note/card được chọn; thao tác thêm, gỡ, đổi tên hoặc tổ chức tag; flag được chọn. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Áp cú pháp search chung Browse/filtered; tìm văn bản trong field, không mặc định tags. Thêm/gỡ tag trên notes được chọn, đổi tên/tổ chức tags theo Browser; tag ở note nên siblings cùng nhận. Đặt/gỡ flag trên cards được chọn, mỗi card tối đa một flag, không thay flag siblings khác → Tập note/card khớp; tags hoặc flags cập nhật đúng cấp và phạm vi lựa chọn; truy vấn đơn thuần không sửa dữ liệu.
- AC: AC-ANKI-017, AC-ANKI-018, AC-ANKI-019, AC-ANKI-078, AC-ANKI-079, AC-ANKI-080; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-01, US-ANKI-05. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-06 |
|---|---|
| Independent | Partial: cần capability US-ANKI-01, US-ANKI-05; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Tìm và phân loại đúng tập note/card trước khi học hoặc chỉnh sửa. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 6 AC; 6 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-07"></a>
### US-ANKI-07 — Học và tự đánh giá card

Là một **người học**, tôi muốn **học và tự đánh giá card** để **phản hồi trí nhớ và tiếp tục phiên học đúng lịch**.

- Nguồn: FR-LRN-REV-001; BR: BR-ANKI-006, BR-ANKI-008, BR-ANKI-011; ERR: ERR-ANKI-000-03. [docs-site/manual/studying.mdx:40](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L40); [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315).
- Đầu vào / tiền điều kiện nghiệp vụ: Deck, card được chọn, rating, thời gian. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Hiện hỏi rồi đáp án; nhận tự chấm; commit AnswerCard sau kiểm tra state; lặp theo queue → Card cập nhật, revlog, thống kê và card tiếp hoặc thông tin hết phiên.
- AC: AC-ANKI-020, AC-ANKI-021, AC-ANKI-022, AC-ANKI-023; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-01, US-ANKI-05, US-ANKI-08, US-ANKI-09. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-07 |
|---|---|
| Independent | Partial: cần capability US-ANKI-01, US-ANKI-05, US-ANKI-08, US-ANKI-09; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Phản hồi trí nhớ và tiếp tục phiên học đúng lịch. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 4 AC; 4 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-08"></a>
### US-ANKI-08 — Chuyển trạng thái và xếp lịch

Là một **người học**, tôi muốn **chuyển trạng thái và xếp lịch** để **có lần ôn tiếp theo phù hợp trạng thái và phản hồi**.

- Nguồn: FR-LRN-SCH-001; BR: BR-ANKI-009, BR-ANKI-010, BR-ANKI-011, BR-ANKI-013; ERR: ERR-ANKI-000-03. [proto/anki/scheduler.proto:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L80); [rslib/src/scheduler/states/review.rs:64](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L64).
- Đầu vào / tiền điều kiện nghiệp vụ: Current state, rating, steps và cấu hình thuật toán. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Tính bốn next states; áp learning/relearning/review, interval có fuzz và giới hạn → Due/state mới; lapse khi thất bại Review.
- AC: AC-ANKI-024, AC-ANKI-025, AC-ANKI-026, AC-ANKI-027; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-01, US-ANKI-02. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-08 |
|---|---|
| Independent | Partial: cần capability US-ANKI-01, US-ANKI-02; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Có lần ôn tiếp theo phù hợp trạng thái và phản hồi. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 4 AC; 4 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-09"></a>
### US-ANKI-09 — Giới hạn khối lượng học

Là một **người học**, tôi muốn **giới hạn khối lượng học** để **kiểm soát tải học hàng ngày**.

- Nguồn: FR-LRN-LIM-001; BR: BR-ANKI-006, BR-ANKI-012; ERR: —. [rslib/src/decks/limits.rs:98](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/decks/limits.rs#L98); [rslib/src/scheduler/queue/builder/gathering.rs:23](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/gathering.rs#L23).
- Đầu vào / tiền điều kiện nghiệp vụ: Preset, override deck/today, counts, cờ limits. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Tính giới hạn còn lại và cây deck; gom learning/new/review theo điều kiện → Queue và counts bị giới hạn; intraday vẫn có thể tiếp tục.
- AC: AC-ANKI-028, AC-ANKI-029, AC-ANKI-030, AC-ANKI-031; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-05, US-ANKI-08. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-09 |
|---|---|
| Independent | Partial: cần capability US-ANKI-05, US-ANKI-08; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Kiểm soát tải học hàng ngày. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 4 AC; 4 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-10"></a>
### US-ANKI-10 — Cấu hình và tối ưu FSRS

Là một **người học nâng cao**, tôi muốn **cấu hình và tối ưu fsrs** để **điều chỉnh mô hình lịch học theo lịch sử cá nhân**.

- Nguồn: FR-LRN-FSRS-001; BR: BR-ANKI-013, BR-ANKI-014; ERR: —. [rslib/src/scheduler/answering/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L484); [docs-site/manual/deck-options.mdx:406](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L406); [docs-site/manual/deck-options.mdx:500](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L500).
- Đầu vào / tiền điều kiện nghiệp vụ: Cờ FSRS, desired retention, params, review history, reschedule choice. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Bật toàn cục; tối ưu từ history theo scope; 0 training item trả nguyên params/count0/health absent; UI current preset báo không có reviews; reschedule theo lựa chọn → Tham số và lịch theo nhánh; zero-item không tạo tham số cá nhân hóa mới; không cam kết đạt retention thực tế.
- AC: AC-ANKI-032, AC-ANKI-033, AC-ANKI-034, AC-ANKI-035; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-08. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Oracle AC-ANKI-035 đã chốt từ source ngày 2026-11-03; fixture/giới hạn ở AC và TC. Thực thi Not Run.

| INVEST | Nhận định cho US-ANKI-10 |
|---|---|
| Independent | Partial: cần capability US-ANKI-08; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Điều chỉnh mô hình lịch học theo lịch sử cá nhân. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 4 AC; 4 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-11"></a>
### US-ANKI-11 — Bury, suspend và xử lý leech

Là một **người học**, tôi muốn **bury, suspend và xử lý leech** để **tạm loại card hoặc xử lý card khó mà không nhầm trạng thái**.

- Nguồn: FR-LRN-HIDE-001; BR: BR-ANKI-015, BR-ANKI-016; ERR: —. [rslib/src/scheduler/bury_and_suspend.rs:32](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L32); [rslib/src/scheduler/answering/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L194).
- Đầu vào / tiền điều kiện nghiệp vụ: Card/note IDs, mode, sibling options, leech threshold/action. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Ẩn theo mode; unbury qua rollover/manual; phát leech và tag note/suspend card theo cấu hình → Card được loại/phục hồi queue; trạng thái trí nhớ nền bảo toàn.
- AC: AC-ANKI-036, AC-ANKI-037, AC-ANKI-038, AC-ANKI-039, AC-ANKI-040; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-07, US-ANKI-08. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-11 |
|---|---|
| Independent | Partial: cần capability US-ANKI-07, US-ANKI-08; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Tạm loại card hoặc xử lý card khó mà không nhầm trạng thái. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 5 AC; 5 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-12"></a>
### US-ANKI-12 — Học tập mục tiêu qua filtered deck

Là một **người học**, tôi muốn **học tập mục tiêu qua filtered deck** để **ôn một tập mục tiêu với lựa chọn có hoặc không đổi lịch**.

- Nguồn: FR-LRN-FILT-001; BR: BR-ANKI-017, BR-ANKI-018, BR-ANKI-019; ERR: ERR-ANKI-000-04. [rslib/src/scheduler/filtered/mod.rs:123](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L123); [rslib/src/scheduler/states/preview_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/preview_filter.rs#L25).
- Đầu vào / tiền điều kiện nghiệp vụ: Search/order/limit, reschedule flag, preview delays. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Build tập hợp lệ; dùng home deck hoặc preview; Empty/Rebuild phục hồi rồi xây lại → Deck tạm, card học và trả home; lịch đổi chỉ theo chế độ.
- AC: AC-ANKI-041, AC-ANKI-042, AC-ANKI-043, AC-ANKI-044, AC-ANKI-045; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-05, US-ANKI-06, US-ANKI-08. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-12 |
|---|---|
| Independent | Partial: cần capability US-ANKI-05, US-ANKI-06, US-ANKI-08; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Ôn một tập mục tiêu với lựa chọn có hoặc không đổi lịch. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 5 AC; 5 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-13"></a>
### US-ANKI-13 — Nhập dữ liệu text

Là một **người quản lý nội dung**, tôi muốn **nhập dữ liệu text** để **cập nhật hàng loạt nội dung mà hiểu cách xử lý trùng**.

- Nguồn: FR-DAT-TEXT-001; BR: BR-ANKI-001, BR-ANKI-020; ERR: ERR-ANKI-000-05, ERR-ANKI-000-06, ERR-ANKI-000-07. [rslib/src/import_export/text/import.rs:250](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L250); [rslib/src/import_export/text/import.rs:318](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L318).
- Đầu vào / tiền điều kiện nghiệp vụ: UTF-8 file, delimiter/mapping, GUID hoặc first field, duplicate policy. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Đọc hàng; resolve type/deck; đối chiếu GUID/first field; thêm, giữ, cập nhật hoặc báo lỗi hàng → Notes/cards nhập, kết quả added/updated/conflict/error; card cũ giữ lịch khi update.
- AC: AC-ANKI-046, AC-ANKI-047, AC-ANKI-048, AC-ANKI-049, AC-ANKI-050; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-01, US-ANKI-02, US-ANKI-05. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-13 |
|---|---|
| Independent | Partial: cần capability US-ANKI-01, US-ANKI-02, US-ANKI-05; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Cập nhật hàng loạt nội dung mà hiểu cách xử lý trùng. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 5 AC; 5 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-14"></a>
### US-ANKI-14 — Trao đổi deck/collection package

Là một **người chia sẻ/quản lý dữ liệu**, tôi muốn **trao đổi deck/collection package** để **trao đổi và khôi phục dữ liệu đúng phạm vi gói**.

- Nguồn: FR-DAT-PKG-001; BR: BR-ANKI-021, BR-ANKI-022; ERR: ERR-ANKI-000-08. [rslib/src/import_export/package/apkg/import/notes.rs:333](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L333); [rslib/src/import_export/package/apkg/import/cards.rs:99](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/cards.rs#L99); [rslib/src/import_export/package/colpkg/import.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/colpkg/import.rs#L31).
- Đầu vào / tiền điều kiện nghiệp vụ: apkg/colpkg, update/merge policy, scheduling/media options. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: apkg merge note GUID và thêm card thiếu; colpkg thay collection; export chọn phạm vi và media → Package hoặc collection cập nhật; khác biệt lịch/media theo loại gói.
- AC: AC-ANKI-051, AC-ANKI-052, AC-ANKI-053, AC-ANKI-054, AC-ANKI-055; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-01, US-ANKI-02. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-14 |
|---|---|
| Independent | Partial: cần capability US-ANKI-01, US-ANKI-02; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Trao đổi và khôi phục dữ liệu đúng phạm vi gói. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 5 AC; 5 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-15"></a>
### US-ANKI-15 — Đồng bộ collection

Là một **người học trên nhiều thiết bị**, tôi muốn **đồng bộ collection** để **tiếp tục học trên bản collection được đồng bộ**.

- Nguồn: FR-DAT-SYNC-001; BR: BR-ANKI-023, BR-ANKI-028; ERR: —. [rslib/src/sync/collection/chunks.rs:162](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/chunks.rs#L162); [rslib/src/sync/collection/meta.rs:65](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L65).
- Đầu vào / tiền điều kiện nghiệp vụ: Local/remote changes, metadata/schema, tài khoản/endpoint, lựa chọn full sync. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Merge record theo mtime/pending; nhập revlog; full upload/download khi cần; media riêng → Collection đồng bộ theo nhánh; không hòa giải từng field.
- AC: AC-ANKI-056, AC-ANKI-057, AC-ANKI-058, AC-ANKI-059; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-01, US-ANKI-14, US-ANKI-19, US-ANKI-20. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-15 |
|---|---|
| Independent | Partial: cần capability US-ANKI-01, US-ANKI-14, US-ANKI-19, US-ANKI-20; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Tiếp tục học trên bản collection được đồng bộ. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 4 AC; 4 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-16"></a>
### US-ANKI-16 — Sao lưu và phục hồi

Là một **người quản lý dữ liệu học**, tôi muốn **sao lưu và phục hồi** để **quay về snapshot có phạm vi khôi phục rõ ràng**.

- Nguồn: FR-DAT-BACK-001; BR: BR-ANKI-022, BR-ANKI-024; ERR: —. [rslib/src/collection/backup.rs:28](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/collection/backup.rs#L28); [docs-site/manual/backups.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L7); [docs-site/manual/backups.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L24).
- Đầu vào / tiền điều kiện nghiệp vụ: Collection thay đổi, lịch backup hoặc snapshot chọn restore. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Tạo backup khi đủ điều kiện; restore thay dữ liệu; xuất colpkg media cho backup đầy đủ → Snapshot/collection phục hồi; mất thay đổi sau snapshot; auto backup không media.
- AC: AC-ANKI-060, AC-ANKI-061, AC-ANKI-062, AC-ANKI-063; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-14, US-ANKI-19, US-ANKI-20. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-16 |
|---|---|
| Independent | Partial: cần capability US-ANKI-14, US-ANKI-19, US-ANKI-20; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Quay về snapshot có phạm vi khôi phục rõ ràng. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 4 AC; 4 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-17"></a>
### US-ANKI-17 — Xem lịch sử và thống kê học

Là một **người học**, tôi muốn **xem lịch sử và thống kê học** để **hiểu khối lượng và kết quả học theo định nghĩa chỉ số**.

- Nguồn: FR-RPT-STAT-001; BR: BR-ANKI-025; ERR: —. [rslib/src/stats/graphs/today.rs:17](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/today.rs#L17); [rslib/src/stats/graphs/retention.rs:53](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L53).
- Đầu vào / tiền điều kiện nghiệp vụ: Review logs, card states, phạm vi deck/search và thời gian. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Tổng hợp Today, đúng/sai, mature, retention và lịch tới hạn theo định nghĩa từng chỉ số → True retention As-Is cộng từng revlog đủ điều kiện trong cửa sổ scheduler; cùng card/ngày có thể đóng góp nhiều lượt; discrepancy manual được ghi nhận.
- AC: AC-ANKI-064, AC-ANKI-065, AC-ANKI-066, AC-ANKI-067; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-07, US-ANKI-08. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Oracle AC-ANKI-067 đã chốt từ source ngày 2026-11-03; fixture/giới hạn ở AC và TC. Thực thi Not Run.

| INVEST | Nhận định cho US-ANKI-17 |
|---|---|
| Independent | Partial: cần capability US-ANKI-07, US-ANKI-08; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Hiểu khối lượng và kết quả học theo định nghĩa chỉ số. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 4 AC; 4 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-18"></a>
### US-ANKI-18 — Quản lý add-on và mở rộng hooks/filters

Là một **tác giả add-on**, tôi muốn **quản lý add-on và mở rộng hooks/filters** để **quản lý extension và mở rộng đúng lifecycle được ứng dụng cung cấp**.

- Nguồn: FR-EXT-ADD-001; BR: BR-ANKI-026, BR-ANKI-027; ERR: —. [docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29).
- Đầu vào / tiền điều kiện nghiệp vụ: Addon IDs hoặc package, danh sách addon chọn, yêu cầu tải/cài từ file/kiểm tra cập nhật/bật/tắt/xóa; callback hooks/filters và sự kiện ứng dụng. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Tools Add-ons tải/cài package và kiểm tra cập nhật; bật/tắt ghi metadata, xử lý addon xung đột khi bật; xóa yêu cầu xác nhận. Ghi yêu cầu restart khi toggle hoặc xóa addon đang bật. Khi addon được nạp, gọi hooks/filters theo lifecycle đã định nghĩa; addon dùng chung profile → Danh sách, metadata và trạng thái addon cập nhật theo kết quả; thông tin tải/cài/cập nhật/lỗi và restart khi được yêu cầu; callback chỉ tác động đúng lifecycle, không mặc nhiên mọi đường nhập.
- AC: AC-ANKI-068, AC-ANKI-069, AC-ANKI-070, AC-ANKI-081, AC-ANKI-082, AC-ANKI-083, AC-ANKI-084, AC-ANKI-085, AC-ANKI-086; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-01, US-ANKI-07, US-ANKI-19. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Điểm cần chốt: review AC, môi trường/harness và estimate của đội kỹ thuật.

| INVEST | Nhận định cho US-ANKI-18 |
|---|---|
| Independent | Partial: cần capability US-ANKI-01, US-ANKI-07, US-ANKI-19; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Quản lý extension và mở rộng đúng lifecycle được ứng dụng cung cấp. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 9 AC; 9 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-19"></a>
### US-ANKI-19 — Quản lý profile cục bộ

Là một **người dùng desktop**, tôi muốn **quản lý profile cục bộ** để **tách collection và thiết lập giữa các không gian học**.

- Nguồn: FR-SYS-PROF-001; BR: BR-ANKI-027; ERR: —. [docs-site/manual/profiles.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/profiles.mdx#L5).
- Đầu vào / tiền điều kiện nghiệp vụ: Profile được tạo/chọn và tài khoản sync tương ứng. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Mở collection/settings/auth theo profile; addon dùng chung. Cùng account không được caller khảo sát bảo vệ bằng uniqueness; trên server test cùng user dùng chung remote collection, sync theo mod/schema và hướng được chọn → Local paths riêng; Cancel/full Download/full Upload có kết quả dữ liệu riêng theo fixture; không phải tenant/RBAC.
- AC: AC-ANKI-071, AC-ANKI-072, AC-ANKI-073; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-01. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Oracle AC-ANKI-072 đã chốt từ source ngày 2026-11-03; fixture/giới hạn ở AC và TC. Thực thi Not Run.

| INVEST | Nhận định cho US-ANKI-19 |
|---|---|
| Independent | Partial: cần capability US-ANKI-01; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Tách collection và thiết lập giữa các không gian học. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 3 AC; 3 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

<a id="us-anki-20"></a>
### US-ANKI-20 — Quản lý và kiểm tra media

Là một **người quản lý nội dung**, tôi muốn **quản lý và kiểm tra media** để **phát hiện asset thiếu hoặc không dùng và hiểu phạm vi sync**.

- Nguồn: FR-DAT-MEDI-001; BR: BR-ANKI-028; ERR: —. [docs-site/manual/media.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/media.mdx#L24); [docs-site/manual/syncing.mdx:54](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/syncing.mdx#L54).
- Đầu vào / tiền điều kiện nghiệp vụ: Tham chiếu media, collection.media, trạng thái sync. Collection/profile và dữ liệu fixture được cô lập; nguồn không định nghĩa thêm quyền giáo viên/admin.
- Luồng giá trị: Check thiếu/không dùng; sync media fetch remote trước upload pending, xử lý checksum/dirty/cursor; static template media dùng _ → Danh sách vấn đề và dữ liệu media theo nhánh; cùng filename chuẩn/khác hash có oracle xác định khi cố định cursor, dirty và thứ tự sync.
- AC: AC-ANKI-074, AC-ANKI-075, AC-ANKI-076, AC-ANKI-077; chi tiết tại [AC v1.0.1](acceptance-criteria.md), test/RTM tại [QA v1.0.1](../test/test-cases.md).
- Phụ thuộc kiểm thử/nghiệp vụ: US-ANKI-01. Đây là phụ thuộc capability có sẵn trong As-Is, không suy diễn thứ tự triển khai mới.
- Ngoài scope: thay đổi quy tắc upstream, chính sách mới, chứng minh mobile/AnkiWeb production và xác nhận runtime. Với ERR chưa có danh mục, không suy ra chức năng không thể lỗi.
- Oracle AC-ANKI-077 đã chốt từ source ngày 2026-11-03; fixture/giới hạn ở AC và TC. Thực thi Not Run.

| INVEST | Nhận định cho US-ANKI-20 |
|---|---|
| Independent | Partial: cần capability US-ANKI-01; có thể kiểm bằng snapshot fixture độc lập, chưa độc lập release. |
| Negotiable | Cách trình bày và chia nhỏ có thể refinement; thay hành vi As-Is cần quyết định/CR có nguồn. |
| Valuable | Phát hiện asset thiếu hoặc không dùng và hiểu phạm vi sync. |
| Estimable | TBD; dev xác nhận sau review phụ thuộc, fixture và nguồn. |
| Small | Chưa xác nhận vừa một sprint; scope một FR, cần chia nhỏ nếu ước lượng vượt khả năng đội. |
| Testable | 4 AC; 4 có oracle mô tả; 0 blocked. Tất cả test Not Run. |

## Bàn giao và tiêu chí hoàn tất

AC phải được stakeholder/QA review; blocker phải được chốt bằng nguồn hoặc quyết định ghi nhận; test cần môi trường, version, evidence thực thi và actual result. ID coverage không chứng minh Done. Giữ mọi story Draft cho tới khi có bằng chứng review/approval, không dùng yêu cầu tạo tài liệu làm approval hành vi. Ưu tiên và points chỉ chốt bởi owner/team.

## Câu hỏi còn mở

Bốn oracle đã chốt cho As-Is trong fixture cụ thể; owner QA chuẩn bị/chạy harness trước kết luận Pass/Fail. Owner thống kê/sản phẩm còn quyết định xử lý discrepancy manual/code retention. Owner sản phẩm/kỹ thuật xác nhận scope, điểm, ưu tiên và NFR; chưa có approval.

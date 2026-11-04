---
id: DOC-CODE-ANKI-001
title: "Ma trận nguồn tái lập SRS Anki"
version: "1.0.1"
phase: Specification
domain: Anki
tags: [anki, as-is, reconstructed, srs]
depends_on: [DOC-SRS-ANKI-001]
related_diagrams: []
author: BA Agent
last_updated: "2026-11-03"
status: draft
---

# Ma trận code → SRS Anki

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---|---|---|---|
| 1.0.1 | 2026-11-03 | BA Analysis | Làm rõ oracle035/067/072/077 và truy vết liên quan; không thay source hoặc kết quả chạy |
| 1.0.0 | 2026-11-02 | BA Agent | Đối chiếu 20 FR với nguồn và nhãn báo cáo cũ, ghi giới hạn nghiên cứu. |

## 1. Tổng quan

[DOC-SRS-ANKI-001 v1.0.1](spec.md) là mô tả As-Is draft. Commit 136bd42bfbd356fc756b6d3e28cc77b02da11ea7, Anki desktop. Phương pháp: tái sử dụng hai báo cáo phân tích source/manual đã có, đọc trực tiếp các điểm validation, state transition, queue, filtered, stats; không khẳng định đọc toàn bộ repository. Không build/run/test. Code = implementation/proto; Doc = manual; suy luận BA = lựa chọn ranh giới/ưu tiên/diễn giải, không phải phê duyệt.

## 2. Ma trận nguồn chức năng

| FR | BR | ERR | Chứng cứ | Path/dòng cố định |
|---|---|---|---|---|
| FR-CNT-NOTE-001 — Soạn và sửa note | BR-ANKI-001, BR-ANKI-003 | ERR-ANKI-000-01 | Code | [rslib/src/notes/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notes/mod.rs#L194); [rslib/src/notetype/cardgen.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L95) |
| FR-CNT-TYPE-001 — Quản lý NoteType, field và template | BR-ANKI-002, BR-ANKI-003 | ERR-ANKI-000-02 | Code | [rslib/src/notetype/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/mod.rs#L484); [proto/anki/notetypes.proto:102](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/notetypes.proto#L102) |
| FR-CNT-CLOZ-001 — Tạo thẻ cloze | BR-ANKI-001, BR-ANKI-004 | ERR-ANKI-000-01 | Code + Doc | [rslib/src/notetype/cardgen.rs:160](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/notetype/cardgen.rs#L160); [docs-site/manual/editing.mdx:364](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L364) |
| FR-CNT-IMGO-001 — Tạo image occlusion | BR-ANKI-003, BR-ANKI-005 | Chưa lập | Code + Doc | [rslib/src/image_occlusion/notetype.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/image_occlusion/notetype.rs#L59); [docs-site/manual/editing.mdx:504](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L504) |
| FR-ORG-DECK-001 — Tổ chức deck và subdeck | BR-ANKI-006, BR-ANKI-012 | Chưa lập | Code + Doc | [docs-site/manual/getting-started.mdx:75](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/getting-started.mdx#L75); [rslib/src/scheduler/queue/builder/mod.rs:135](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/mod.rs#L135) |
| FR-ORG-SRCH-001 — Tìm kiếm và quản lý tags/flags | BR-ANKI-007 | Chưa lập | Doc; implementation/runtime chưa xác minh | [docs-site/manual/searching.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/searching.mdx#L5); [docs-site/manual/browsing.mdx:216](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L216); [docs-site/manual/browsing.mdx:240](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/browsing.mdx#L240); [docs-site/manual/editing.mdx:226](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx#L226) |
| FR-LRN-REV-001 — Học và tự đánh giá card | BR-ANKI-006, BR-ANKI-008, BR-ANKI-011 | ERR-ANKI-000-03 | Code + Doc | [docs-site/manual/studying.mdx:40](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx#L40); [rslib/src/scheduler/answering/mod.rs:315](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L315) |
| FR-LRN-SCH-001 — Chuyển trạng thái và xếp lịch | BR-ANKI-009, BR-ANKI-010, BR-ANKI-011, BR-ANKI-013 | ERR-ANKI-000-03 | Code | [proto/anki/scheduler.proto:80](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L80); [rslib/src/scheduler/states/review.rs:64](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/review.rs#L64) |
| FR-LRN-LIM-001 — Giới hạn khối lượng học | BR-ANKI-006, BR-ANKI-012 | Chưa lập | Code | [rslib/src/decks/limits.rs:98](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/decks/limits.rs#L98); [rslib/src/scheduler/queue/builder/gathering.rs:23](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/queue/builder/gathering.rs#L23) |
| FR-LRN-FSRS-001 — Cấu hình và tối ưu FSRS | BR-ANKI-013, BR-ANKI-014 | Chưa lập | Code + Doc; source review 2026-11-03, runtime Not Run | [rslib/src/scheduler/answering/mod.rs:484](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L484); [docs-site/manual/deck-options.mdx:406](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L406); [docs-site/manual/deck-options.mdx:500](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/deck-options.mdx#L500); [ts/routes/deck-options/FsrsOptions.svelte:200](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L200); [ts/routes/deck-options/FsrsOptions.svelte:225](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L225); [ts/routes/deck-options/FsrsOptions.svelte:235](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/deck-options/FsrsOptions.svelte#L235); [rslib/src/scheduler/service/mod.rs:264](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/service/mod.rs#L264); [rslib/src/scheduler/fsrs/params.rs:95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/fsrs/params.rs#L95); [proto/anki/scheduler.proto:357](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/proto/anki/scheduler.proto#L357); [ftl/core/deck-config.ftl:495](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ftl/core/deck-config.ftl#L495) |
| FR-LRN-HIDE-001 — Bury, suspend và xử lý leech | BR-ANKI-015, BR-ANKI-016 | Chưa lập | Code | [rslib/src/scheduler/bury_and_suspend.rs:32](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/bury_and_suspend.rs#L32); [rslib/src/scheduler/answering/mod.rs:194](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/answering/mod.rs#L194) |
| FR-LRN-FILT-001 — Học tập mục tiêu qua filtered deck | BR-ANKI-017, BR-ANKI-018, BR-ANKI-019 | ERR-ANKI-000-04 | Code | [rslib/src/scheduler/filtered/mod.rs:123](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/filtered/mod.rs#L123); [rslib/src/scheduler/states/preview_filter.rs:25](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/scheduler/states/preview_filter.rs#L25) |
| FR-DAT-TEXT-001 — Nhập dữ liệu text | BR-ANKI-001, BR-ANKI-020 | ERR-ANKI-000-05, ERR-ANKI-000-06, ERR-ANKI-000-07 | Code | [rslib/src/import_export/text/import.rs:250](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L250); [rslib/src/import_export/text/import.rs:318](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/text/import.rs#L318) |
| FR-DAT-PKG-001 — Trao đổi deck/collection package | BR-ANKI-021, BR-ANKI-022 | ERR-ANKI-000-08 | Code | [rslib/src/import_export/package/apkg/import/notes.rs:333](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/notes.rs#L333); [rslib/src/import_export/package/apkg/import/cards.rs:99](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/apkg/import/cards.rs#L99); [rslib/src/import_export/package/colpkg/import.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/import_export/package/colpkg/import.rs#L31) |
| FR-DAT-SYNC-001 — Đồng bộ collection | BR-ANKI-023, BR-ANKI-028 | Chưa lập | Code | [rslib/src/sync/collection/chunks.rs:162](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/chunks.rs#L162); [rslib/src/sync/collection/meta.rs:65](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L65) |
| FR-DAT-BACK-001 — Sao lưu và phục hồi | BR-ANKI-022, BR-ANKI-024 | Chưa lập | Code + Doc | [rslib/src/collection/backup.rs:28](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/collection/backup.rs#L28); [docs-site/manual/backups.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L7); [docs-site/manual/backups.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/backups.mdx#L24) |
| FR-RPT-STAT-001 — Xem lịch sử và thống kê học | BR-ANKI-025 | Chưa lập | Code + Doc; source review 2026-11-03, runtime Not Run | [rslib/src/stats/graphs/today.rs:17](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/today.rs#L17); [rslib/src/stats/graphs/retention.rs:53](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L53); [rslib/src/storage/revlog/get.sql:1](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/get.sql#L1); [rslib/src/storage/revlog/mod.rs:122](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/mod.rs#L122); [rslib/src/storage/revlog/mod.rs:175](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/storage/revlog/mod.rs#L175); [rslib/src/stats/graphs/mod.rs:31](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/mod.rs#L31); [rslib/src/stats/graphs/retention.rs:16](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/stats/graphs/retention.rs#L16); [rslib/src/revlog/mod.rs:107](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/revlog/mod.rs#L107); [ts/routes/graphs/true-retention.ts:105](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/ts/routes/graphs/true-retention.ts#L105); [docs-site/manual/stats.mdx:229](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/stats.mdx#L229) |
| FR-EXT-ADD-001 — Quản lý add-on và mở rộng hooks/filters | BR-ANKI-026, BR-ANKI-027 | Chưa lập | Code + Doc | [docs-site/manual/addons.mdx:9](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/addons.mdx#L9); [qt/aqt/addons.py:353](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L353); [qt/aqt/addons.py:446](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L446); [qt/aqt/addons.py:963](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L963); [qt/aqt/addons.py:990](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L990); [qt/aqt/addons.py:1011](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1011); [qt/aqt/addons.py:1043](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/addons.py#L1043); [docs-site/addons/hooks-and-filters.mdx:7](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/addons/hooks-and-filters.mdx#L7); [pylib/tools/genhooks.py:29](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/pylib/tools/genhooks.py#L29) |
| FR-SYS-PROF-001 — Quản lý profile cục bộ | BR-ANKI-027 | Chưa lập | Code + Doc; source review 2026-11-03, runtime Not Run | [docs-site/manual/profiles.mdx:5](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/profiles.mdx#L5); [qt/aqt/profiles.py:212](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L212); [qt/aqt/profiles.py:659](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L659); [qt/aqt/profiles.py:681](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L681); [qt/aqt/sync.py:307](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L307); [rslib/src/sync/http_server/mod.rs:122](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/http_server/mod.rs#L122); [rslib/src/sync/collection/meta.rs:59](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L59); [qt/aqt/sync.py:138](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L138); [rslib/src/sync/collection/download.rs:35](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/download.rs#L35); [rslib/src/sync/collection/upload.rs:79](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/upload.rs#L79); [rslib/src/sync/collection/tests.rs:591](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/tests.rs#L591) |
| FR-DAT-MEDI-001 — Quản lý và kiểm tra media | BR-ANKI-028 | Chưa lập | Code + Doc; source review 2026-11-03, runtime Not Run | [docs-site/manual/media.mdx:24](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/media.mdx#L24); [docs-site/manual/syncing.mdx:54](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/syncing.mdx#L54); [rslib/src/sync/media/syncer.rs:60](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/syncer.rs#L60); [rslib/src/sync/media/changes.rs:44](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/changes.rs#L44); [rslib/src/media/files.rs:403](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L403); [rslib/src/sync/media/database/client/mod.rs:206](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/client/mod.rs#L206); [rslib/src/sync/media/database/server/entry/upload.rs:35](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/server/entry/upload.rs#L35); [rslib/src/sync/media/tests.rs:278](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/tests.rs#L278); [rslib/src/backend/sync.rs:188](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/backend/sync.rs#L188); [rslib/src/sync/media/database/client/changetracker.rs:56](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/client/changetracker.rs#L56); [rslib/src/media/files.rs:165](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L165) |

## 3. Quy chuẩn chuyển đổi

- Giữ ID FR do controller cấp, không đổi chúng theo module thực thi. requirements.json là danh mục cùng version.
- BR WHEN/THEN/UNLESS ở SRS có source riêng; giới hạn chứng cứ được giữ trong UNLESS và câu hỏi mở.
- ERR là analytical label, 000 không HTTP; không chế tạo localization key. Quan sát enum/log/guard không chứng minh UI wording.
- NFR có method và trạng thái; không có số liệu benchmark/SLA giả. Chỉ có static evidence, không có test Pass.
- Source manual là primary documentation tại snapshot, không thay thế runtime verification. FR-ORG-SRCH-001 dựa chủ yếu trên Doc; profile/media đã bổ sung caller/backend/test source cho oracle072/077 trong phạm vi server test.

## 4. Ánh xạ nhãn báo cáo cũ

Không sửa nhãn trong tài liệu cũ. Mapping nhiều-nhiều cho thấy sự hợp nhất/tách quy tắc, không thay nghĩa lịch sử.

| Báo cáo học | BR SRS |
|---|---|
| BR-LEARN-001 | BR-ANKI-006, BR-ANKI-012 |
| BR-LEARN-002 | BR-ANKI-008 |
| BR-LEARN-003 | BR-ANKI-009 |
| BR-LEARN-004 | BR-ANKI-010 |
| BR-LEARN-005 | BR-ANKI-013 |
| BR-LEARN-006 | BR-ANKI-014 |
| BR-LEARN-007 | BR-ANKI-012 |
| BR-LEARN-008 | BR-ANKI-012 |
| BR-LEARN-009 | BR-ANKI-015 |
| BR-LEARN-010 | BR-ANKI-016 |
| BR-LEARN-011 | BR-ANKI-017 |
| BR-LEARN-012 | BR-ANKI-018 |
| BR-LEARN-013 | BR-ANKI-019 |
| BR-LEARN-014 | BR-ANKI-011 |
| BR-LEARN-015 | BR-ANKI-025 |

| Báo cáo nội dung (mục quy tắc đánh số) | BR SRS |
|---|---|
| 1 — Note/card/tags/deck | BR-ANKI-001, BR-ANKI-006 |
| 2 — Sinh card theo template | BR-ANKI-003 |
| 3 — Cloze và IO | BR-ANKI-004, BR-ANKI-005 |
| 4 — Text import duplicate | BR-ANKI-020 |
| 5–6 — apkg và NoteType merge | BR-ANKI-021 |
| 7 — apkg/colpkg | BR-ANKI-022 |
| 8 — Sync | BR-ANKI-023 |
| 9 — Media | BR-ANKI-028 |
| 10 — Backup | BR-ANKI-024 |
| Ranh giới profile/addon | BR-ANKI-026, BR-ANKI-027 |

Nguồn gốc: [learning-business.md](../../../plans/reports/learning-business.md), [content-business.md](../../../plans/reports/content-business.md). BR-ANKI-002/007 bổ sung từ validation NoteType và search/tag/flag manual trực tiếp. Initial draft cũng đối chiếu addon manager tại qt/aqt/addons.py để FR-EXT-ADD-001 bao phủ thao tác người dùng cùng hooks.

## 5. Ma trận kiểm tra tài liệu

| Kiểm tra | Phương pháp | Trạng thái |
|---|---|---|
| Số lượng và ID | JSON parse; đếm 20 FR, 28 BR, 8 ERR, 8 NFR, kiểm tra uniqueness | Pass kiểm tra cấu trúc, 2026-11-02 |
| Tham chiếu FR → BR/ERR | Membership trong danh mục JSON | Pass kiểm tra cấu trúc, 2026-11-02 |
| Source anchor | File tồn tại và line trong độ dài source, URL khóa commit | Pass kiểm tra anchor, 2026-11-02; không chứng minh mọi diễn giải đúng |
| Runtime behavior | Cần fixtures và app được chạy | Not Run |
| Approval | Cần nguồn người/thời điểm | Chưa có; draft |

## 6. Câu hỏi chưa giải quyết

Đã chốt oracle035/067/072/077 từ source; xem [hồ sơ bằng chứng](../governance/evidence-and-scope.md). Còn quyết định To-Be cho khác biệt retention manual/code; bury interday, package Always equal timestamp, phạm vi ensure_not_empty, runtime/NFR và người phê duyệt vẫn giữ theo SRS mục 4.3. Không coi source review là runtime Pass.


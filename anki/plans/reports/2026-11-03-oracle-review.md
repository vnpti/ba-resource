---
id: DOC-REVIEW-ORACLE-ANKI-20261103
title: Independent source review — oracle 072 và 077
version: "1.0.0"
phase: Review
domain: Anki
tags: [oracle, sync, media, independent-review]
depends_on: [DOC-SRS-ANKI-001, DOC-TC-ANKI-001]
related_diagrams: []
author: BA Agent
last_updated: "2026-11-03"
status: draft
---

# Independent review oracle 072 / 077

| Phiên bản | Ngày | Thay đổi |
|---|---|---|
| 1.0.0 | 2026-11-03 | Đối chiếu độc lập caller, guard và side effect; không chạy ứng dụng/test |

Source read-only: commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`. Không sửa SRS/QA/source. Những kết luận dưới đây là source-verified, không phải runtime Pass.

## Guard bắt buộc cho 072

- `SyncMeta::compared_to_remote` xét **modified bằng nhau trước**, trả NoChanges ngay. Chỉ khi modified khác nhau mới xét schema khác để yêu cầu FullSync. `empty` nghĩa không có card, không phải không có note/notetype/media. [meta.rs:65][META65], [meta.rs:142][META142].
- Với modified khác + schema khác: hai phía có card → upload_ok và download_ok đều true; local rỗng/remote có card → chỉ download; local có card/remote rỗng → chỉ upload. Backend map hai cờ thành FULL_SYNC/FULL_DOWNLOAD/FULL_UPLOAD. [meta.rs:69][META69], [backend/sync.rs:53][BS53]. Không được hứa mọi profile mới đều có hộp thoại ba lựa chọn.
- Call path: profile-specific hkey → `mw.col.sync_collection` → backend normal sync → FullSyncRequired trả trước transaction normal-sync → Python chooser. [profiles.py:659][PR659], [sync.py:129][QT129], [normal.rs:80][N80], [sync.py:138][QT138]. Không thấy guard kiểm account đã dùng trong profile khác ở đường này; không suy diễn server production không thể có các policy khác.
- Click Cancel ở chooser có ba nút chỉ gọi `on_done()`, không gọi `full_upload` hoặc `full_download`. Chốt oracle **không thay thế/merge collection bởi thao tác sync này**, không chốt toàn bộ profile/DB byte-identical: trước chooser UI đã có thể lưu host number/endpoint từ metadata. [sync.py:116][QT116], [sync.py:153][QT153]. Cancel ở progress khi transfer đang chạy là nhánh khác.
- Backend không bắt đầu media sync mới khi kết quả là FullSyncRequired, nhưng fixture vẫn cần không có job media đang chạy hoặc tắt media nếu muốn khẳng định media không đổi. [backend/sync.rs:384][BS384].
- Guard hạ tầng trước so metadata: server should_continue=true và chênh clock không quá300s. [status.rs:42][ST42]. Test nguồn xác nhận local empty + server nonempty không cho upload: [collection/tests.rs:606][CT606].

## Guard và side effect bắt buộc cho 077

- Sync đầu tiên register local filesystem changes, lấy client cursor và server USN. Chỉ fetch remote khi hai USN khác nhau; fetch xong mới gửi pending uploads. [syncer.rs:61][MS61]. Remote change feed dùng `usn > cursor`, không áp “server thắng” cho mọi file đang có server. [changes.sql:9][SQL9].
- Khi **remote change record của cùng filename được fetch**, hai SHA1 nonempty khác nhau → Download kể cả local pending/dirty. Tests phủ cả pending và clean. [changes.rs:44][MC44], [changes.rs:135][MC135]. Không phụ thuộc mtime của hai file trong conflict decision này.
- Download archive đi qua `add_file_from_ankiweb`. Với filename hợp lệ đã normalized (ví dụ `shared.png`), ghi đè trực tiếp cùng path; nhánh rename chỉ dành tên chưa hợp lệ/normalized. [download.rs:48][MD48], [files.rs:407][MF407].
- Sau download, record_additions lưu SHA1 mới và `sync_required=false`; transaction cập nhật cursor. File này không còn pending để bị upload lại trong cùng sync. [client/mod.rs:241][DB241], [syncer.rs:174][MS174].
- Test upstream “server (first sync) content wins” là tuần tự client1 upload bytes1 rồi client2 sync bytes2 cùng filename, cuối cùng cả hai bytes1. Đây không phải luật tổng quát cho mọi lần sửa sau hoặc mọi race. [media/tests.rs:278][MT278].
- Counterexample chặn overgeneralization: client cursor đã bằng server USN và local dirty có bytes khác → bỏ fetch, upload pending; server xử lý different SHA1 thành Replaced. [syncer.rs:74][MS74], [server/entry/upload.rs:70][SU70]. Vì vậy expected phải gắn cursor/change-feed/dirty và thứ tự sync.
- Cùng hash + pending chỉ RemovePending; remote deleted + local nonempty pending giữ local để upload sau; deletion không cùng policy với hai file nonempty. [changes.rs:49][MC49].

## Trạng thái review báo cáo đầu vào

Các guard trên được kiểm tra trước khi báo cáo tác giả sẵn sàng và đã gửi controller. Sau đó đã đọc báo cáo `plans/reports/2026-11-03-sync-media-oracles.md`; kết quả cuối ở mục “Kết quả đối chiếu báo cáo tác giả” bên dưới.

## Câu hỏi còn lại

- Runtime/test chưa chạy; mọi TC vẫn Not Run.
- Không còn câu hỏi nguồn về nhánh Cancel trước transfer và conflict remote-record nói trên. Cần đảm bảo fixture cuối giữ các guard đã liệt kê.

[META65]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L65
[META69]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L69
[META142]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L142
[BS53]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/backend/sync.rs#L53
[BS384]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/backend/sync.rs#L384
[PR659]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L659
[QT129]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L129
[QT138]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L138
[QT116]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L116
[QT153]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L153
[N80]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/normal.rs#L80
[ST42]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/status.rs#L42
[CT606]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/tests.rs#L606
[MS61]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/syncer.rs#L61
[MS74]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/syncer.rs#L74
[MS174]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/syncer.rs#L174
[SQL9]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/server/entry/changes.sql#L9
[MC44]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/changes.rs#L44
[MC49]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/changes.rs#L49
[MC135]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/changes.rs#L135
[MD48]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/download.rs#L48
[MF407]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L407
[DB241]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/client/mod.rs#L241
[MT278]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/tests.rs#L278
[SU70]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/server/entry/upload.rs#L70

## Kết quả đối chiếu báo cáo tác giả

Đã đọc đầy đủ `plans/reports/2026-11-03-sync-media-oracles.md` sau khi tác giả cung cấp. **Status: DONE — không có finding trọng yếu hoặc blocker oracle cho phạm vi fixture đã định nghĩa.**

- F072 đã giữ đúng guard mod/schema khác nhau, hai phía nonempty, auth/profile path riêng, media/auto-sync/addon tắt; phân biệt Cancel, Download, Upload và empty-local. Kết luận không có guard trùng account giới hạn ở caller được khảo sát; không tuyên bố policy hosted. Đây là phạm vi hợp lý.
- Cancel ở prompt được mô tả không merge/replace nội dung, có ngoại lệ host/url metadata; khớp code. Không lẫn với cancel khi full transfer đang chạy.
- Full Download kiểm integrity file tạm rồi atomic rename thay active local collection: [download.rs:41](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/download.rs#L41). Full Upload server kiểm integrity rồi atomic rename thay collection server: [upload.rs:79](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/upload.rs#L79). UI gọi backup trước download: [sync.py:248](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L248). Oracle snapshot thay thế thay vì field merge là đúng.
- Media M1 cursor0/server1, different nonempty SHA1/dirty, normalized filename và thứ tự sync đủ cụ thể để chốt server content overwrite local + clear dirty. M2 với cursor bằng server đi upload; M3 đã khóa thứ tự xử lý upload trên self-host nên có winner xác định. Không có tuyên bố “first sync wins” hay “last writer wins” áp vô điều kiện.
- Các nhánh normal collection merge/graves P5 là mở rộng nghiên cứu; không được xem là đã review toàn bộ chỉ từ kết luận core072 này. Controller/tác giả đang tách chúng khỏi nghiệm thu tối thiểu072 để case hữu hạn. Không thấy vấn đề cần chặn core072/077.

**Hai bổ sung citation, không phải lỗi hành vi:**

1. Ref S02 của báo cáo tác giả dẫn `profiles.py:212–239` cho load/path nhưng các claim sync key/user cần thêm [profiles.py:659](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L659) và [681](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L681).
2. Ref S07 chỉ dẫn download, cần thêm [upload.rs:79–95](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/upload.rs#L79-L95) cho phần server-upload replacement.

Đã gửi cả hai bổ sung cho tác giả và controller. Không tự sửa báo cáo tác giả. AC/TC đủ cơ sở thiết kế Specified cho fixture; status thực thi vẫn Not Run.

### Câu hỏi còn lại sau review

Không còn câu hỏi chặn oracle core072/077. Harness/runtime/hosted AnkiWeb vẫn chưa kiểm chứng và nằm ngoài kết luận source-review này.

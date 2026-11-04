# Chốt oracle AC/TC-ANKI-072 và 077

Ngày: 2026-11-03. Source: `ankitects/anki@136bd42bfbd356fc756b6d3e28cc77b02da11ea7`. Phương pháp: đọc source/manual/test; **không build, không chạy Anki/test/sync, không truy cập collection người dùng**. Chỉ báo cáo này được ghi. Các expected bên dưới là thiết kế có bằng chứng tĩnh, không phải kết quả Pass thực thi.

## Kết luận và thay đổi catalog đề xuất

Có thể chuyển **design_status** hai AC/TC từ `Blocked` sang `Specified` nếu dùng fixture và phạm vi dưới đây; giữ `status=Not Run`, `actual_result=Not Run`, approval Draft. Giữ ID072/077, phân nhánh bằng bảng ví dụ trong cùng case; không thêm ERR giả. Chưa thể chứng nhận behavior hosted AnkiWeb chỉ từ source self-host.

- **072:** cùng account không tạo một namespace collection riêng cho mỗi tên profile. Đường UI/login được khảo sát không kiểm tra account đang dùng bởi profile khác; kết quả phụ thuộc collection metadata, hướng full sync được chọn hoặc normal merge. Manual cảnh báo ghi đè là hướng dẫn tránh dùng sai, không phải bằng chứng cho một lỗi runtime luôn xảy ra. [S01][S02][S03][S04][S05][S24][S25][S26]
- **077:** khi client nhận thay đổi server cho một filename hợp lệ khác hash, nó **download rồi ghi đè đúng filename**, kể cả bản local còn dirty. Sync bình thường đọc thay đổi server trước khi upload. Hai client tạo tên trùng từ nền sạch rồi sync A xong mới B: nội dung A thắng. Upload đã tới server self-host sau đó có thể thay nội dung server; đây là nhánh khác, không suy ra quy tắc “file mtime mới nhất thắng”. [S11][S12][S13][S14][S16]
- `TC-072.mode` cần đổi thành **Switch Profile + login/callback + collection sync trên server thử nghiệm cô lập**. `TC-077.mode` cần đổi thành **Media sync backend/protocol + thư mục/media DB tạm + completion status**. Chỉ Switch Profile hoặc Check Media không thực hiện hai hành vi đang nghiệm thu. [S03][S11][S20]

## Bằng chứng và ranh giới

Các nhãn Sxx bên dưới là nguồn pinned có path/line, dùng cho cả rule và fixture suy diễn.

| Ref | Chứng cứ |
|---|---|
| [S01] | Manual profiles: collection/settings riêng, warning cùng account có thể ghi đè |
| [S02] | Profile load/save theo tên; collection path ([S25]) theo profile; sync key/user nằm trong profile ([S26]) |
| [S03] | Sync button ([S24]) → login nếu thiếu auth → callback sync; login thành công chỉ set key/user profile hiện tại |
| [S04] | Self-host: hkey chọn User; mỗi User một collection ([S27]) và media manager, không có tham số tên profile local |
| [S05] | Collection metadata quyết định NoChanges/full/normal và chiều cho phép; empty nghĩa không có card ([S28]) |
| [S06] | UI full sync: prompt upload/download/cancel; confirm riêng khi chỉ có một chiều; download yêu cầu backup |
| [S07] | Full download integrity-check file tạm rồi replace local; server nhận upload ([S31]) integrity-check rồi replace server |
| [S08] | Normal sync: deletions → unchunked → server chunks → client chunks; transaction commit/rollback |
| [S09] | Graves ([S30]) xóa record theo ID; note/card conflict dùng pending-USN và mtime, không merge field |
| [S10] | Test collection: full upload một collection, collection thứ hai rỗng chỉ được download; normal propagation |
| [S11] | Media sync register local → fetch remote nếu USN khác → upload pending → sanity |
| [S12] | Bảng quyết định hash/dirty/deletion; unit test các nhánh |
| [S13] | ZIP download ([S36]) → add_file_from_ankiweb: normalized filename ghi trực tiếp; tên không chuẩn nhánh riêng |
| [S14] | Download cập nhật local DB clean; trường hợp rename đánh dấu deletion tên cũ + upload tên mới |
| [S15] | Local add_file chống trùng bằng hash suffix; không phải đường normal sync download |
| [S16] | Server nhận upload khác hash thay entry/file ([S34]); cùng hash/no-op deletion không tăng USN |
| [S17] | Media tombstone: server size0, USN tăng; change stream dùng empty sha1 ([S32]); client deletion khác collection graves |
| [S18] | Media tests: roundtrip, parallel requests và first-sync content thắng |
| [S19] | ChangeTracker: folder/file mtime, skipped files; manual cảnh báo sửa tại chỗ chưa chắc bị phát hiện |
| [S20] | Media RPC chạy nền; phải poll status tới inactive và không lỗi; Qt hiển thị lỗi/completion riêng ([S35]) |
| [S21] | Test server có nhánh TEST_ENDPOINT; self-host auth khác hosted; session collision không phải profile uniqueness |

## 072 — Hai profile cùng account

### Caller và behavior đã xác minh

`main.on_sync_button_clicked()` đọc auth profile hiện tại; nếu thiếu thì `sync_login()`, callback thành công tiếp tục `_sync_collection_and_media()`. `sync_login()` set `syncKey`/`syncUser` trên profile hiện tại. `ProfileManager.load/save()` đọc/ghi bản ghi theo tên; collection ở `<base>/<profile>/collection.anki2`. Không có bước liệt kê profile khác hoặc reject trùng key trong chuỗi caller này. Đây là kết luận trong **phạm vi code đã lần**, không khẳng định mọi addon hoặc server đều không thể từ chối. [S02][S03][S24][S25][S26]

Self-host tại commit này dùng `users[req.sync_key]`, mở `<server-base>/<user>/collection.anki2`; không dùng tên profile local để tách collection. Vì vậy hai auth trỏ cùng User sẽ đọc/ghi cùng collection server. Hash derivation có comment rõ “not what AnkiWeb does”; không suy rộng cách login/token hay vận hành storage private của hosted service. [S04][S27]

Backend ưu tiên kiểm tra `remote.modified == local.modified` → NoChanges; chỉ sau đó xét schema khác → FullSyncRequired. Khi schema bằng và mod khác → NormalSyncRequired. Với schema khác, `upload_ok = !local.empty || remote.empty`, `download_ok = !remote.empty || local.empty`; empty dựa trên có ít nhất một card. [S28] Do đó **tên profile và trùng account tự chúng chưa đủ xác định prompt/overwrite**. [S05][S29]

### Fixture nền F072 (suy diễn để cô lập oracle từ S02–S10)

1. Một base tạm chứa hai profile QA-A, QA-B; hai collection path thật khác nhau. Auto-sync mở/đóng tắt, media syncing tắt, addon tắt. Chỉ một profile active tại một thời điểm.
2. Server **SimpleServer đúng commit** chạy trong môi trường test loopback/cô lập, một user QA riêng; endpoint explicit, auth hợp lệ cùng user cho cả A/B. Không kế thừa `TEST_ENDPOINT`/test auth từ môi trường vì helper upstream cho phép chuyển sang external endpoint. Chưa chạy server trong nghiên cứu này. [S21]
3. A có đúng note/card marker `ONLY_A`; B có đúng note/card marker `ONLY_B`; ID/guid khác nhau, không media. Có thể dùng stock Basic một card/note. Chụp tập note/card IDs, fields, scheduling, revlog trước thao tác; không so sánh byte-identical SQLite vì metadata sync có thể đổi.
4. Chuẩn bị server bằng full upload A thành công, đợi hoàn tất. Snapshot A, B và server sau bước chuẩn bị. Kiểm tra B và server đều nonempty, `B.scm != S.scm`, `B.mod != S.mod`. Nếu tạo quá nhanh trùng timestamp, fixture chưa hợp lệ; tạo schema change hợp lệ ở B dưới clock harness rồi đo lại. Không dùng tên profile để đoán schema.
5. Mỗi nhánh dưới restore lại F072; không nối các nhánh trên trạng thái đã bị nhánh trước thay đổi. Khóa đồng hồ tránh rollover/auto actions ngoài fixture; request không lỗi, collection integrity hợp lệ.

### Các nhánh nghiệm thu chính cùng ID072

| Nhánh | Data và thao tác chính xác | Oracle backend / dữ liệu | Oracle UI |
|---|---|---|---|
| P1 — Cancel | F072; B bấm Sync; backend trả full, UI chọn Cancel | Cả hai chiều được phép; không gọi full upload/download. `ONLY_A` vẫn server/A, `ONLY_B` vẫn B. Pending edits B vẫn còn; không merge nội dung. Có thể thay profile metadata như host/url nên không assert toàn bộ profile blob bất biến | Prompt Upload/Download/Cancel; default Cancel; không phải auth error. [S05][S06] |
| P2 — Download | F072 độc lập; B bấm Sync, chọn Download; đợi full sync/reopen thành công | B chứa tập note/card/scheduling server của A; `ONLY_B` không còn trong **active B collection**. A vẫn A. Unsynced edits/revlog/graves chỉ có trong B cũ không được merge vào bản tải về. Không tuyên bố bị xóa khỏi backup: UI đã yêu cầu tạo backup trước download; chỉ assert backup request, không đoán file backup chắc chắn được tạo | Prompt full choice; download thực hiện backup request, đóng/mở collection; thành công không phải lỗi profile collision. [S06][S07][S31] |
| P3 — Upload | F072 độc lập; B bấm Sync, chọn Upload; đợi xong; chưa sync A | Server có B (`ONLY_B`), không còn `ONLY_A` trong active server collection; B vẫn B. **A local vẫn giữ A** đến khi A sync. Không merge unsynced server data vào B. [S31] Sau đó A sync, xác nhận metadata khác và chọn Download: A trở thành B | Prompt ở B; sau upload không tự đổi mọi local profile. Prompt chiều ở A do metadata; chỉ assert download khi fixture đã xác nhận nhánh full. [S05][S06][S07][S31] |

P2/P3 là điều kiện cụ thể giải thích warning manual. P1 cho thấy không nên viết AC “hễ hai profile cùng account thì luôn mất dữ liệu ngay” hoặc “luôn bị chặn”. Không gọi backend full upload để bỏ qua lựa chọn chiều của UI rồi kết luận UI cho phép. FullSyncRequired trả về trước normal transaction, nên Cancel trong fixture này không chạy merge/deletion phase. [S01][S05][S06][S08]

**Ranh giới, không mở rộng TC072:** nếu B rỗng/schema bằng/mod bằng thì nhánh có thể khác. Nếu cùng nền và normal sync, backend xử lý graves trước chunks; mtime/pending điều khiển thay record, không bảo vệ theo profile name. Collection graves xóa note/card/deck theo ID; khác media tombstone. Full download/upload của fixture072 thay snapshot file, không merge pending edits/graves của phía bị thay. Không cần thêm normal-merge example vào TC072 vì ngoài fixture hữu hạn đã chốt. [S05][S07][S08][S09][S30][S31]

### AC072 thay thế (giữ FR-SYS-PROF-001, BR-ANKI-027)

**Title:** Hai profile dùng cùng account: kết quả theo nhánh sync, không có bảo vệ namespace profile.

**Given:** hai profile tạm A/B có collection riêng nhưng cùng auth tới một user của server test đúng commit; auto-sync/media/addon tắt; server chứa A, B nonempty có marker riêng; schema/mod B khác server như F072.

**When:** B sync và thực hiện lần lượt trên snapshot độc lập các lựa chọn Cancel / Download / Upload.

**Then:** Cancel giữ nội dung hai phía; Download thay active B bằng snapshot server và bỏ các thay đổi chỉ có ở B khỏi active collection; Upload thay server bằng B còn A local giữ nguyên tới lần sync sau. Không kỳ vọng lỗi trùng account. Chỉ nghiệm thu đúng fixture/branch, không kết luận universal cho hosted server.

**TC072 data/steps/expected:** dùng F072 với đúng ba examples độc lập P1–P3 (Cancel, Download, Upload). Steps: dựng và đo preconditions → capture record snapshots → gọi UI/backend đúng entry point → capture required/prompt + chọn branch → đợi xong → so sánh IDs/fields/scheduling và auth/path → cleanup riêng. Actual vẫn Not Run. Lỗi hạ tầng/auth/I/O phải ghi error thực tế, không chấm Pass “đã chặn trùng account”.

## 077 — Cùng filename, khác nội dung

### Fixture bytes và state có thể tái lập

Hai ảnh PNG hợp lệ 1×1 RGB,69bytes; đã tính base64/SHA1 trong bộ nhớ cho báo cáo, **chưa dùng chạy sync**:

| Payload | SHA1 | Base64 |
|---|---|---|
| A, đỏ | `2732f12a8f18d27cf0fa78ef41091bfa1ccec9ce` | `iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC` |
| B, xanh | `3b37538efb87e9eb1c6d547562f499932b894f17` | `iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGNgYPgPAAEDAQAIicLsAAAAAElFTkSuQmCC` |

Tên chính xác `shared.png`: ASCII lowercase, chuẩn NFC, không path separator, không collision khác biệt hoa/thường. Hai client C1/C2 và server S có media folder/DB riêng; cùng test user; không thay đổi file trong khi sync. Mỗi branch reset snapshot. Chỉ media-sync, không collection-sync/Check Media; không sửa note field.

### M1 — Oracle chính, sequential normal sync (test upstream hỗ trợ trực tiếp)

**Initial:** S trống, `last_usn=0`; C1/C2 DB/media trống, `last_sync_usn=0`. Thêm `shared.png` A bằng `MediaManager.add_file()` ở C1, B bằng cùng API ở C2. Vì file chưa tồn tại ở mỗi folder, cả hai trả đúng `shared.png`; DB entry checksum a/b, `sync_required=true`. Assert bytes và dirty trước sync. [S15][S33]

**Order:** sync C1 tới completion → sync C2 tới completion → sync C1 kiểm tra lại. Dùng `MediaSyncer.sync(None)` hoặc backend RPC cộng poll status, không coi RPC start trả về là đã xong. [S11][S20]

**Expected:**

1. C1 upload A; S có `shared.png` hash a, size69, media USN1; C1 entry clean, `last_sync_usn=1`. [S11][S16][S17]
2. C2 begin thấy server1 khác local0; fetch trả `(shared.png,1,a)`. Local b còn dirty nhưng `determine_required_change(b,a,InDbAndPending)=Download`. [S11][S12]
3. Download ghi A trực tiếp vào `C2/shared.png`, không tạo `shared-<hash>.png`, không giữ B trong `media.trash`; `record_additions` đặt hash a/dirty=false. B chưa sync bị thay thế, không upload B trong bước sau vì pending đã hết. S không có USN2 do B. C1,C2,S đều hash a; filename count1. [S13][S14]
4. Thứ tự đối xứng C2→C1 trên fixture reset cho hash b ở cả ba bên. Đây là **first completed upload observed on next fetch wins**, không phải file timestamp hoặc “client sync sau thắng”. Upstream `parallel_requests` phần khác nội dung thực tế gọi sync1 rồi sync2 và assert cả hai là payload1. [S18]

### Những nhánh phải phân biệt để không overstate

| Nhánh | Fixture / thứ tự chính xác | Expected và nguồn |
|---|---|---|
| M2 — S chưa có thay đổi mới, local sửa sau lần sync | C1,C2,S đã đồng nhất A ở USN1; sửa tại chỗ C2 thành B, đảm bảo ChangeTracker thấy folder/file mtime đổi, xác nhận entry b/dirty=true trước network; S vẫn1. C2 sync → C1 sync | C2 localUSN=serverUSN nên không fetch overwrite; upload B thay server, S USN2; C1 fetch B; tất cả b, clean. Không tạo tên mới. Thay file mới sau nền sync là upload hợp lệ, khác M1. [S11][S16][S19] |
| M3 — hai upload in-flight, server tự host | Từ nền S trống0, hai client đã hoàn tất fetch tại0 và ZIP A/B đã chuẩn bị; dùng protocol harness/barrier, server xử lý `upload_changes(A)` xong rồi `upload_changes(B)` **mà C2 không fetch lại trước upload**. Không gọi hai normal sync tuần tự để giả mô phỏng race | S cuối b, USN2, count1. [S34] Payload upload không mang timestamp file hay expected-old-hash để CAS; register_uploaded_change khác hash → replace. Harness protocol trực tiếp không chạy local ack handler: giữ cả hai local cursor0 và dirty=true sau hai upload. C1 vẫn a, C2 vẫn b tại mốc này; tiếp theo sync C1 → C2 đầy đủ: cả hai nhận/fetch server2, C1 download b, C2 RemovePending, cuối cùng đều b và cursor2. Không mặc định “first sync wins” trong race. Đây là oracle source self-host, không assertion hosted implementation. [S16][S17][S22] |
| M4 — same hash | Giống M1 nhưng cả C1/C2 cùng A | C2 nhận checksum giống và pending→RemovePending, không upload dư, không rename, S vẫn1. Protocol upload trực tiếp cùng nội dung cũng no-op USN. [S12][S16][S18] |
| M5 — delete versus remote addition/update chưa nhận | S vừa đổi `shared.png` thành A với USN1; C2 lastUSN0, local entry tombstone `sha1=None,mtime=0,dirty=true`, không file | Fetch remote nonempty → Download kể cả local pending deletion; C2 khôi phục A và clean; không gửi deletion tiếp. [S12][S14] |
| M6 — remote deletion, local pending replacement | Baseline S/C1/C2=A,USN1. C1 xóa và sync → S tombstone USN2. C2 đã sửa thành B, dirty=true,lastUSN1, chưa nhận deletion. C2 sync | Fetch empty remote checksum với local b dirty → None, giữ B; sau đó upload B phục hồi server entry USN3. C1 sync lại → tải B. Nếu đổi duy nhất C2 thành clean A, remote deletion → Delete, file chuyển vào media.trash, local DB entry bị xóa, không upload lại. [S11][S12][S14][S17][S23] |
| M7 — add local vào folder đã có tên, không phải sync collision | Folder C1 đã có A ở shared.png. Gọi `add_file("shared.png", B)` tại chính C1 | Trả `shared-3b37538efb87e9eb1c6d547562f499932b894f17.png`; giữ A và thêm B. Hash suffix do **local import/add API**; không đem expected này áp vào M1. [S15] |

M2 cần định nghĩa **cách tạo dirty**: edit nội dung tại chỗ không nhất thiết đổi folder mtime. ChangeTracker bỏ toàn bộ scan nếu folder mtime không đổi; khi scan còn so file mtime. Test harness nên tạo/xóa sentinel riêng để đổi folder mtime, kiểm tra chênh lệch mtime thực tế hoặc dùng API fixture nội bộ cập nhật DB có transaction; không sleep cố định rồi đoán đã dirty. Folder stamp tính milliseconds, scan file mtime dùng seconds; backend add/download còn ghi mtime theo helper milliseconds. Không assert một đơn vị thống nhất cho mọi đường ghi. [S19][S38][S37]

M3 chỉ assert state từng mốc đã quy định; chưa có lịch interleaving thì không có unique winner. `send_changes` chỉ nâng local cursor khi oldUSN+processed-count bằng reply USN; nếu không, giữ cursor để lượt sau fetch phần bỏ lỡ. Như vậy sau ack upload không tự chứng minh mọi client đã hội tụ. [S11]

### Filesystem và failure semantics

Tên hợp lệ trong M1 được ghi trực tiếp bằng `write_file` trước transaction ghi media DB. Việc overwritten B không gọi helper trash/unique-name. [S33][S36] Với deletion, MediaManager helper di chuyển file sang sibling `media.trash`, còn local DB cuối fetch bỏ entry. Server deletion giữ tombstone size0 và gửi empty checksum; [S32] **không phải** collection `graves`. [S13][S14][S17][S23]

Không extrapolate M1 sang tên Unicode không chuẩn, case-only conflicts, filename cấm/too long, zero-byte/oversized file: có normalize/skip/validate riêng. Download tên không chuẩn đi nhánh unique-name; DB đánh dấu xóa tên cũ và pending tên mới, nhưng đó không phải scenario `shared.png` đã chọn. Không tuyên bố tất cả rename/reference-update được xử lý hoàn hảo khi chưa test nhánh đó. [S13][S14][S15][S19][S22]

Không hứa rollback cả filesystem khi network/I/O/sanity thất bại: file operations và DB transactions là hai bước; media sanity fail force-resync DB rồi trả ResyncRequired. Gói ZIP malformed, filesystem denied, auth expired, quota/network errors cần case riêng với injected failure và oracle theo vị trí fail. Ca077 chính chỉ kết luận success path. [S11][S13][S16][S20]

### AC077 thay thế (giữ FR-DAT-MEDI-001, BR-ANKI-028)

**Title:** Cùng filename chuẩn, khác hash: normal sync nhận server trước upload pending.

**Given:** C1/C2/S độc lập, cùng user server test đúng commit, media cursor0, server trống, C1 có shared.png=A dirty, C2 có shared.png=B dirty; checksum a khác b; không tiến trình khác sửa dữ liệu.

**When:** sync C1 xong rồi C2 xong, sau đó sync C1 kiểm tra lại.

**Then:** cả ba có đúng filename shared.png/hash a; C2 mất bản B trong active media folder, DB C2 clean, không upload B, không tạo hash-suffix backup hay media grave. Đảo thứ tự trên snapshot mới thì hash b thắng. Các nhánh M2–M7 có expected riêng; không dùng “always newest/last writer wins” cho mọi interleaving.

**TC077 data/steps/expected:** dùng PNG bytes ở trên; dựng độc lập M1 và thứ tự đảo, và M2 là examples chính; M3–M7 là boundary phân biệt, không bắt buộc mở rộng catalog trong lần chốt này (nếu thực thi M3 phải dùng protocol/server harness; M7 là local-add). Chụp filename set, SHA1 bytes, DB checksum/dirty/cursor, server USN/size/count và request order trước/sau. Steps: assert fixture → start media sync → poll status tới inactive/no exception → kiểm tra từng mốc → lượt hội tụ → cleanup. Không chỉ nhìn GUI “sync complete” hoặc số file vì count1 không phân biệt A/B. Không dùng Check Media để kích hoạt conflict resolution. [S11][S20]

## Bằng chứng test sẵn có và kế hoạch thực thi

- `media/tests.rs::parallel_requests` là evidence tĩnh sát nhất M1/M4; `media_roundtrip` xác nhận sửa/xóa truyền giữa client. Các test đã đọc, **không chạy trong lượt này**. [S18]
- `collection/tests.rs::upload_download` xác nhận collection thứ hai rỗng không được upload đè server; `regular_sync` xác nhận propagation cùng nền. Chưa có test UI hai profile cùng account trong các đoạn đã khảo sát; P1–P3 là thiết kế mới suy diễn trực tiếp từ caller + backend. [S10]
- Harness upstream có thể chọn external `TEST_ENDPOINT`; khi triển khai test sau này bắt buộc chọn explicit isolated endpoint và temp paths của fixture. Chưa có endpoint/process nào được khởi chạy trong nghiên cứu này. [S21]
- Sau thực thi cần log UI branch, phiên bản/OS, clock+timestamps, request order, before/after hashes và errors. Server hosted cần khảo sát riêng hoặc protocol-contract test; không dùng comment/source self-host làm bằng chứng kiểm thử hosted.

## Câu hỏi còn mở / giới hạn

1. Nếu acceptance bắt buộc hosted AnkiWeb thay vì SimpleServer cùng commit, owner phải cung cấp tài khoản/endpoint test được phép và chốt phạm vi contract; implementation hosted không có trong checkout. Hai AC có thể Specified cho phạm vi local isolated, không cần giữ Blocked chỉ vì hosted ngoài scope.
2. Chưa kiểm chứng runtime UI translations, OS-specific filename normalization, failure atomicity, concurrent sync không định thứ tự. Các nhánh thành công đã cố định đủ state/order để tránh oracle mơ hồ.
3. Chưa thực thi tests và chưa có QA harness cụ thể cho UI profile callback/protocol barriers; đây là dependency execution, không phải thiếu oracle thiết kế cho fixture đã nêu.

Status: DONE_WITH_CONCERNS
Summary: Chốt oracle072 theo metadata/direction/normal graves, oracle077 theo fetch-before-upload và thứ tự request; đề xuất AC/TC thay thế có data/steps/expected. Đủ evidence để design Specified trong phạm vi server thử nghiệm đúng commit; execution vẫn Not Run.
Concerns: Hosted AnkiWeb và các failure/race không cố định lịch nằm ngoài oracle; cần harness/runtime validation khi thực thi.

[S01]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/profiles.mdx#L5-L25
[S02]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L212-L239
[S03]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L307-L346
[S04]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/http_server/mod.rs#L122-L170
[S05]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L59-L89
[S06]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/sync.py#L138-L264
[S07]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/download.rs#L35-L48
[S08]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/normal.rs#L69-L142
[S09]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/chunks.rs#L159-L215
[S10]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/tests.rs#L591-L619
[S11]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/syncer.rs#L60-L269
[S12]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/changes.rs#L44-L136
[S13]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L403-L442
[S14]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/client/mod.rs#L206-L266
[S15]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L165-L225
[S16]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/server/entry/upload.rs#L35-L99
[S17]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/server/meta/mod.rs#L20-L61
[S18]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/tests.rs#L173-L294
[S19]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/client/changetracker.rs#L56-L227
[S20]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/backend/sync.rs#L188-L267
[S21]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/tests.rs#L79-L115
[S22]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/zip.rs#L50-L148
[S23]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L341-L393

[S24]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/main.py#L1090-L1129
[S25]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L308-L321
[S26]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/profiles.py#L656-L688
[S27]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/http_server/user.rs#L16-L92
[S28]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/meta.rs#L128-L148
[S29]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/backend/sync.rs#L43-L67
[S30]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/graves.rs#L47-L61
[S31]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/collection/upload.rs#L65-L96
[S32]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/database/server/entry/changes.sql#L1-L11
[S33]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/mod.rs#L60-L107
[S34]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/http_server/media_manager/upload.rs#L23-L95
[S35]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/mediasync.py#L32-L97
[S36]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/sync/media/download.rs#L23-L53
[S37]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/syncing.mdx#L54-L68
[S38]: https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/rslib/src/media/files.rs#L331-L338

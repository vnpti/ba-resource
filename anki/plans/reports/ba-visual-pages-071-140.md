# Visual QA — Word pages 071–140 và sáu PNG diagrams

- Ngày: 2026-11-02. Bản kiểm tra: BA v1.0.0 Draft, render trước đợt sửa bố cục cuối.
- Phạm vi: đã mở trực tiếp **tất cả 70 trang 71–140**, từng ảnh thật bằng `view_image`, ở tỷ lệ đọc được; không chỉ dùng contact sheet. Đã mở cả `diagram-01.png` đến `diagram-06.png`.
- Chỉ đánh giá hiển thị, không xác nhận nghiệp vụ/runtime hoặc test execution.

## Kết quả

Không thấy chữ Việt hỏng/mất dấu, nội dung bị cắt ở lề, bảng tràn ngang, chữ đè footer, hay trang hoàn toàn trắng trong 71–140. Nội dung bảng và acceptance criteria đọc được. Có vấn đề phân trang cần chỉnh; hai state diagrams có nhãn chồng nhau trong PNG ban đầu.

| Mức | Trang / artifact | Quan sát thực tế | Cách xử lý |
|---|---|---|---|
| Vừa | 79 → 80 | Hàng `BR-ANKI-025` bị chia giữa câu; trang80 bắt đầu phần tiếp diễn nhưng ô mã trống | Không cho hàng bảng tách qua trang (`w:cantSplit` / bỏ Allow row to break across pages); chuyển nguyên hàng sang80 |
| Vừa | 88 → 89 | Hàng `ERR-ANKI-000-07` bị chia; trang89 chỉ còn đoạn điều kiện “nhưng NoteType không tương thích” với ô mã trống | Cùng cách trên; giữ một rule/error trong một hàng nguyên |
| Nhẹ | 140 → trang kế tiếp | Tiêu đề `Steps` cuối trang140 đứng riêng, chưa có bước nào bên dưới | Keep with next cho tiêu đề Steps và đoạn bước đầu |
| Nhẹ | 117 | Chỉ tiêu đề “Câu hỏi còn mở” và một đoạn ngắn nằm đầu trang; phần lớn trang trắng | Điều chỉnh khoảng cách/ngắt trang phần cuối user stories để giữ đoạn kết với nội dung trước, không giảm chữ đến khó đọc |
| Nhẹ | 72,75,83,86,92,95 | Trang đuôi use case chỉ còn vài source bullets và phần giới hạn ở khoảng 15–25% đầu trang | Tối ưu spacing/keep rules ở cuối từng use case; không phải mất nội dung hay trang trắng thực sự |
| Vừa | diagram-02 | Các nhãn Good/Again/Easy quanh Review–Relearning chồng nhau; hai self-loop cùng đích khiến nhãn Again/Hard khó phân biệt | Đã sửa source `docs/anki/srs/states.md` theo yêu cầu bổ sung của root: nhãn cạnh ngắn + bảng giải mã đầy đủ; gộp hai self-loop mỗi trạng thái thành một cạnh liệt kê mã. Chờ render/recheck |
| Vừa | diagram-03 | Nhãn Bury/Unbury bên trái và Sibling bury/Unbury bên phải chồng nhau | Đã sửa cùng file: mã Q0–Q5 + bảng giải mã; giữ nguyên cạnh và ý nghĩa. Chờ render/recheck |

Không sửa nội dung nghiệp vụ. Ngoại lệ ownership được root cấp trong lúc QA: sửa layout hai Mermaid blocks và bảng giải mã trong `states.md`; guard FSRS, ma trận chuyển và Good/Easy riêng vẫn giữ.

## Sổ kiểm tra đủ trang

| Các trang đã mở riêng lẻ | Kết quả |
|---|---|
| 71–80 | Readable; lưu ý72,75 và hàng79→80 |
| 81–90 | Readable; lưu ý83,86 và hàng88→89 |
| 91–100 | Readable; lưu ý92,95; trang98 hơi thưa nhưng còn đủ nhóm nguồn, không đáng chặn |
| 101–110 | Pass; bảng tiếp diễn giữa các hàng, lặp header rõ |
| 111–120 | Pass về chữ/bảng;111 còn một hàng cuối bảng INVEST (tùy chọn keep bảng nhỏ cùng trang);117 là orphan tail |
| 121–130 | Pass; AC có tiếp diễn qua trang nhưng không mất dòng hay đè footer |
| 131–140 | Pass về chữ và biên;140 có tiêu đề Steps orphan |

## Sổ kiểm tra diagrams

| PNG | Nội dung | Kết quả visual của PNG đã mở |
|---|---|---|
| 01 | ERD | Nhãn entity/field/cardinality đọc được; không bị cắt; root đang sửa nền nhãn qua exporter riêng |
| 02 | Normal state | Cần rerender sau sửa đã nêu |
| 03 | Queue overlay | Cần rerender sau sửa đã nêu |
| 04 | Study activity | Pass; chữ Việt, decision, nhánh và arrowheads rõ |
| 05 | Sync sequence | Pass; participant, alt branches, message, lifelines rõ; không tràn khung |
| 06 | System context / usecase map | Pass; scope frame, nhóm UC, actors và text đầy đủ, không clipping |

## Giới hạn / còn mở

- Các số trang trên thuộc snapshot render đã kiểm tra; đổi pagination có thể làm dịch số trang. Dùng mã BR/ERR và tên heading để định vị sau rerender.
- Chưa xác nhận PNG02/03 sau sửa trong báo cáo này; root sẽ render lại và kiểm tra visual trước giao cuối.
- Không sửa exporter hoặc Word trực tiếp trong lượt QA này.

Status: DONE_WITH_CONCERNS
Summary: Đã kiểm tra trực tiếp70 trang và6 PNG. Không có lỗi glyph/clipping; có2 hàng bảng tách,1 heading orphan, trang đuôi thưa và2 state diagrams cần kiểm tra lại sau sửa source.
Concerns: Cần rerender, kiểm tra nhãn diagrams02/03 và pagination nêu trên.

## Recheck bản render-final — 2026-11-02

Đã mở trực tiếp đủ **18 trang được giao**: 59,60,61,62,63,64,65,66,67,69,70,82,83,91,92,143,144,180; cùng PNG02 và PNG03 cập nhật. Các số trang trong mục này thuộc bản212 trang tại `render-final`, không dùng số của snapshot đầu.

| Phạm vi | Kết quả recheck |
|---|---|
| 59 / PNG02 | Cải thiện rõ; còn chạm/chồng nhẹ giữa dấu ngoặc cuối `Good [RL3]` và chữ `A` đầu `Again [R3]` ở cạnh Review↔Relearning. Đề nghị nhãn cạnh Review→Relearning chỉ còn `R3`; bảng trang60 đã giải mã Again đầy đủ. Chưa sửa source trong lượt recheck |
| 60–63 | Bảng giải mã, guard FSRS và các khối ma trận rõ, không glyph lỗi, không cắt/đè footer |
| 64 / PNG03 | Pass; các mã Q0–Q5 và Suspend tách rõ, không còn chồng nhãn |
| 65–67 | Pass; queue dictionary và ma trận overlay/filtered rõ, các khối không bị cắt |
| 69–70 | Activity/sequence hoàn chỉnh, không clipping. Nhãn sequence nhỏ khi fit nguyên trang; đọc được khi zoom, PNG riêng cung cấp độ phân giải cao |
| 82–83 | Đóng finding split row BR-ANKI-025: toàn bộ hàng chuyển sang83, mã và diễn giải đi cùng nhau |
| 91–92 | Đóng finding split row ERR-ANKI-000-07: toàn bộ hàng chuyển sang92, không còn ô mã trống ở phần tiếp diễn |
| 143–144 | Đóng finding Steps orphan của TC-ANKI-005: Steps chuyển sang đầu144 cùng bước1. Các heading Steps khác trong hai trang cũng có bước đi cùng |
| 180 | Pass; test case, Steps, Expected/Cleanup và source links đọc được, không cắt footer |

Không có glyph Việt lỗi, mất nội dung, hay bảng vượt lề trong18 trang này. Khoảng trắng ở cuối mục là cosmetic; không phải trang trắng thực sự. Không suy rộng kết quả này thành recheck mọi trang212 trang; các trang không đổi thuộc evidence kiểm tra trước/comparison của root.

Status: DONE_WITH_CONCERNS
Summary: Recheck hoàn tất18 trang và2 PNG; split rows/Steps orphan đã sửa, queue diagram pass. Normal state diagram còn một điểm nhãn chạm nhẹ cần tinh chỉnh cuối.
Concerns: PNG02/trang59 cần nhãn R3 ngắn hơn rồi kiểm tra lại ảnh; không có blocker khác trong phạm vi đã xem.

## Release addendum — controller

Resolved remaining normal-state label collision by using R3/RL3 codes with existing trigger/guard table. Regenerated exports. Pixel comparison:208/212 pages unchanged; controller inspected changed pages59,64,69,70 directly. Labels readable, no collisions or clipping. Release visual status:PASS.

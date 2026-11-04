# Visual QA — Word pages 001–070

- Ngày: 2026-11-02.
- Status: DONE_WITH_CONCERNS.
- Phạm vi: kiểm tra trực tiếp đủ 70 ảnh `plans/2026-11-02-anki-ba-bundle/render/page-1.png` đến `page-70.png` bằng `view_image`, chế độ original; ảnh 827 × 1170 px. Không dựa riêng vào contact sheet.
- Đối tượng: bản render đang có trong lượt kiểm tra này; không xác nhận những bản xuất lại sau đó. Không chỉnh nội dung, nguồn hay ảnh.

## Phát hiện cần sửa

| Mức | Trang | Hiện tượng quan sát | Sửa cụ thể và kiểm tra lại |
|---|---|---|---|
| Cao | 35 | ERD: nhãn quan hệ trên các cạnh thành hình chữ nhật xanh xám đặc; không thấy chữ. Entity và field vẫn đọc được. | Sửa style/text/background hoặc pipeline raster SVG của nhãn Mermaid; xuất lại ERD. Xác nhận từng cạnh có nhãn đọc được, không bị nền che. |
| Cao | 58 | Sơ đồ normal study: các nhãn cạnh Review/Relearning chồng nhau; đoạn `Good hết step và không short-term`, `Again và cần học lại ngắn hạn`, `Easy` dính vào nhau. Một số đường xuyên vùng chữ. | Tăng khoảng cách các node/cạnh, bố trí lại nhãn; hoặc tách sơ đồ Learning và Relearning mà giữ các chuyển trạng thái. Xuất lại và đọc riêng từng nhãn/mũi tên. |
| Vừa | 62 | Sơ đồ queue overlay: nhãn Bury/Unbury chồng nhau ở phía trên UserBuried; nhãn Sibling bury và Unbury/đổi ngày sát/chồng ở phía trên SchedBuried. | Tách đường đi/về hoặc đặt nhãn vào vùng riêng; tăng khoảng cách đứng giữa ActiveQueue và hai nhánh. |
| Vừa | 6–7, 29–30, 30–31, 35–36 | Hàng bảng bị chia qua trang. Trang 7 mở bằng mảnh từ `nhau`/`nghiệm thu`; trang 30 mở bằng phần đuôi BR của FR-LRN-REV; trang 31 tiếp đuôi FR-DAT-BACK; trang 36 tiếp mô tả Note → Card nhưng ô quan hệ rỗng. Không phát hiện mất nội dung, nhưng khó ghép hàng khi đọc. | Đặt `cantSplit`/bỏ Allow row to break across pages cho các hàng; giữ repeat header. Xuất lại và kiểm tra vị trí ngắt trang. |
| Vừa | 67 | Sequence đồng bộ có chữ nhỏ rõ rệt so với văn bản/bảng trên cùng trang; cần phóng lớn mới đọc thuận tiện các thông điệp và nhánh alt. Không thấy clipping. | Dành trang riêng với layout ngang hoặc tách phần collection và media; tăng kích thước chữ diagram. Kiểm tra bản in/hiển thị ở kích thước trang thực. |

## Kết quả còn lại

- Không phát hiện lỗi dấu tiếng Việt, glyph ô vuông, tràn lề hoặc trang hoàn toàn trắng trong 1–70.
- Văn bản và bảng nhìn chung đọc được. Trang 66 và 68 có sơ đồ đọc được, không thấy nhãn bị mất/chồng như 35/58/62.
- Các trang đuôi chương ngắn và vùng trắng trước sơ đồ không được coi là lỗi riêng nếu là ngắt chương có chủ ý.
- Các mô tả trường từ điển dữ liệu bị tách qua nhiều trang nhưng không mất chữ; có thể dùng keep-with-next cho tên trường và nội dung khi tinh chỉnh pagination. Đây là cải thiện phụ, không thay cho sửa các lỗi trên.

## Phủ kiểm tra

Đã xem từng trang: 1–10, 11–20, 21–30, 31–40, 41–50, 51–60, 61–70. Đã mở lại trang 35, 58 và 62 để xác nhận lỗi sơ đồ; trang 15 đã kiểm tra lại, không kết luận clipping.

## Câu hỏi / giới hạn còn lại

- Chưa kiểm tra lại bản render sau sửa. Số trang có thể đổi khi bật `cantSplit` hoặc đổi kích thước sơ đồ; cần tìm theo tên sơ đồ/FR để xác nhận lại.
- Không đánh giá nội dung nghiệp vụ, hyperlink hoặc khả năng chỉnh sửa Word trong lượt visual QA này.

## Kiểm tra lại bản cuối — render-final

- Ngày: 2026-11-02. Status của phạm vi kiểm tra lại: **DONE — PASS**.
- Đã mở và đọc trực tiếp đủ 33 ảnh bản cuối bằng `view_image` original: **6, 7, 25, 26, 27, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56** tại `plans/2026-11-02-anki-ba-bundle/render-final/page-N.png`.
- **Đã sửa và xác nhận:** ERD trang 35 hiện chữ trên tất cả nhãn quan hệ; không còn các hộp nền che chữ. Các hàng bảng ở 6–7, 29–30, 30–31 và 35–36 không còn bị chia giữa trang; tên quan hệ/FR và nội dung cùng hàng giữ nguyên trên một trang.
- Các record lỗi ở 26–27 và record từ điển dữ liệu ở 36–56 giữ tên cùng mô tả. Không thấy clipping, mất dấu tiếng Việt, bảng không đọc được hoặc trang trắng mới trong 33 trang này.
- Làm rõ nhận xét sequence ở trang 67 bản đầu: chữ nhỏ hơn body nhưng vẫn đọc được tại ảnh nguyên trang 827 × 1170; không mất nội dung và không phải lỗi không đọc được tuyệt đối. Với SVG/PNG độc lập đi kèm theo thông tin controller, đây là đề xuất tăng tiện dụng, không phải blocker xuất bản.
- Sơ đồ state và sequence trong bản cuối nằm ngoài tập 33 trang được giao kiểm tra lại; controller phân công agent khác xác nhận. Phần PASS này không tự xác nhận các trang ngoài danh sách.
- Nhận xét/lỗi của lượt đầu phía trên được giữ làm lịch sử; lỗi ERD và split-row đã đóng theo bằng chứng bản cuối. Không còn blocker trong phạm vi 33 trang đã kiểm tra lại. Câu hỏi mở: không có trong phạm vi này.

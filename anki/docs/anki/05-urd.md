---
id: DOC-URD-ANKI-001
title: Yêu cầu người dùng Anki
version: "1.0.0"
phase: Elicitation
domain: Anki
tags: [urd, personas, journeys]
depends_on: [DOC-PRD-ANKI-001]
related_diagrams: []
author: BA Analysis
last_updated: "2026-11-02"
status: draft
---

# Yêu cầu người dùng Anki

## Lịch sử sửa đổi

| Phiên bản | Ngày | Nội dung |
| --- | --- | --- |
| 1.0.0 | 2026-11-02 | Nhóm người dùng, nhu cầu và hành trình suy luận từ hệ thống |

## 1. Nguồn và mức xác nhận

Nguồn: [PRD v1.0.0](01-prd.md), [manual học](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/studying.mdx), [manual soạn](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/editing.mdx), [manual sync](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/syncing.mdx). Chưa thực hiện phỏng vấn/quan sát người dùng; nhu cầu và pain point là giả thuyết BA có căn cứ chức năng, không phải lời nói của khách hàng.

## 2. Actor và phạm vi trách nhiệm

| Actor | Loại | Mục tiêu | Phạm vi |
| --- | --- | --- | --- |
| ACT-ANKI-01 Người học | Primary | Học và ôn collection của mình | Review, cấu hình, thống kê, tạm ẩn card |
| ACT-ANKI-02 Người soạn | Primary | Chuẩn bị và cập nhật kiến thức | Note, note type, media, deck, import/export |
| ACT-ANKI-03 Người dùng quản lý dữ liệu | Primary | Di chuyển và khôi phục dữ liệu | Profile, sync, backup |
| ACT-ANKI-04 Dịch vụ sync | Supporting external system | Trao đổi collection/media theo giao thức | AnkiWeb hoặc server tự host được cấu hình |
| ACT-ANKI-05 Tác giả add-on | Supporting ecosystem role | Bổ sung hành vi cho desktop | Tích hợp hooks, nằm ngoài baseline runtime mặc định |

Các actor người dùng có thể là cùng một người. Không có cơ sở để suy ra RBAC học viên/giáo viên/admin từ profile. Scheduler là thành phần bên trong hệ thống, không phải actor bên ngoài trong sơ đồ use case.

## 3. Nhu cầu và truy vết

| Mã nhu cầu | Người dùng cần | Điều kiện quan sát được | FR liên quan |
| --- | --- | --- | --- |
| UN-ANKI-001 | Soạn một nội dung và kiểm tra theo nhiều chiều | Sửa note ảnh hưởng card liên quan; mỗi card giữ lịch riêng | FR-CNT-NOTE-001, FR-CNT-TYPE-001 |
| UN-ANKI-002 | Học phần bị che trong văn bản/ảnh | Các cloze index hoặc vùng/nhóm che sinh card tương ứng | FR-CNT-CLOZ-001, FR-CNT-IMGO-001 |
| UN-ANKI-003 | Tổ chức và tìm tập kiến thức | Chọn được deck/subdeck, tìm theo tag/flag | FR-ORG-DECK-001, FR-ORG-SRCH-001 |
| UN-ANKI-004 | Biết cần học gì và phản hồi mức nhớ | Card đủ điều kiện được hiển thị; rating cập nhật trạng thái | FR-LRN-REV-001, FR-LRN-SCH-001 |
| UN-ANKI-005 | Kiểm soát công sức học | Giới hạn/preset tác động đúng phạm vi và thời điểm | FR-LRN-LIM-001, FR-LRN-FSRS-001 |
| UN-ANKI-006 | Tạm bỏ qua hoặc ôn tập có mục tiêu | Bury khác suspend; filtered deck có chế độ riêng | FR-LRN-HIDE-001, FR-LRN-FILT-001 |
| UN-ANKI-007 | Nhập/cập nhật/chia sẻ nội dung | Kết quả thêm/cập nhật/xung đột theo định dạng | FR-DAT-TEXT-001, FR-DAT-PKG-001 |
| UN-ANKI-008 | Tiếp tục học và phục hồi | Collection/media/profile có phạm vi và thao tác riêng | FR-DAT-SYNC-001, FR-DAT-BACK-001, FR-SYS-PROF-001, FR-DAT-MEDI-001 |
| UN-ANKI-009 | Xem kết quả và mở rộng cách sử dụng | Xem thống kê; quản lý add-on được chọn | FR-RPT-STAT-001, FR-EXT-ADD-001 |

Mức cấp bách đề xuất theo P0/P1 tại PRD. Chưa có khảo sát để xếp nhu cầu theo tỷ lệ người dùng hoặc giá trị doanh thu.

## 4. Hành trình học hằng ngày

| Chặng | Hành động người dùng | Kết quả hệ thống | Điểm cần giải thích |
| --- | --- | --- | --- |
| Chuẩn bị | Mở profile, chọn deck | Overview số thẻ có thể học | Tổng kho khác số được phục vụ hôm nay |
| Nhớ | Xem câu hỏi và tự nhớ | Chỉ nội dung câu hỏi trước khi Show Answer | Chưa chọn rating trong trạng thái question |
| Đối chiếu | Hiện đáp án và chọn rating | Chuyển trạng thái/lịch, ghi lịch sử | Hard vẫn là nhớ được; quên dùng Again |
| Điều chỉnh | Sửa note, bury/suspend nếu cần | Thay nội dung hoặc trạng thái queue | Không xóa note khi chỉ cần tạm ẩn |
| Kết thúc | Hết thẻ đủ điều kiện | Thông tin hoàn tất/giới hạn/chờ | Không đồng nghĩa đã nhớ toàn bộ nội dung |

## 5. Hành trình chuẩn bị nội dung

Chọn note type và deck → nhập fields/tags/media → kiểm tra mẫu câu hỏi → lưu → kiểm tra card sinh ra → học hoặc export. Người dùng cần hiểu rằng tag ở note còn deck/flag ở card; thay đổi template có thể ảnh hưởng nhiều note/card. Ngoại lệ nhập trùng và card rỗng phải được xử lý theo entry point, không dùng một thông báo giả chung.

## 6. Hành trình nhiều thiết bị và khôi phục

Sync trước khi đổi thiết bị → tiếp tục học/sửa → sync lại → kiểm tra collection và media hoàn tất. Khi yêu cầu one-way sync, người dùng xác định phía dữ liệu muốn giữ. Khi cần khôi phục, chọn backup đúng thời điểm và kiểm tra media riêng. Không xem sync là bản sao lưu có thể quay về bất kỳ thời điểm nào.

## 7. Ma trận kiểm tra nhu cầu

| Chủ đề | Bằng chứng cần để xác nhận với người dùng |
| --- | --- |
| Note/Card | Tác vụ tạo note hai chiều và giải thích lịch riêng |
| Rating | Tình huống quên, nhớ khó, nhớ có nỗ lực, nhớ ngay |
| Import/Sync/Restore | Người dùng chọn đúng thao tác cho ba tình huống khác nhau |
| Khối lượng | Người dùng giải thích vì sao hôm nay không thấy tất cả card |

## Câu hỏi còn mở

Nhóm persona nào cần ưu tiên nghiên cứu? Người dùng hiện có dùng add-on hoặc client nào? Mức quen thuộc với Note/Card và FSRS là bao nhiêu? Những thông tin này cần khảo sát, không suy ra từ source.

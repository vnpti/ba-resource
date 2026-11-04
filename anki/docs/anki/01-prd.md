---
id: DOC-PRD-ANKI-001
title: Yêu cầu sản phẩm Anki
version: "1.0.0"
phase: ProductDefinition
domain: Anki
tags: [prd, as-is, scope]
depends_on: [DOC-BRD-ANKI-001]
related_diagrams: []
author: BA Analysis
last_updated: "2026-11-02"
status: draft
---

# Yêu cầu sản phẩm Anki

## Lịch sử sửa đổi

| Phiên bản | Ngày | Nội dung |
| --- | --- | --- |
| 1.0.0 | 2026-11-02 | Danh mục 20 năng lực As-Is; ưu tiên BA đề xuất |

## 1. Tầm nhìn và mục tiêu

Anki giúp người học quản lý nội dung cần nhớ và lịch ôn từng thẻ. Vòng lặp sản phẩm là tạo/nhập nội dung → học → phản hồi → cập nhật lịch → tiếp tục ôn. Mục tiêu và phép đo đề xuất BG-ANKI-001 đến BG-ANKI-004 nằm tại [BRD v1.0.0](06-brd.md); không có OKR doanh nghiệp hoặc target hiệu năng đã được chủ dự án xác nhận.

## 2. Đối tượng sử dụng

| Persona | Vai trò | Nhu cầu | Cơ sở |
| --- | --- | --- | --- |
| PER-ANKI-01 | Người học ngôn ngữ | Học hai chiều, dùng audio, ôn theo lịch | Nhóm sử dụng được manual đề cập; hành trình BA suy luận |
| PER-ANKI-02 | Người học chuyên môn | Cloze/ảnh và quản lý nhiều nội dung cần ôn | Nhóm sử dụng được manual đề cập; chưa phỏng vấn |
| PER-ANKI-03 | Người soạn kho kiến thức | Tạo và cập nhật note/template, chia sẻ package | Suy luận từ năng lực soạn/import/export |
| PER-ANKI-04 | Người dùng nâng cao | Tùy chọn lịch, filtered deck, add-on | Suy luận từ năng lực cấu hình |

Chi tiết nhu cầu và hành trình tại [URD v1.0.0](05-urd.md). Không suy đoán tuổi, thu nhập, tần suất sử dụng hoặc tỷ lệ thiết bị.

## 3. Phạm vi

Đây là baseline mô tả các năng lực hiện có của Anki Desktop theo snapshot, không phải cam kết MVP mới. P0/P1/P2 dưới đây là mức quan trọng do BA đề xuất để đọc và kiểm thử, chưa phải backlog ưu tiên của đội Anki. Phạm vi source và giới hạn REA theo [hồ sơ chứng cứ](governance/evidence-and-scope.md).

| Năng lực / FR | Kết quả người dùng nhận được | Ưu tiên đề xuất |
| --- | --- | --- |
| FR-CNT-NOTE-001 | Tạo/sửa note và sinh card liên quan | P0 |
| FR-CNT-TYPE-001 | Quản lý cấu trúc field và mẫu thẻ | P0 |
| FR-CNT-CLOZ-001 | Tạo câu hỏi điền phần bị che | P1 |
| FR-CNT-IMGO-001 | Tạo câu hỏi từ vùng che ảnh | P1 |
| FR-ORG-DECK-001 | Tổ chức deck và subdeck | P0 |
| FR-ORG-SRCH-001 | Tìm và phân loại bằng tags/flags | P0 |
| FR-LRN-REV-001 | Xem đáp án và đánh giá mức nhớ | P0 |
| FR-LRN-SCH-001 | Chuyển trạng thái và xác định lịch ôn | P0 |
| FR-LRN-LIM-001 | Điều chỉnh lượng thẻ được phục vụ | P0 |
| FR-LRN-FSRS-001 | Điều chỉnh FSRS/preset/retention | P1 |
| FR-LRN-HIDE-001 | Bury, suspend và xử lý leech | P0 |
| FR-LRN-FILT-001 | Ôn tập thẻ được chọn theo điều kiện | P1 |
| FR-DAT-TEXT-001 | Nhập/cập nhật dữ liệu văn bản | P0 |
| FR-DAT-PKG-001 | Trao đổi deck hoặc collection package | P0 |
| FR-DAT-SYNC-001 | Đồng bộ collection giữa các lần dùng | P0 |
| FR-DAT-BACK-001 | Sao lưu và phục hồi dữ liệu học | P0 |
| FR-RPT-STAT-001 | Xem thống kê học và lịch sử | P1 |
| FR-EXT-ADD-001 | Quản lý mở rộng qua add-on | P2 |
| FR-SYS-PROF-001 | Tách collection theo profile | P1 |
| FR-DAT-MEDI-001 | Quản lý/kiểm tra/đồng bộ media | P0 |

Ngoài phạm vi: thanh toán AnkiMobile, nội bộ AnkiWeb production, quản lý lớp/học viên/giáo viên, collaborative editing, AI tutor, mọi hành vi add-on bên thứ ba. Việc nằm ngoài phạm vi khảo sát không chứng minh tính năng tương ứng không tồn tại ở nơi khác.

## 4. Ràng buộc và tiêu chí thành công của tài liệu

- Tuân theo kiến trúc note/card hiện có, không gom lịch vào note.
- Mô tả hệ thống local desktop; không đặt HTTP status cho lỗi nội bộ nếu source không có.
- Tách lựa chọn người dùng khỏi chính sách hệ thống: preset/limits/reschedule có phạm vi khác nhau.
- Không cam kết hiệu quả khoa học, doanh thu hoặc SLA chưa đo.
- Mọi FR có SRS → Story → AC → Test và chứng cứ nguồn hoặc gap được nêu rõ.

## 5. Phụ thuộc và nguồn

[SRS v1.0.0](srs/spec.md) là nơi sở hữu FR/BR/ERR. [RTM](test/test-cases.md) sở hữu truy vết kiểm thử. Nguồn sản phẩm: [README snapshot](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/README.md), [manual về nền tảng học](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/background.mdx), báo cáo phân tích source đã hoàn thành.

## Câu hỏi còn mở

Ưu tiên P0/P1/P2 và tiêu chí ra quyết định phát triển cần Product Owner xác nhận nếu dùng bộ tài liệu này cho một dự án triển khai mới.

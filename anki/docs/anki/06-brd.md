---
id: DOC-BRD-ANKI-001
title: Yêu cầu nghiệp vụ Anki
version: "1.0.0"
phase: BusinessAnalysis
domain: Anki
tags: [brd, as-is, business]
depends_on: []
related_diagrams: []
author: BA Analysis
last_updated: "2026-11-02"
status: draft
---

# Yêu cầu nghiệp vụ Anki

## Lịch sử sửa đổi

| Phiên bản | Ngày | Nội dung |
| --- | --- | --- |
| 1.0.0 | 2026-11-02 | Tái lập nghiệp vụ từ source và kết quả khảo sát; chưa có phê duyệt sản phẩm |

## 1. Bối cảnh và mục đích

Anki hỗ trợ người học tạo kiến thức cần ghi nhớ, tự kiểm tra và nhận lịch ôn dựa trên lịch sử từng card. Bài toán nghiệp vụ là phân bổ công sức ôn cho các đơn vị kiến thức theo tình trạng nhớ, đồng thời giữ quyền kiểm soát nội dung và dữ liệu học cho người dùng. Đây là diễn giải BA từ [luồng review](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/qt/aqt/reviewer.py#L532) và [mô hình note/card](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/manual/getting-started.mdx#L106).

Tài liệu mô tả hệ thống hiện có, không đề nghị xây một phiên bản Anki mới. Phạm vi tài liệu gồm 20 năng lực chức năng trong PRD/SRS, không phải kiểm kê mọi menu, API, add-on hoặc mọi nhánh triển khai của repo.

## 2. Mục tiêu nghiệp vụ và cách đánh giá

| Mã mục tiêu | Kết quả cần hỗ trợ | Cách đo đề xuất | Mức đích / người xác nhận |
| --- | --- | --- | --- |
| BG-ANKI-001 | Duy trì kiến thức qua các lần ôn | Kết quả nhớ ở lần ôn đủ điều kiện, cùng thời gian học và số thẻ đến hạn | Chưa có dữ liệu; Product Owner xác nhận định nghĩa và mục tiêu |
| BG-ANKI-002 | Tái sử dụng nội dung mà không soạn trùng | Tỷ lệ hoàn tất tạo note nhiều card; tỷ lệ import thành công theo dòng/note | Chưa đo; BA và QA xác nhận phép đo |
| BG-ANKI-003 | Tiếp tục học qua thiết bị và thời gian | Tỷ lệ tác vụ sync/restore hoàn thành không mất dữ liệu kỳ vọng | Chưa đo; người phụ trách dữ liệu/QA xác nhận |
| BG-ANKI-004 | Phục vụ nhu cầu học khác nhau | Tỷ lệ hoàn tất tác vụ với template, media, filtered deck hoặc add-on | Chưa đo; nghiên cứu người dùng cần thiết |

Chỉ số trên là đề xuất theo dõi, không phải telemetry đã xác minh có trong Anki. Desired retention của FSRS là đầu vào mô hình lịch học, không đồng nghĩa KPI giữ chân khách hàng hay tỷ lệ nhớ thực tế đã đo.

## 3. Phạm vi và bên liên quan

Trong phạm vi: desktop; soạn/tổ chức nội dung; review/lập lịch; import/export; client sync; backup/media; thống kê; profile và quản lý add-on. Ngoài phạm vi: nội bộ hosted AnkiWeb, source ứng dụng mobile, xây LMS đa người dùng, thanh toán, AI sinh nội dung, vận hành production.

| Bên liên quan | Lợi ích | Trách nhiệm cần xác nhận |
| --- | --- | --- |
| Người học | Có nội dung, lịch ôn và dữ liệu học tiếp tục được | Đánh giá mức nhớ, chọn và kiểm tra nội dung |
| Người soạn/chia sẻ | Nội dung dùng lại được | Chất lượng note/template và phạm vi package |
| Người duy trì dự án | Hiểu tác động thay đổi và tương thích | Xác nhận hành vi mong muốn khi source/manual khác nhau |
| QA / hỗ trợ | Có expected result và cách tái hiện | Chạy test với collection riêng, ghi evidence |
| Tác giả add-on | Có điểm mở rộng | Xác nhận tương thích cho add-on cụ thể |

Đây là trách nhiệm nghiệp vụ, không phải bảng phân quyền RBAC của ứng dụng.

## 4. Mô hình duy trì và ROI

Theo [website chính thức](https://apps.ankiweb.net/), desktop và đồng bộ AnkiWeb miễn phí; mua AnkiMobile góp phần hỗ trợ phát triển. [FAQ trong snapshot](https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/docs-site/faqs/how-can-i-donate.mdx#L7) phân biệt tài trợ Anki và đóng góp cho đội AnkiDroid. Chưa có bằng chứng doanh thu hoặc cơ cấu chi phí.

Nếu đánh giá một dự án áp dụng hoặc tùy biến Anki, dùng công thức đề xuất: `ROI = (Lợi ích quy đổi - Tổng chi phí) / Tổng chi phí × 100%`, với kỳ đo và chi phí lớn hơn 0 được thống nhất trước. Không đưa ra ROI số khi chưa có đầu vào.

| Đầu vào cần thu thập | Cách lấy | Trạng thái |
| --- | --- | --- |
| Thời gian học trước/sau với cùng mục tiêu | Nghiên cứu có nhóm/điều kiện so sánh phù hợp | Chưa có |
| Chi phí thiết lập, soạn nội dung, đào tạo | Time log và đơn giá được chủ dự án xác nhận | Chưa có |
| Chi phí bảo trì, hỗ trợ, hạ tầng nếu tự host | Dữ liệu vận hành và báo giá thực tế | Chưa có |
| Giá trị của kết quả ghi nhớ | Chủ dự án thống nhất cách quy đổi hoặc giữ chỉ số phi tài chính | Chưa có |

## 5. Rủi ro và kiểm soát

| Rủi ro | Tác động | Kiểm soát / cách xác minh |
| --- | --- | --- |
| Nhầm Hard với Again | Tín hiệu lịch học không phản ánh việc quên | Hướng dẫn rating và kiểm thử hiểu biết người dùng |
| Nhập/sync/restore sai phạm vi | Thay hoặc bỏ sót dữ liệu cần giữ | Test collection riêng, phân biệt apkg/colpkg/full sync và media |
| Tăng thẻ mới quá mức phù hợp | Tăng tải ôn về sau | Kiểm tra giới hạn ngày, backlog và thời gian học |
| Add-on thay đổi đường mặc định | Expected result không còn phù hợp | Ghi danh sách/phiên bản add-on; chạy baseline không add-on rồi kiểm tra riêng |
| Tài liệu và mã khác nhau | Đặc tả sai điều kiện nghiệm thu | Giữ issue mở, tái hiện runtime trước khi chốt |

## 6. Điều kiện bàn giao

Bộ tài liệu được bàn giao khi ID và liên kết hợp lệ, mỗi FR có nguồn, downstream có RTM và giới hạn được công bố. Phê duyệt nghiệp vụ, thực thi test và quyết định triển khai là các bước riêng do người có thẩm quyền thực hiện. Danh mục quyết định tại [hồ sơ kiểm soát](governance/decisions-and-handoff.md).

## Câu hỏi còn mở

Ai là Product Owner/người duyệt tài liệu? Mục tiêu định lượng và kỳ đo nào được chấp nhận? Có cần phân tích triển khai cụ thể với mobile/add-on không? Các câu hỏi này không chặn xuất bản tài liệu khảo sát Draft.

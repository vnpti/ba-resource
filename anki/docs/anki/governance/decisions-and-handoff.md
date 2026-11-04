---
id: DOC-GOV-ANKI-001
title: Quyết định và bàn giao bộ tài liệu BA
version: "1.0.1"
phase: Handoff
domain: Anki
tags: [decisions, risks, handoff, approval]
depends_on: [DOC-EVID-ANKI-001, DOC-BRD-ANKI-001]
related_diagrams: []
author: BA Analysis
last_updated: "2026-11-03"
status: draft
---

# Quyết định và bàn giao bộ tài liệu BA

## Lịch sử sửa đổi

| Phiên bản | Ngày | Nội dung |
| --- | --- | --- |
| 1.0.1 | 2026-11-03 | Làm rõ bốn oracle từ source; cập nhật phạm vi/truy vết liên quan, giữ Draft và Not Run |
| 1.0.0 | 2026-11-02 | Ghi quyết định phạm vi, issue mở, trách nhiệm thẩm định và hướng bàn giao |

## 1. Quyết định phạm vi có căn cứ

| Mã | Quyết định | Nguồn và ý nghĩa |
| --- | --- | --- |
| DEC-ANKI-001 | Tái lập Anki Desktop tại commit cố định | README upstream và yêu cầu phân tích repo |
| DEC-ANKI-002 | Dùng REA kết hợp đọc source/manual | Yêu cầu người dùng; REA chỉ bao phủ target TypeScript đã ghi |
| DEC-ANKI-003 | Xuất bộ BA tiếng Việt với truy vết | Yêu cầu người dùng trong cuộc hội thoại ngày 2026-11-02 |
| DEC-ANKI-004 | Giữ Draft, chưa ghi người duyệt | Chưa có bằng chứng phê duyệt từ chủ sản phẩm |
| DEC-ANKI-005 | Test case là thiết kế, trạng thái Not Run | Chưa chạy Anki; xuất tài liệu không phải kiểm thử sản phẩm |
| DEC-ANKI-006 | Không tự đặt ROI/SLA/estimate | Không có dữ liệu/người xác nhận; chuyển thành câu hỏi có owner |
| DEC-ANKI-007 | Làm rõ 4 oracle theo source, giữ ID và Not Run; bản bộ 1.0.1 | Yêu cầu tiếp tục đối chiếu/cập nhật/export của người dùng ngày 2026-11-03; không sửa sản phẩm |

## 2. Các vấn đề cần thẩm định

Owner dưới đây là vai trò đề xuất, chưa phải cá nhân đã nhận việc.

| ID | Vấn đề | Tác động | Owner / bước xác minh |
| --- | --- | --- | --- |
| OQ-ANKI-001 | Manual studying nói learning không bị bury, nhưng code và deck options hỗ trợ interday learning | Có thể viết AC sai nếu gộp intraday/interday | Người duy trì scheduler và QA tái hiện hai loại card |
| OQ-ANKI-002 | Đã chốt As-Is: không dedup review/card/day; manual khác code | Oracle AC/TC-067 Specified; còn quyết định To-Be sửa manual hay implementation | Owner thống kê/sản phẩm; runtime vẫn Not Run |
| OQ-ANKI-003 | Package Always vẫn bỏ qua timestamp bằng nhau tại helper | Ảnh hưởng cập nhật note đã tồn tại | Owner import xác minh ý nghĩa UI và caller |
| OQ-ANKI-004 | Cardgen có fallback ensure_not_empty | Không thể khẳng định mọi front rỗng đều không sinh card | Owner content xác định caller/điều kiện |
| OQ-ANKI-005 | Đã chốt oracle media theo filename chuẩn, cursor/dirty và thứ tự sync | AC/TC-077 Specified cho server test cùng commit; không khái quát race bất định | Đóng thiếu oracle thiết kế ngày 2026-11-03; QA thực thi còn Not Run |
| OQ-ANKI-006 | Chưa có SLA, mục tiêu KPI, ROI, story point | Không dùng tài liệu làm hợp đồng chất lượng/chi phí | Product Owner, QA và đội phát triển xác nhận |
| OQ-ANKI-008 | Zero training item giữ params/count0/health absent; UI no reviews | AC/TC-035 Specified, không giả lỗi thiếu review threshold | Đóng thiếu oracle thiết kế ngày 2026-11-03; QA thực thi còn Not Run |
| OQ-ANKI-009 | Caller không reject account trùng; fixture hai bên nonempty/mod khác/schema khác xác định full sync | AC/TC-072 Specified theo Cancel/Download/Upload; scope SimpleServer | Đóng thiếu oracle thiết kế ngày 2026-11-03; hosted implementation ngoài xác minh |
| OQ-ANKI-007 | Hành vi mobile, hosted service và add-on cụ thể | Ngoài baseline runtime đã khảo sát | Mở phạm vi riêng khi có mục tiêu triển khai |

## 3. Ma trận thẩm định

| Vai trò | Phần cần kiểm tra | Trạng thái |
| --- | --- | --- |
| Business/Product Owner | BRD, PRD, URD, ưu tiên và KPI | Chưa chỉ định, chưa duyệt |
| Maintainer/Tech Lead | SRS, source mapping, schema và giới hạn thuật toán | Chưa duyệt |
| QA Lead | Fixture, expected, coverage và test cần runtime | Chưa chạy test, chưa duyệt |
| Đại diện người dùng | Persona, thuật ngữ, journeys | Chưa thực hiện nghiên cứu xác nhận |

Không có chữ ký, tên người duyệt hay ngày approval được điền thay. Việc validation cấu trúc thành công chỉ xác nhận cấu trúc và truy vết của tài liệu.

## 4. Checklist sử dụng và bàn giao

1. Đọc PRD để xác định 20 FR thuộc phạm vi; đọc SRS để lấy BR/ERR chính thức của baseline.
2. Đọc ERD và trạng thái trước khi diễn giải nghiệp vụ Note/Card, queue và filtered deck.
3. Dùng use case cho walkthrough; dùng backlog/AC cho refinement; dùng test case cho thực thi QA.
4. Với test cần clock, state cũ, lỗi backend hoặc hai thiết bị, thiết lập harness/collection riêng theo TC. Không dùng collection thật.
5. Khi chạy test, ghi build/commit, môi trường, dữ liệu, người chạy, thời gian và evidence; chỉ đổi Not Run thành Pass/Fail sau thực thi.
6. Giải quyết OQ và NFR chưa chốt trước khi dùng tài liệu như một cam kết triển khai.

## 5. Quản lý thay đổi

Không có CR sản phẩm mới trong lần xuất này. Khi có yêu cầu đổi hành vi, lập CR với ID riêng, source/target version, before/after, FR/BR/ERR/US/AC/TC và sơ đồ chịu tác động. Dùng RTM để tìm downstream; giữ baseline khi CR còn đề xuất. Thay đổi đã được người dùng/chủ dự án cho phép trong phiên không cần xin lại, nhưng phải ghi nguồn cho phép.

Ví dụ quy trình, không phải CR thực tế: nếu thay chính sách sync, xác định SRS → use case sync → story → AC/TC → data/state/sequence liên quan; chỉ cập nhật những file bị ảnh hưởng và giữ test về Not Run cho phần thay đổi. Không đổi hàng loạt giá trị ở lịch sử tài liệu.

## Câu hỏi còn mở

Còn OQ-ANKI-001,003,004,006,007; OQ-ANKI-002 chỉ còn quyết định To-Be manual/code, oracle As-Is đã rõ. OQ-ANKI-005,008,009 đã đóng thiếu oracle thiết kế theo fixture, không phải đóng kiểm thử runtime. Người duyệt và ngưỡng chất lượng vận hành chưa được chỉ định/xác nhận.

---
id: DOC-INDEX-ANKI-001
title: Danh mục bộ tài liệu BA Anki
version: "1.0.1"
phase: Handoff
domain: Anki
tags: [index, baseline, handoff]
depends_on: []
related_diagrams: []
author: BA Analysis
last_updated: "2026-11-03"
status: draft
---

# Danh mục bộ tài liệu BA Anki

## Lịch sử sửa đổi

| Phiên bản | Ngày | Nội dung |
| --- | --- | --- |
| 1.0.1 | 2026-11-03 | Làm rõ bốn oracle từ source; cập nhật phạm vi/truy vết liên quan, giữ Draft và Not Run |
| 1.0.0 | 2026-11-02 | Xuất bộ tài liệu As-Is phục vụ thẩm định |

## 1. Cách sử dụng

Bộ tài liệu trình bày nghiệp vụ hiện có của Anki Desktop tại commit `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`. Có 20 năng lực chức năng, 28 quy tắc, 8 tình huống lỗi phân tích, 8 mục phi chức năng, 10 use case, 20 user story, 86 AC/test case và 6 sơ đồ. Đây là bộ tài liệu theo cấu trúc BA-kit, chưa được chủ sản phẩm duyệt và không phải chứng nhận IEEE/ISO.

Trình tự đọc: BRD → PRD → URD → SRS → mô hình/use case → backlog → AC → test/RTM → hồ sơ bàn giao. Các bản HTML, Word và PDF được sinh từ cùng nguồn Markdown. Bản Word/PDF trình bày ma trận quá rộng thành bản ghi có nhãn để giữ nội dung đọc được; CSV giữ dạng bảng cho QA.

## 2. Danh mục tài liệu

| Nhóm | Tài liệu | Mục đích |
| --- | --- | --- |
| Nghiệp vụ | [BRD](06-brd.md) | Mục tiêu, phạm vi, lợi ích, ROI đầu vào, rủi ro |
| Sản phẩm | [PRD](01-prd.md) | Danh mục năng lực, persona, ưu tiên đề xuất |
| Người dùng | [URD](05-urd.md) | Actor, nhu cầu, journeys |
| Đặc tả | [SRS](srs/spec.md) | Nơi định nghĩa FR/BR/ERR/NFR và interfaces |
| Chứng cứ | [Source matrix](srs/code-derived-spec.md) | Nối yêu cầu với file/dòng tại commit |
| Dữ liệu | [ERD và từ điển](srs/erd.md) | Thực thể, thuộc tính, kiểu, quan hệ và ràng buộc |
| Trạng thái | [Card và queue](srs/states.md) | State, trigger, guard, side effects |
| Quy trình | [Activity, sequence, context](diagrams/flows.md) | Luồng học, sync và ranh giới hệ thống |
| Use case | [UC 001](usecases/UC-ANKI-001.md) · [002](usecases/UC-ANKI-002.md) · [003](usecases/UC-ANKI-003.md) · [004](usecases/UC-ANKI-004.md) · [005](usecases/UC-ANKI-005.md) | Nội dung, tổ chức, học và cấu hình |
| Use case | [UC 006](usecases/UC-ANKI-006.md) · [007](usecases/UC-ANKI-007.md) · [008](usecases/UC-ANKI-008.md) · [009](usecases/UC-ANKI-009.md) · [010](usecases/UC-ANKI-010.md) | Filtered, nhập/xuất, sync và quản lý dữ liệu |
| Backlog | [User stories](userstories/backlog.md) | Giá trị người dùng, FR nguồn, INVEST và phụ thuộc |
| Nghiệm thu | [Acceptance Criteria](userstories/acceptance-criteria.md) | Gherkin happy/negative/boundary |
| Kiểm thử | [Test cases và RTM](test/test-cases.md) | Fixture, steps, expected, cleanup, trạng thái Not Run |
| Kiểm soát | [Evidence và phạm vi](governance/evidence-and-scope.md) | Phương pháp, REA và giới hạn |
| Bàn giao | [Quyết định và câu hỏi mở](governance/decisions-and-handoff.md) | Owner, approval, issue và change control |

## 3. Nguồn máy đọc và quy ước

[requirements.json](srs/requirements.json) là catalog máy đọc đồng bộ SRS. [qa-catalog.json](test/qa-catalog.json) và [traceability.csv](test/traceability.csv) phục vụ kiểm tra liên kết. Test cases sở hữu RTM; không có bảng truy vết thứ hai được chỉnh độc lập.

FR/BR/ERR mô tả baseline khảo sát. Story point, SLA/KPI và approval chưa xác nhận không được tự điền. `000` trong ERR là nhãn không-HTTP của catalog, không phải mã do ứng dụng trả. Coverage là độ phủ thiết kế trong phạm vi 20 FR, không phải phần trăm đã kiểm thử toàn bộ Anki.

## 4. Trạng thái bàn giao

Bản bộ là Draft 1.0.1; file có thay đổi lên patch 1.0.1, file còn lại giữ 1.0.0. Độ phủ thiết kế hợp lệ: FR 20/20, BR 28/28, ERR 8/8, AC 86/86. Bốn oracle035/067/072/077 đã chốt từ source theo fixture; thực thi 0/86, tất cả Not Run. Bộ tài liệu có thể dùng để walkthrough và chuẩn bị QA. Trước khi sử dụng làm baseline triển khai hoặc nghiệm thu, người có thẩm quyền xác nhận các mục mở, môi trường test và NFR còn thiếu ngưỡng.

## Câu hỏi còn mở

Xem trạng thái từng OQ tại hồ sơ bàn giao. Bốn oracle đã đủ thiết kế nhưng quyết định sản phẩm, NFR, approval và thực thi còn được theo dõi; không coi việc xuất file là bằng chứng phê duyệt hoặc test Pass.

Bản 1.0.1 làm rõ source hiện hữu, không thêm năng lực sản phẩm hoặc đổi ID. Tham chiếu version1.0.0 trong tài liệu không thay đổi là baseline ban đầu; patch này giữ phạm vi và ID tương thích.

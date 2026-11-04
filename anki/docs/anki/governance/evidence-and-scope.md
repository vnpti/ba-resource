---
id: DOC-EVID-ANKI-001
title: Phạm vi và bằng chứng phân tích
version: "1.0.1"
phase: Governance
domain: Anki
tags: [evidence, rea, scope]
depends_on: []
related_diagrams: []
author: BA Analysis
last_updated: "2026-11-03"
status: draft
---

# Phạm vi và bằng chứng phân tích

## Lịch sử sửa đổi

| Phiên bản | Ngày | Nội dung |
| --- | --- | --- |
| 1.0.1 | 2026-11-03 | Làm rõ bốn oracle từ source; cập nhật phạm vi/truy vết liên quan, giữ Draft và Not Run |
| 1.0.0 | 2026-11-02 | Chốt snapshot, phân loại chứng cứ và giới hạn |

## 1. Định danh đối tượng

- Repository: [ankitects/anki](https://github.com/ankitects/anki).
- Commit: `136bd42bfbd356fc756b6d3e28cc77b02da11ea7`, nhánh main tại thời điểm clone; ngày commit 2026-10-29.
- `.version`: `26.09.3`. Không coi snapshot nhánh main là release binary đã kiểm định.
- Bộ BA cập nhật ngày 2026-11-03; phiên bản bộ 1.0.1, tiếng Việt, Draft. Chỉ file thay đổi được nâng patch; tài liệu không đổi giữ 1.0.0.
- Mô tả 20 năng lực được liệt kê trong PRD, không kiểm toán toàn bộ repository hoặc mọi ứng dụng trong hệ sinh thái.

## 2. Hệ thống nguồn

| Nguồn | Có thể chứng minh | Không thể chứng minh |
| --- | --- | --- |
| Rust/Python/TypeScript/protobuf/SQL tại commit | Khai báo và logic tĩnh trong nhánh đã đọc | Hành vi mọi môi trường runtime, mọi add-on |
| Manual trong cùng commit | Hành vi được tài liệu mô tả | Không bảo đảm luôn đồng nhất với implementation |
| Website chính thức | Thông tin công khai về sản phẩm/hệ sinh thái | Doanh thu, MAU, chi phí hoặc hệ thống nội bộ |
| REA Evidence | AST, module, import và quan hệ tĩnh trong thư mục khảo sát | Toàn bộ scheduler, sync, Svelte UI hoặc runtime |
| Phân tích BA | Mô hình, diễn giải, cấu trúc đặc tả và test design | Phê duyệt nghiệp vụ hay kết quả test đã chạy |

Các source link cố định theo commit để truy vết. SRS và source matrix giữ đường dẫn/dòng; REA JSON đầy đủ được đóng gói ở thư mục evidence của ZIP.

## 3. REA đã thực hiện

Target: `ts/routes/deck-options`. Parent Evidence: `ev_b577322d29549c59bbc0cdf59e6481ea2e6fa3b6269a6ba6cc0a9bff8caf398d`.

REA đọc 7 file TypeScript, trong đó có 2 file test; 39.883 byte text; 4.684 AST nodes; 121 findings; 0 parse failures. Đây không phải 121 quy tắc nghiệp vụ. `lib.ts` có các export `DeckOptionsState`, `ValueTab`, `commitEditing`, `createLimits`, `fsrsParams`. Import backend ở trạng thái external; không resolve xuyên sang Rust trong target này.

SHA-256 tree theo REA: `7a5e83769d0a9cca1fc6d262491eb34b2bcd324c3eec853f54dd9dc34d9325ac`. SHA-256 `lib.ts`: `691ca18e2fea2dfcfd87b5e650c9fb31514a99984c51dcd0d047591919e89e33`.

Semantic coverage là unknown với 1.036 semantic unknowns. Application coverage complete chỉ áp dụng inventory của target đã chọn. Nhãn authority shipped-artifact trong output không biến source checkout thành một binary phát hành. Không thực thi JavaScript hoặc ứng dụng Anki trong khảo sát này.

## 4. Quy ước áp dụng BA kit

Đã dùng các skill ba-brd, ba-prd, ba-urd, ba-srs, ba-code-to-srs, ba-usecase, ba-erd, ba-state, ba-userstory, ba-ac, ba-test-cases và ba-export, cùng metadata/versioning/traceability rules. Các sơ đồ bổ sung là phần phụ lục SRS; không giả phê duyệt hoặc chứng nhận IEEE/ISO.

FR/BR/ERR mới thuộc baseline chuẩn hóa ở SRS. Mã BR trong báo cáo khảo sát ban đầu giữ nguyên và có bảng đối chiếu; không sửa lịch sử để giả rằng chúng là cùng namespace. `000` trong mã ERR biểu thị không áp dụng HTTP cho catalog phân tích desktop; cột HTTP là N/A. Localization chưa quan sát được ghi chưa xác minh.

Xuất bản Draft theo yêu cầu người dùng không phải approval nội dung. Quy trình export của kit vốn nói thu thập tài liệu được duyệt; ở đây xuất bản khảo sát có trạng thái hiển thị rõ và không gán người/ngày duyệt.

## 5. Bổ sung đối chiếu source ngày 2026-11-03

REA evidence cũ giữ nguyên, không giả thành kết quả chạy mới. Bốn oracle lần này được xác định bằng đọc caller, implementation, SQL/protobuf/UI và upstream test source; không chạy các test đó. [Bản ghi máy đọc và SHA-256 source](../../../evidence/oracle-resolutions-2026-11-03.json) lưu fixture/expected/nguồn; PNG mẫu media nằm ở evidence/fixtures trong ZIP.

| Ca | Oracle As-Is được chốt | Giới hạn |
| --- | --- | --- |
| AC/TC-ANKI-035 | 0 training item trả nguyên params, count0, health absent; UI no reviews | Optimize current preset, không phải Optimize All |
| AC/TC-ANKI-067 | Hai log Review cùng card/ngày Again+Good đều tính: Count2,50.0% | Cửa sổ scheduler/search cố định; manual first/day khác code |
| AC/TC-ANKI-072 | FullSync fixture: Cancel giữ nội dung, Download thay local, Upload thay server | Nonempty, mod/schema khác; SimpleServer cùng commit |
| AC/TC-ANKI-077 | Remote change chưa nhận có thể ghi đè local dirty; localdirty khi cursor hiện hành upload được | Filename chuẩn, payload và thứ tự sync xác định; không áp mọi race |

Báo cáo đối chiếu: [FSRS](../../../plans/reports/2026-11-03-fsrs-oracle.md), [retention](../../../plans/reports/2026-11-03-retention-oracle.md), [profile/media](../../../plans/reports/2026-11-03-sync-media-oracles.md), [review độc lập](../../../plans/reports/2026-11-03-oracle-review.md). Bộ test chính giữ 86 ID; fixture retention22row và các nhánh sync mở rộng trong báo cáo là tài liệu tham khảo thiết kế, không tự được tính thành test đã chạy.

## 6. Câu hỏi còn mở

Mọi khác biệt source/manual và phạm vi chưa khảo sát được quản lý tại [sổ quyết định và bàn giao](decisions-and-handoff.md). Source tĩnh không thay thế kiểm thử runtime.

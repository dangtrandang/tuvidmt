# lasotuvi — vendored

Nguồn: https://github.com/doanguyen/lasotuvi (MIT License, (c) doanguyen)
Vendor ngày 2026-07-03 để làm engine an sao Tử Vi Đẩu Số (phái Việt Nam,
Tuần Triệt, theo sách Thiên Lương / Thái Thứ Lang) cho app trolychiemtinh.
Mọi chỉnh sửa so với bản gốc được đánh dấu comment `# [TLCT]` kèm lý do.

## Audit 2026-07-03 (bé Devapp — đọc 100% source trước khi chạy, theo yêu cầu anh Sơn)
- An ninh: SẠCH. Chỉ import `math`, `time.strftime`. Không network/file-IO/exec/subprocess.
- Đã xóa `Lich_EPHEM.py` (bản lịch thay thế dùng pyephem, không cần — dùng Lich_HND thuần).
- Bug phát hiện (sẽ sửa, đánh dấu [TLCT]):
  1. ThienBan.py:65-66 — menhChu/thanChu tra `diaChi[self.canNam]` (SAI: can 1-10
     index vào bảng địa chi 1-12); phải tra theo `self.chiNam`.
  2. [ĐÃ SỬA 2026-10-11 - TLCT] Sao singleton module-level + themSao: đã cô lập
     bằng copy.copy(sao) trong DiaBan.themSao và gán None tường minh trong dacTinhSao.
     Engine an toàn tuyệt đối cho long-running server / concurrent API.
  3. `x is 0` so sánh int literal (AmDuong.dichCung...) → SyntaxWarning Python≥3.8,
     hoạt động đúng trên CPython; nên đổi == khi tiện (đã sửa [TLCT]).


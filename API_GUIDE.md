# 📖 HƯỚNG DẪN TÍCH HỢP TỬ VI BACKEND API

Tài liệu này cung cấp hướng dẫn đầy đủ, chi tiết và các đoạn mã mẫu sẵn sàng sao chép (copy-paste) để bạn dễ dàng tích hợp API lập lá số Tử Vi vào bất kỳ ứng dụng nào (Web, Mobile App, Bot, WordPress...).

---

## 1. Thông tin kết nối (Base URL)

- **Production API URL (VPS có SSL):** `https://api.hongngochuyenhoc.com`
- **Tài liệu trực quan tương tác (Swagger UI):** `https://api.hongngochuyenhoc.com/docs`
- **Tài liệu ReDoc:** `https://api.hongngochuyenhoc.com/redoc`
- **Môi trường Test Local (khi chạy máy tính):** `http://127.0.0.1:8000`

> [!NOTE]
> **CORS:** API đã được cấu hình mở toàn bộ (`allow_origins=["*"]`). Bất kỳ trang web nào (kể cả chạy từ `localhost`, `vercel.app`, hay tên miền riêng) đều có thể gọi trực tiếp bằng JavaScript mà không bị trình duyệt chặn.

---

## 2. Danh sách Endpoints

### 2.1. Kiểm tra trạng thái máy chủ (Health Check)
Dùng để kiểm tra xem server backend có đang hoạt động hay không.

- **Phương thức:** `GET`
- **Đường dẫn:** `/api/v1/health`
- **Phản hồi mẫu (`200 OK`):**
  ```json
  {
    "status": "ok",
    "message": "Tu Vi Backend API is running",
    "version": "1.0.0"
  }
  ```

---

### 2.2. Lập lá số Tử Vi Đẩu Số (Core API)
Nhận thông tin ngày giờ sinh của đương số, tự động an sao và trả về toàn bộ dữ liệu lá số.

- **Phương thức:** `POST`
- **Đường dẫn:** `/api/v1/laso`
- **Header bắt buộc:** `Content-Type: application/json`

#### Tham số đầu vào (Request Body JSON):

| Tên trường | Kiểu dữ liệu | Bắt buộc | Mặc định | Ý nghĩa & Quy tắc |
| :--- | :--- | :---: | :---: | :--- |
| `ho_ten` | `string` | Không | `"Vô danh"` | Họ và tên của đương số |
| `ngay_sinh` | `integer` | **Có** | - | Ngày sinh (từ `1` đến `31`) |
| `thang_sinh` | `integer` | **Có** | - | Tháng sinh (từ `1` đến `12`) |
| `nam_sinh` | `integer` | **Có** | - | Năm sinh (ví dụ `1990`) |
| `gio_sinh` | `integer` | **Có** | - | Giờ sinh theo đồng hồ 24h (`0` đến `23`) |
| `phut_sinh` | `integer` | Không | `0` | Phút sinh (`0` đến `59`) |
| `gioi_tinh` | `integer` / `string` | **Có** | - | Giới tính: `1` hoặc `"nam"` (Nam), `-1` hoặc `"nu"` (Nữ) |
| `duong_lich` | `boolean` | Không | `true` | `true` nếu là Dương lịch; `false` nếu là Âm lịch |
| `thang_nhuan` | `boolean` | Không | `false` | `true` nếu sinh vào tháng nhuận (chỉ áp dụng cho Âm lịch) |
| `mui_gio` | `float` | Không | `7.0` | Múi giờ sinh (mặc định `7.0` cho Việt Nam) |

#### 🕒 Bảng quy đổi Giờ sinh sang Canh giờ Tử Vi (12 Địa Chi):
Hệ thống tự động chuyển đổi giờ/phút thành 12 canh giờ theo quy tắc Tử Vi chuẩn:
- **Giờ Tý:** 23h00 hôm trước - 00h59 sáng *(Nếu sinh sau 23h00, engine tự động cộng 1 ngày sang hôm sau để tính giờ Tý của ngày mới)*.
- **Giờ Sửu:** 01h00 - 02h59
- **Giờ Dần:** 03h00 - 04h59
- **Giờ Mão:** 05h00 - 06h59
- **Giờ Thìn:** 07h00 - 08h59
- **Giờ Tỵ:** 09h00 - 10h59
- **Giờ Ngọ:** 11h00 - 12h59
- **Giờ Mùi:** 13h00 - 14h59
- **Giờ Thân:** 15h00 - 16h59
- **Giờ Dậu:** 17h00 - 18h59
- **Giờ Tuất:** 19h00 - 20h59
- **Giờ Hợi:** 21h00 - 22h59

---

## 3. Cấu trúc dữ liệu phản hồi (Response Data)

Khi gọi thành công, API trả về mã `HTTP 200` với 2 khối dữ liệu chính:

```json
{
  "thien_ban": { ... },
  "dia_ban": [ ... ]
}
```

### 3.1. Khối `thien_ban` (Thông tin tổng quan lá số)
Chứa đầy đủ thông tin Bát tự Can Chi, Bản mệnh và Cục:
- `ho_ten`: Họ tên người xem.
- `nam_nu`: "Nam" hoặc "Nữ".
- `ngay_duong`, `thang_duong`, `nam_duong`: Ngày tháng năm Dương lịch.
- `ngay_am`, `thang_am`, `nam_am`: Ngày tháng năm Âm lịch.
- `can_gio_sinh`, `chi_gio_sinh`: Tên Can Chi giờ sinh (ví dụ: "Bính", "Thân").
- `can_ngay`, `chi_ngay`: Can Chi ngày sinh.
- `can_thang`, `chi_thang`: Can Chi tháng sinh.
- `can_nam`, `chi_nam`: Can Chi năm sinh (ví dụ: "Canh", "Ngọ").
- `ban_menh`: Ngũ hành nạp âm của bản mệnh (ví dụ: `"LỘ BÀN THỔ"`).
- `ten_cuc`: Tên Cục định mệnh (ví dụ: `"Thổ ngũ Cục"`).
- `menh_chu`, `than_chu`: Sao Mệnh chủ và Thân chủ.
- `sinh_khac`: Tương quan Ngũ hành giữa Bản mệnh và Cục.
- `am_duong_menh`: "Âm dương thuận lý" hoặc "Âm dương nghịch lý".

### 3.2. Khối `dia_ban` (Danh sách 12 Cung)
Mảng gồm đúng **12 phần tử** đại diện cho 12 cung từ Tý đến Hợi:
- `cung_so`: Số thứ tự cung (1: Tý, 2: Sửu, ..., 12: Hợi).
- `ten_cung`: Tên địa chi cung ("Tý", "Sửu", "Dần"...).
- `cung_chu`: Tên cung chức quản lý ("Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc", "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ").
- `hanh_cung`: Ngũ hành của cung ("Thủy", "Thổ", "Mộc", "Hỏa", "Kim").
- `is_than`: `true` nếu cung này là nơi **Thân cư** (ví dụ Thân cư Phu Thê, Thân cư Quan Lộc...).
- `dai_han`: Tuổi bắt đầu khởi đại hạn 10 năm tại cung này (ví dụ `5`, `15`, `25`...).
- `tieu_han`: Tên chi tiểu hạn tương ứng của cung.
- `tuan`: `true` nếu cung dính sao **Tuần Không** (`false` nếu không dính).
- `triet`: `true` nếu cung dính sao **Triệt Lộ** (`false` nếu không dính).
- `sao`: Danh sách tất cả các sao đóng tại cung này.
  - `ten_sao`: Tên sao tiếng Việt (ví dụ: "Tử Vi", "Thiên Phủ", "Hóa Khoa"...).
  - `loai_sao`: `1` là Chính tinh, `2` trở lên là Phụ tinh.
  - `ngu_hanh`: Ngũ hành của sao (`K`: Kim, `M`: Mộc, `T`: Thủy, `H`: Hỏa, `O`: Thổ).
  - `css_sao`: Tên class CSS đề xuất theo ngũ hành (`saoKim`, `saoMoc`, `saoThuy`, `saoHoa`, `saoTho`).
  - `dac_tinh`: Độ đắc hãm của sao:
    - `"M"`: Miếu địa
    - `"V"`: Vượng địa
    - `"Đ"`: Đắc địa
    - `"B"`: Bình hòa
    - `"H"`: Hãm địa
    - `null`: Không xét đắc hãm (các phụ tinh nhỏ).

---

## 4. Mã mẫu tích hợp nhanh (Copy-Paste)

### 4.1. JavaScript (Fetch API - Dùng cho React, Vue, Next.js, Web thuần)
```javascript
async function getLaSoTuVi() {
  const url = "https://api.hongngochuyenhoc.com/api/v1/laso";
  
  const payload = {
    ho_ten: "Nguyễn Văn A",
    ngay_sinh: 15,
    thang_sinh: 8,
    nam_sinh: 1990,
    gio_sinh: 10,
    phut_sinh: 30,
    gioi_tinh: 1,       // 1: Nam, -1: Nữ
    duong_lich: true     // true: Dương lịch, false: Âm lịch
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Lỗi:", errorData);
      return;
    }

    const data = await response.json();
    console.log("Thông tin Thiên Bàn:", data.thien_ban);
    console.log("Danh sách 12 Cung:", data.dia_ban);
    
    // Ví dụ: Tìm cung Mệnh
    const cungMenh = data.dia_ban.find(c => c.cung_chu === "Mệnh");
    console.log("Cung Mệnh tại:", cungMenh.ten_cung, "Chính tinh:", cungMenh.sao.filter(s => s.loai_sao === 1));

  } catch (err) {
    console.error("Lỗi kết nối mạng:", err);
  }
}

getLaSoTuVi();
```

---

### 4.2. cURL (Dùng test nhanh trên Terminal hoặc Postman)
```bash
curl -X POST "https://api.hongngochuyenhoc.com/api/v1/laso" \
     -H "Content-Type: application/json" \
     -d '{
       "ho_ten": "Trần Thị B",
       "ngay_sinh": 20,
       "thang_sinh": 11,
       "nam_sinh": 1995,
       "gio_sinh": 6,
       "phut_sinh": 15,
       "gioi_tinh": -1,
       "duong_lich": true
     }'
```

---

### 4.3. Python (Dùng cho Bot Telegram, Zalo hoặc Automation)
```python
import requests

url = "https://api.hongngochuyenhoc.com/api/v1/laso"

payload = {
    "ho_ten": "Lê Văn C",
    "ngay_sinh": 1,
    "thang_sinh": 5,
    "nam_sinh": 2000,
    "gio_sinh": 14,
    "phut_sinh": 0,
    "gioi_tinh": 1,
    "duong_lich": True
}

res = requests.post(url, json=payload)
if res.status_code == 200:
    data = res.json()
    print("Bản Mệnh:", data["thien_ban"]["ban_menh"])
    print("Cục:", data["thien_ban"]["ten_cuc"])
else:
    print("Lỗi:", res.status_code, res.text)
```

---

### 4.4. Flutter / Dart (Dành cho Mobile App iOS & Android)
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<void> fetchLaSo() async {
  final url = Uri.parse('https://api.hongngochuyenhoc.com/api/v1/laso');
  
  final response = await http.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'ho_ten': 'Phạm Hoàng D',
      'ngay_sinh': 9,
      'thang_sinh': 9,
      'nam_sinh': 1998,
      'gio_sinh': 8,
      'phut_sinh': 45,
      'gioi_tinh': 1,
      'duong_lich': true,
    }),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(utf8.decode(response.bodyBytes));
    print('Thiên Bàn: ${data['thien_ban']}');
  } else {
    print('Lỗi: ${response.statusCode}');
  }
}
```

---

## 5. Xử lý lỗi (Error Handling)

Khi truyền dữ liệu không hợp lệ (ví dụ: ngày 31 tháng 2, thiếu trường bắt buộc...), server sẽ trả về mã `HTTP 422 Unprocessable Entity` với cấu trúc thông báo bằng tiếng Việt rõ ràng:

```json
{
  "detail": "Dữ liệu yêu cầu không hợp lệ hoặc thiếu trường bắt buộc.",
  "errors": [
    {
      "field": "body -> ngay_sinh",
      "message": "Ngày sinh không hợp lệ cho tháng/năm đã chọn"
    }
  ]
}
```
Client chỉ cần kiểm tra `response.status === 422` để hiển thị cảnh báo tương ứng cho người dùng trên giao diện.

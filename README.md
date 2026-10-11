# Tử Vi Đẩu Số — Backend API (FastAPI)

Backend REST API phục vụ cho ứng dụng PWA xem lá số Tử Vi Đẩu Số, sử dụng FastAPI và Python, tích hợp engine an sao Tử Vi Đẩu Số thuần Việt (`lasotuvi`).

> 🚀 **HƯỚNG DẪN TÍCH HỢP & MÃ MẪU GỌI API:** Xem chi tiết tại [**`API_GUIDE.md`**](API_GUIDE.md)  
> 🌐 **Production API URL:** `https://api.hongngochuyenhoc.com` (Swagger UI: `https://api.hongngochuyenhoc.com/docs`)

---

## 1. Cấu trúc thư mục

```text
tuvidmt/
├── api/
│   ├── __init__.py
│   ├── models.py       # Pydantic Schemas (Request, Response, Validation)
│   ├── routes.py       # FastAPI Endpoints (/api/v1/health, /api/v1/laso)
│   └── service.py      # Business Logic: kiểm tra ngày, đổi giờ chi, gọi engine & serialize
├── lasotuvi/           # Engine Tử Vi Đẩu Số (đã chuẩn hóa package & cô lập trạng thái)
│   ├── __init__.py
│   ├── AmDuong.py
│   ├── App.py
│   ├── DiaBan.py
│   ├── Lich_HND.py
│   ├── Sao.py
│   └── ThienBan.py
├── tests/
│   ├── __init__.py
│   └── test_api.py     # 9 nhóm kiểm thử tự động toàn diện
├── Dockerfile          # Cấu hình container Python 3.11-slim
├── compose.yaml        # Docker Compose service backend
├── .dockerignore       # Loại trừ cache, venv, tests khi build image
├── main.py             # Entrypoint khởi tạo FastAPI App, CORS, Error Handlers
├── requirements.txt    # Danh sách dependency
└── NGUON_GOC.md        # Lịch sử audit & giấy phép MIT của engine
```

---

## 2. Hướng dẫn chạy ứng dụng

### 2.1. Chạy bằng Docker (Khuyên dùng trên Windows)

#### Build và khởi chạy container chạy nền:
```powershell
docker compose up --build -d
```

#### Xem trạng thái container và health check:
```powershell
docker compose ps
```

#### Xem log thời gian thực:
```powershell
docker compose logs -f
```

#### Dừng ứng dụng container:
```powershell
docker compose down
```

- **Health Check Endpoint:** `http://localhost:8000/api/v1/health`
- **Tài liệu Swagger UI tương tác:** `http://localhost:8000/docs`

---

### 2.2. Chạy trực tiếp trên máy Local (Không dùng Docker)

#### Cài đặt thư viện:
```powershell
pip install -r requirements.txt
```

#### Khởi chạy Uvicorn server:
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Chạy bộ kiểm thử tự động:
```powershell
pytest -v -s tests/test_api.py
```

---

## 3. Tài liệu Endpoints

### 3.1. Health Check
- **Endpoint:** `GET /api/v1/health`
- **Mô tả:** Kiểm tra trạng thái hoạt động của backend service, không tính toán lá số.
- **Phản hồi mẫu (200 OK):**
```json
{
  "status": "ok",
  "message": "Tu Vi Backend API is running",
  "version": "1.0.0"
}
```

---

### 3.2. Lập lá số Tử Vi
- **Endpoint:** `POST /api/v1/laso`
- **Content-Type:** `application/json`

#### Request Body Schema:
| Trường | Kiểu dữ liệu | Bắt buộc | Mặc định | Mô tả |
|---|---|---|---|---|
| `ho_ten` | string | Không | `"Vô danh"` | Họ và tên đương số |
| `ngay_sinh` | integer | **Có** | - | Ngày sinh (1 - 31) |
| `thang_sinh` | integer | **Có** | - | Tháng sinh (1 - 12) |
| `nam_sinh` | integer | **Có** | - | Năm sinh (1000 - 3000) |
| `gio_sinh` | integer | **Có** | - | Giờ sinh theo đồng hồ 24h (0 - 23) |
| `phut_sinh` | integer | Không | `0` | Phút sinh theo đồng hồ (0 - 59) |
| `gioi_tinh` | integer / string | **Có** | - | `1` / `"nam"`: Nam; `-1` / `"nu"`: Nữ |
| `duong_lich` | boolean | Không | `true` | `true`: Dương lịch, `false`: Âm lịch |
| `thang_nhuan` | boolean | Không | `false` | `true`: sinh vào tháng nhuận (chỉ dùng cho Âm lịch) |
| `mui_gio` | float | Không | `7.0` | Múi giờ địa phương (Việt Nam là +7.0) |

#### Request mẫu:
```json
{
  "ho_ten": "Nguyễn Văn A",
  "ngay_sinh": 15,
  "thang_sinh": 8,
  "nam_sinh": 1990,
  "gio_sinh": 11,
  "phut_sinh": 30,
  "gioi_tinh": 1,
  "duong_lich": true,
  "mui_gio": 7.0
}
```

#### Response mẫu (rút gọn):
```json
{
  "thien_ban": {
    "ho_ten": "Nguyễn Văn A",
    "gioi_tinh": 1,
    "nam_nu": "Nam",
    "ngay_duong": 15,
    "thang_duong": 8,
    "nam_duong": 1990,
    "ngay_am": 25,
    "thang_am": 6,
    "nam_am": 1990,
    "thang_nhuan": 0,
    "gio_sinh_can_chi": "Bính Ngọ",
    "can_gio_sinh": 3,
    "chi_gio_sinh": "Ngọ",
    "can_ngay": "Nhâm",
    "chi_ngay": "Tý",
    "can_thang": "Quý",
    "chi_thang": "Mùi",
    "can_nam": "Canh",
    "chi_nam": "Ngọ",
    "am_duong_nam_sinh": "Dương",
    "am_duong_menh": "Âm dương nghịch lý",
    "hanh_cuc": 4,
    "ten_cuc": "Hỏa lục Cục",
    "menh_chu": "Phá quân",
    "than_chu": "Linh tinh",
    "menh": "O",
    "ban_menh": "LỘ BÀN THỔ",
    "sinh_khac": "Cục sinh Bản mệnh",
    "mui_gio": 7.0
  },
  "dia_ban": [
    {
      "cung_so": 1,
      "ten_cung": "Tý",
      "cung_chu": "Huynh đệ",
      "hanh_cung": "Thủy",
      "am_duong": 1,
      "is_than": false,
      "dai_han": 116,
      "tieu_han": "Dần",
      "tuan": false,
      "triet": false,
      "sao": [
        {
          "sao_id": 6,
          "ten_sao": "Thiên cơ",
          "ngu_hanh": "M",
          "loai_sao": 1,
          "phuong_vi": "Nam đẩu tinh",
          "am_duong": -1,
          "vong_trang_sinh": 0,
          "css_sao": "hanhMoc",
          "dac_tinh": "Đ"
        }
      ]
    }
  ]
}
```

---

### 3.3. Mã mẫu gọi nhanh (Quickstart Snippets)

#### JavaScript / TypeScript (Web Frontend, React, Vue, Next.js):
```javascript
const res = await fetch("https://api.hongngochuyenhoc.com/api/v1/laso", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    ho_ten: "Nguyễn Văn A",
    ngay_sinh: 15,
    thang_sinh: 8,
    nam_sinh: 1990,
    gio_sinh: 11,
    phut_sinh: 30,
    gioi_tinh: 1,      // 1: Nam, -1: Nữ
    duong_lich: true    // true: Dương lịch, false: Âm lịch
  })
});
const data = await res.json();
console.log("Thiên Bàn:", data.thien_ban);
console.log("12 Cung Địa Bàn:", data.dia_ban);
```

#### cURL (Terminal / Postman):
```bash
curl -X POST "https://api.hongngochuyenhoc.com/api/v1/laso" \
     -H "Content-Type: application/json" \
     -d '{
       "ho_ten": "Nguyễn Văn A",
       "ngay_sinh": 15,
       "thang_sinh": 8,
       "nam_sinh": 1990,
       "gio_sinh": 11,
       "phut_sinh": 30,
       "gioi_tinh": 1,
       "duong_lich": true
     }'
```

#### Python:
```python
import requests

res = requests.post("https://api.hongngochuyenhoc.com/api/v1/laso", json={
    "ho_ten": "Nguyễn Văn A",
    "ngay_sinh": 15,
    "thang_sinh": 8,
    "nam_sinh": 1990,
    "gio_sinh": 11,
    "phut_sinh": 30,
    "gioi_tinh": 1,
    "duong_lich": True
})
data = res.json()
print("Bản Mệnh:", data["thien_ban"]["ban_menh"])
```

---

### 3.4. Ý nghĩa các trường dữ liệu quan trọng trong Output

| Trường | Vị trí | Ý nghĩa cho việc vẽ giao diện |
| :--- | :--- | :--- |
| `thien_ban.ban_menh` | Thiên Bàn | Tên ngũ hành nạp âm bản mệnh (ví dụ: `LỘ BÀN THỔ`) |
| `thien_ban.ten_cuc` | Thiên Bàn | Tên Cục (ví dụ: `Hỏa lục Cục`, `Thủy nhị Cục`...) |
| `dia_ban[].cung_chu` | Mỗi Cung | Tên cung chức (Mệnh, Phụ Mẫu, Phúc Đức, Điền Trạch, Quan Lộc...) |
| `dia_ban[].is_than` | Mỗi Cung | `true` nếu cung này là nơi **Thân cư** (ví dụ Thân cư Phu thê) |
| `dia_ban[].tuan` | Mỗi Cung | `true` nếu cung bị ảnh hưởng bởi sao **Tuần Không** |
| `dia_ban[].triet` | Mỗi Cung | `true` nếu cung bị ảnh hưởng bởi sao **Triệt Lộ** |
| `dia_ban[].sao[].dac_tinh` | Mỗi Sao | Độ đắc hãm: `M` (Miếu), `V` (Vượng), `Đ` (Đắc), `B` (Bình), `H` (Hãm) |
| `dia_ban[].sao[].css_sao` | Mỗi Sao | Class màu ngũ hành: `hanhKim`, `hanhMoc`, `hanhThuy`, `hanhHoa`, `hanhTho` |

---

## 4. Quy ước chuyển đổi giờ sinh và ranh giới giờ Tý


Trong chiêm tinh học phương Đông, một ngày gồm 12 canh giờ (Địa Chi), mỗi canh giờ tương ứng 2 tiếng đồng hồ.

### 4.1. Bảng quy đổi 24 mốc giờ sang 12 Chi:
| Giờ đồng hồ | Chi giờ | Tên Chi | Mã ID engine |
|---|---|---|---|
| **23:00 – 00:59** | 1 | **Tý** | `1` |
| 01:00 – 02:59 | 2 | Sửu | `2` |
| 03:00 – 04:59 | 3 | Dần | `3` |
| 05:00 – 06:59 | 4 | Mão | `4` |
| 07:00 – 08:59 | 5 | Thìn | `5` |
| 09:00 – 10:59 | 6 | Tỵ | `6` |
| 11:00 – 12:59 | 7 | Ngọ | `7` |
| 13:00 – 14:59 | 8 | Mùi | `8` |
| 15:00 – 16:59 | 9 | Thân | `9` |
| 17:00 – 18:59 | 10 | Dậu | `10` |
| 19:00 – 20:59 | 11 | Tuất | `11` |
| 21:00 – 22:59 | 12 | Hợi | `12` |

### 4.2. Quy ước kỹ thuật về ranh giới giờ Tý (23:00 – 01:00):
- **Phân định Chi:** Toàn bộ khoảng thời gian từ `23:00` đến `00:59` được tính là **Giờ Tý** (`gioSinh = 1`).
- **Xử lý ngày:** Ngày sinh được giữ nguyên theo ngày hành chính mà người dùng nhập vào. Engine không tự động dịch chuyển ngày (không cộng thêm 1 ngày khi sinh lúc 23h–23h59) nhằm:
  1. Bảo toàn nguyên tắc không thay đổi ngày của engine gốc `lasotuvi`.
  2. Phù hợp với thói quen của người dùng thông thường khi nhập ngày tháng sinh từ giấy tờ tùy thân.
  3. Tránh việc âm thầm sửa đổi ngày dẫn đến hiểu lầm cho người dùng.

---

## 5. Xử lý lỗi và tính an toàn

- **Lỗi thiếu trường hoặc sai kiểu dữ liệu:** Trả về `HTTP 422 Unprocessable Entity` với danh sách các trường lỗi rõ ràng.
- **Lỗi ngày không tồn tại:** 
  - Dương lịch: Các ngày như 31/02, 29/02 năm thường, 31/04... bị từ chối với `HTTP 422` kèm thông báo chi tiết.
  - Âm lịch: Các ngày vượt quá 30, hoặc ngày 30 trong tháng thiếu (29 ngày), hoặc tháng nhuận không tồn tại trong năm đó bị từ chối với `HTTP 422`.
- **An toàn bảo mật:** Các ngoại lệ nội bộ không mong muốn được ghi log chi tiết trên server và trả về `HTTP 500` thông báo chung, tuyệt đối không để lộ traceback hệ thống hay đường dẫn file ra ngoài client.

---

## 6. Hướng dẫn triển khai VPS qua Dockge

[Dockge](https://dockge.kuma.pet/) là trình quản lý Docker Compose trực quan, hiện đại, rất phù hợp để quản trị stack backend Tử Vi trên VPS Linux. Dự án hỗ trợ 2 phương pháp triển khai:

---

### Phương pháp 1 (Khuyên dùng): Triển khai qua Image đóng gói sẵn trên GHCR
*(Không cần SSH vào VPS, không cần clone repo, không tiêu tốn RAM/CPU của VPS để build)*

Image được tự động build và push lên GitHub Container Registry (`ghcr.io/dangtrandang/tuvidmt`) qua GitHub Actions mỗi khi có commit trên nhánh `master`.

#### Các bước thực hiện trên Web UI của Dockge:
1. Mở giao diện web của Dockge (`http://<ip-vps>:5001`).
2. Bấm nút **"Compose"** (Tạo Stack mới).
3. Đặt **Stack Name**: `tuvidmt`.
4. Dán nội dung file [`dockge-compose.yaml`](dockge-compose.yaml) vào khung soạn thảo Compose bên trái:
   ```yaml
   services:
     backend:
       image: ghcr.io/dangtrandang/tuvidmt:${TAG:-latest}
       container_name: tuvi-backend
       restart: unless-stopped
       ports:
         - "${HOST_PORT:-127.0.0.1:8000}:8000"
       environment:
         - PORT=8000
       healthcheck:
         test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health')"]
         interval: 15s
         timeout: 5s
         retries: 3
         start_period: 5s
   ```
5. Trong khung biến môi trường **.env** bên phải, cấu hình:
   ```env
   HOST_PORT=127.0.0.1:8000
   TAG=latest
   ```
6. Bấm nút **"Deploy"**. Dockge sẽ tự động pull image từ GHCR và khởi chạy container trong vài giây.

> [!NOTE]
> **Quyền truy cập GHCR Package:**
> - Mặc định khi GitHub Actions publish package lần đầu, package có thể ở chế độ *Private*.
> - Để Dockge pull image mà không cần xác thực: Vào repo GitHub -> **Packages** -> chọn `tuvidmt` -> **Package settings** -> cuộn xuống **Danger Zone** và chuyển sang **Public**.
> - Nếu muốn giữ Private: SSH vào VPS chạy `docker login ghcr.io -u <github-username> -p <personal-access-token>` một lần duy nhất.

---

### Phương pháp 2: Build trực tiếp từ mã nguồn trên VPS

Dành cho trường hợp bạn muốn clone mã nguồn và tự build trên VPS.

1. Đăng nhập SSH vào VPS và chuyển tới thư mục stacks của Dockge (ví dụ `/opt/stacks`):
   ```bash
   cd /opt/stacks
   git clone https://github.com/dangtrandang/tuvidmt.git tuvidmt
   cd tuvidmt
   cp .env.example .env
   ```
2. Mở giao diện Dockge, stack `tuvidmt` sẽ tự động hiển thị trong danh sách.
3. Bấm **"Deploy"** để Dockge tiến hành build và chạy container.

---

### 6.2. Cấu hình bảo mật mạng với `HOST_PORT`
- **Cơ chế hoạt động:** Cấu hình `HOST_PORT=127.0.0.1:8000` ánh xạ container vào `127.0.0.1:8000:8000`.
- **Lợi ích an toàn:** Container chỉ lắng nghe duy nhất trên giao diện loopback nội bộ của VPS (`127.0.0.1`), **tuyệt đối không mở cổng 8000 ra Internet**.
- **Kết nối Domain / SSL:** Sử dụng Reverse Proxy (Nginx, Caddy, Nginx Proxy Manager) hoặc Cloudflare Tunnel trên VPS để trỏ tên miền (ví dụ: `https://api.tuvi.yourdomain.com`) chuyển tiếp an toàn vào `http://127.0.0.1:8000`.

### 6.3. Kiểm tra sức khỏe và Rollback
- **Kiểm tra trạng thái:** Container `tuvi-backend` hiển thị badge màu xanh lá **`healthy`**.
- **Kiểm tra từ terminal VPS:**
  ```bash
  curl http://127.0.0.1:8000/api/v1/health
  ```
- **Cập nhật phiên bản:** Khi có bản cập nhật mới trên GitHub, trong giao diện Dockge chỉ cần bấm **"Update"** (hoặc pull tag mới) rồi bấm **"Deploy"**.
- **Rollback:** Đổi biến `TAG=<commit_sha>` trong khung `.env` của Dockge (ví dụ `TAG=sha-9f3d76a`) và bấm **"Deploy"** để quay về phiên bản mong muốn.



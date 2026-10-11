# -*- coding: utf-8 -*-
"""
Bộ kiểm thử tự động toàn diện cho FastAPI Backend Tử Vi Đẩu Số.
Bao gồm 9 nhóm kiểm thử bắt buộc theo đặc tả kỹ thuật.
"""
import json
import os
import subprocess
import sys
import pytest
from fastapi.testclient import TestClient

from main import app
from api.service import convert_time_to_chi

client = TestClient(app)


# ============================================================================
# KIỂM THỬ 1: Health Check Endpoint
# ============================================================================
def test_01_health_check():
    """Kiểm tra GET /api/v1/health hoạt động bình thường, trả về 200."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "message" in data


# ============================================================================
# KIỂM THỬ 2: Lập lá số Dương lịch hợp lệ
# ============================================================================
def test_02_valid_solar_chart():
    """Kiểm tra POST /api/v1/laso với ngày sinh Dương lịch chuẩn."""
    payload = {
        "ho_ten": "Nguyễn Văn A",
        "ngay_sinh": 15,
        "thang_sinh": 8,
        "nam_sinh": 1990,
        "gio_sinh": 11,
        "phut_sinh": 30,
        "gioi_tinh": 1,
        "duong_lich": True,
        "mui_gio": 7.0
    }
    response = client.post("/api/v1/laso", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Kiểm tra cấu trúc cấp cao
    assert "thien_ban" in data
    assert "dia_ban" in data

    # Kiểm tra thông tin Thiên Bàn
    tb = data["thien_ban"]
    assert tb["ho_ten"] == "Nguyễn Văn A"
    assert tb["nam_nu"] == "Nam"
    assert tb["ngay_duong"] == 15
    assert tb["thang_duong"] == 8
    assert tb["nam_duong"] == 1990
    assert tb["can_nam"] == "Canh"
    assert tb["chi_nam"] == "Ngọ"
    assert tb["ban_menh"] == "LỘ BÀN THỔ"
    assert "ten_cuc" in tb
    assert "menh_chu" in tb
    assert "than_chu" in tb


# ============================================================================
# KIỂM THỬ 3: Lập lá số Âm lịch hợp lệ
# ============================================================================
def test_03_valid_lunar_chart():
    """Kiểm tra POST /api/v1/laso với ngày sinh Âm lịch chuẩn."""
    payload = {
        "ho_ten": "Trần Thị B",
        "ngay_sinh": 25,
        "thang_sinh": 6,
        "nam_sinh": 1990,
        "gio_sinh": 7,
        "phut_sinh": 15,
        "gioi_tinh": -1,
        "duong_lich": False,
        "mui_gio": 7.0
    }
    response = client.post("/api/v1/laso", json=payload)
    assert response.status_code == 200
    data = response.json()

    tb = data["thien_ban"]
    assert tb["ho_ten"] == "Trần Thị B"
    assert tb["nam_nu"] == "Nữ"
    assert tb["ngay_am"] == 25
    assert tb["thang_am"] == 6
    assert tb["nam_am"] == 1990
    assert tb["can_nam"] == "Canh"
    assert tb["chi_nam"] == "Ngọ"
    assert len(data["dia_ban"]) == 12


# ============================================================================
# KIỂM THỬ 4: Từ chối ngày không hợp lệ (31/02, 29/02 năm thường...)
# ============================================================================
def test_04_invalid_dates_rejected():
    """Kiểm tra API từ chối các ngày không tồn tại với mã HTTP 422."""
    # 4.1: Ngày 31/02 Dương lịch
    res1 = client.post("/api/v1/laso", json={
        "ho_ten": "Test 31/02",
        "ngay_sinh": 31,
        "thang_sinh": 2,
        "nam_sinh": 1990,
        "gio_sinh": 8,
        "phut_sinh": 0,
        "gioi_tinh": 1,
        "duong_lich": True
    })
    assert res1.status_code == 422
    assert "không hợp lệ" in res1.json()["detail"].lower()

    # 4.2: Ngày 29/02 năm không nhuận (1991)
    res2 = client.post("/api/v1/laso", json={
        "ho_ten": "Test 29/02 không nhuận",
        "ngay_sinh": 29,
        "thang_sinh": 2,
        "nam_sinh": 1991,
        "gio_sinh": 8,
        "phut_sinh": 0,
        "gioi_tinh": 1,
        "duong_lich": True
    })
    assert res2.status_code == 422

    # 4.3: Ngày 31 tháng 4 (tháng 4 chỉ có 30 ngày)
    res3 = client.post("/api/v1/laso", json={
        "ho_ten": "Test 31/04",
        "ngay_sinh": 31,
        "thang_sinh": 4,
        "nam_sinh": 1990,
        "gio_sinh": 8,
        "phut_sinh": 0,
        "gioi_tinh": 1,
        "duong_lich": True
    })
    assert res3.status_code == 422

    # 4.4: Ngày 30 tháng âm thiếu (tháng 8 âm năm 1990 chỉ có 29 ngày)
    res4 = client.post("/api/v1/laso", json={
        "ho_ten": "Test âm lịch thiếu",
        "ngay_sinh": 30,
        "thang_sinh": 8,
        "nam_sinh": 1990,
        "gio_sinh": 8,
        "phut_sinh": 0,
        "gioi_tinh": 1,
        "duong_lich": False
    })
    assert res4.status_code == 422


# ============================================================================
# KIỂM THỬ 5: Từ chối khi thiếu trường bắt buộc
# ============================================================================
def test_05_missing_required_fields():
    """Kiểm tra API trả về 422 khi thiếu bất kỳ trường bắt buộc nào."""
    # Thiếu ngày sinh
    res1 = client.post("/api/v1/laso", json={
        "thang_sinh": 8,
        "nam_sinh": 1990,
        "gio_sinh": 10,
        "gioi_tinh": 1
    })
    assert res1.status_code == 422

    # Thiếu năm sinh
    res2 = client.post("/api/v1/laso", json={
        "ngay_sinh": 15,
        "thang_sinh": 8,
        "gio_sinh": 10,
        "gioi_tinh": 1
    })
    assert res2.status_code == 422

    # Thiếu giới tính
    res3 = client.post("/api/v1/laso", json={
        "ngay_sinh": 15,
        "thang_sinh": 8,
        "nam_sinh": 1990,
        "gio_sinh": 10
    })
    assert res3.status_code == 422


# ============================================================================
# KIỂM THỬ 6: Địa Bàn luôn có đúng 12 cung, không chứa cung giả index 0
# ============================================================================
def test_06_exactly_12_palaces_no_dummy():
    """Kiểm tra Địa Bàn luôn có đúng 12 phần tử và cung_so từ 1 đến 12."""
    res = client.post("/api/v1/laso", json={
        "ngay_sinh": 10,
        "thang_sinh": 5,
        "nam_sinh": 1995,
        "gio_sinh": 14,
        "phut_sinh": 20,
        "gioi_tinh": 1,
        "duong_lich": True
    })
    assert res.status_code == 200
    dia_ban = res.json()["dia_ban"]

    # Phải có chính xác 12 cung
    assert len(dia_ban) == 12

    # Thứ tự cung_so phải từ 1 đến 12 liên tục
    cung_so_list = [c["cung_so"] for c in dia_ban]
    assert cung_so_list == list(range(1, 13))

    # Không có bất kỳ cung nào có tên "Hem có" hoặc cung_so == 0
    ten_cung_list = [c["ten_cung"] for c in dia_ban]
    assert "Hem có" not in ten_cung_list
    assert 0 not in cung_so_list

    # 12 cung phải là 12 Địa Chi theo đúng thứ tự Tý đến Hợi
    expected_chi = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    assert ten_cung_list == expected_chi


# ============================================================================
# KIỂM THỬ 7: Thuộc tính Tuần và Triệt luôn là boolean chuẩn
# ============================================================================
def test_07_tuan_triet_always_boolean():
    """Kiểm tra mọi cung trong Địa Bàn đều có tuan và triet là kiểu bool."""
    res = client.post("/api/v1/laso", json={
        "ngay_sinh": 24,
        "thang_sinh": 2,
        "nam_sinh": 1995,
        "gio_sinh": 6,
        "phut_sinh": 45,
        "gioi_tinh": -1,
        "duong_lich": True
    })
    assert res.status_code == 200
    dia_ban = res.json()["dia_ban"]

    count_tuan = 0
    count_triet = 0
    for c in dia_ban:
        # Kiểu dữ liệu phải là bool
        assert isinstance(c["tuan"], bool)
        assert isinstance(c["triet"], bool)
        if c["tuan"] is True:
            count_tuan += 1
        if c["triet"] is True:
            count_triet += 1

    # Trong Tử Vi, Tuần Không luôn đóng ở 2 cung, Triệt Lộ luôn đóng ở 2 cung
    assert count_tuan == 2, f"Kỳ vọng 2 cung có Tuần, thực tế: {count_tuan}"
    assert count_triet == 2, f"Kỳ vọng 2 cung có Triệt, thực tế: {count_triet}"


# ============================================================================
# KIỂM THỬ 8: Lập liên tiếp 2 lá số vs Chạy độc lập (Chống rò rỉ trạng thái)
# ============================================================================
def test_08_no_state_leakage_between_consecutive_calls():
    """
    Lập liên tiếp hai lá số trong cùng tiến trình (Lá 1 -> Lá 2),
    so sánh kết quả Lá 2 với việc chạy Lá 2 trong tiến trình mới hoàn toàn.
    Đảm bảo 100% sao không bị rò rỉ hoặc nhiễm chéo đặc tính.
    """
    payload_1 = {
        "ho_ten": "Người 1 (1990)",
        "ngay_sinh": 15,
        "thang_sinh": 8,
        "nam_sinh": 1990,
        "gio_sinh": 11,
        "phut_sinh": 30,
        "gioi_tinh": 1,
        "duong_lich": True
    }
    payload_2 = {
        "ho_ten": "Người 2 (1995)",
        "ngay_sinh": 24,
        "thang_sinh": 2,
        "nam_sinh": 1995,
        "gio_sinh": 3,
        "phut_sinh": 10,
        "gioi_tinh": -1,
        "duong_lich": True
    }

    # 1. Gọi liên tiếp trên cùng tiến trình
    res1 = client.post("/api/v1/laso", json=payload_1)
    assert res1.status_code == 200

    res2_consecutive = client.post("/api/v1/laso", json=payload_2)
    assert res2_consecutive.status_code == 200
    data2_consec = res2_consecutive.json()

    # 2. Gọi Lá 2 trong một process hoàn toàn mới độc lập
    payload_json = json.dumps(payload_2)
    sub_script = f"""
import json, sys, os
sys.path.insert(0, os.path.abspath('.'))
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
payload = json.loads({repr(payload_json)})
res = client.post('/api/v1/laso', json=payload)
print(json.dumps(res.json(), ensure_ascii=False))
"""
    proc = subprocess.run(
        [sys.executable, "-X", "utf8", "-c", sub_script],
        capture_output=True,
        encoding="utf-8",
        cwd=os.path.abspath(".")
    )
    assert proc.returncode == 0, f"Subprocess failed: {proc.stderr}"
    data2_fresh = json.loads(proc.stdout)

    # 3. So sánh đối chiếu toàn diện giữa 2 kết quả
    # So sánh Thiên Bàn
    assert data2_consec["thien_ban"] == data2_fresh["thien_ban"]

    # So sánh từng cung và từng sao trong Địa Bàn
    for i in range(12):
        cung_consec = data2_consec["dia_ban"][i]
        cung_fresh = data2_fresh["dia_ban"][i]

        assert cung_consec["cung_so"] == cung_fresh["cung_so"]
        assert cung_consec["ten_cung"] == cung_fresh["ten_cung"]
        assert cung_consec["cung_chu"] == cung_fresh["cung_chu"]
        assert cung_consec["tuan"] == cung_fresh["tuan"]
        assert cung_consec["triet"] == cung_fresh["triet"]

        sao_consec = {s["sao_id"]: s for s in cung_consec["sao"]}
        sao_fresh = {s["sao_id"]: s for s in cung_fresh["sao"]}

        assert len(sao_consec) == len(sao_fresh)
        for sid, sf in sao_fresh.items():
            sc = sao_consec[sid]
            assert sc["dac_tinh"] == sf["dac_tinh"], (
                f"LỆCH ĐẶC TÍNH: Sao {sf['ten_sao']} (ID {sid}) tại cung {cung_consec['ten_cung']}: "
                f"Consecutive={sc['dac_tinh']} vs Fresh={sf['dac_tinh']}"
            )


# ============================================================================
# KIỂM THỬ 9: Quy tắc chuyển giờ sinh và các mốc ranh giới (bao gồm 23h-01h Tý)
# ============================================================================
def test_09_hour_conversion_rules():
    """
    Kiểm tra thuật toán convert_time_to_chi() trên toàn bộ 24 mốc giờ
    và các ranh giới giao canh (01:00, 03:00, ..., 23:00).
    """
    # 9.1: Kiểm tra 12 khung giờ chi chuẩn
    test_cases = [
        # Giờ Tý (23:00 - 00:59): chi = 1
        (23, 0, 1),
        (23, 30, 1),
        (23, 59, 1),
        (0, 0, 1),
        (0, 30, 1),
        (0, 59, 1),

        # Giờ Sửu (01:00 - 02:59): chi = 2
        (1, 0, 2),
        (1, 30, 2),
        (2, 59, 2),

        # Giờ Dần (03:00 - 04:59): chi = 3
        (3, 0, 3),
        (4, 30, 3),

        # Giờ Mão (05:00 - 06:59): chi = 4
        (5, 0, 4),
        (6, 45, 4),

        # Giờ Thìn (07:00 - 08:59): chi = 5
        (7, 0, 5),
        (8, 15, 5),

        # Giờ Tỵ (09:00 - 10:59): chi = 6
        (9, 0, 6),
        (10, 50, 6),

        # Giờ Ngọ (11:00 - 12:59): chi = 7
        (11, 0, 7),
        (12, 30, 7),

        # Giờ Mùi (13:00 - 14:59): chi = 8
        (13, 0, 8),
        (14, 59, 8),

        # Giờ Thân (15:00 - 16:59): chi = 9
        (15, 0, 9),
        (16, 20, 9),

        # Giờ Dậu (17:00 - 18:59): chi = 10
        (17, 0, 10),
        (18, 59, 10),

        # Giờ Tuất (19:00 - 20:59): chi = 11
        (19, 0, 11),
        (20, 30, 11),

        # Giờ Hợi (21:00 - 22:59): chi = 12
        (21, 0, 12),
        (22, 59, 12),
    ]

    for h, m, expected_chi in test_cases:
        actual_chi = convert_time_to_chi(h, m)
        assert actual_chi == expected_chi, f"Sai tại {h:02d}:{m:02d}: Kỳ vọng chi={expected_chi}, thực tế={actual_chi}"

    # 9.2: Kiểm tra bắt lỗi giờ/phút ngoài phạm vi 24h
    with pytest.raises(ValueError):
        convert_time_to_chi(24, 0)

    with pytest.raises(ValueError):
        convert_time_to_chi(-1, 0)

    with pytest.raises(ValueError):
        convert_time_to_chi(12, 60)

    with pytest.raises(ValueError):
        convert_time_to_chi(12, -5)

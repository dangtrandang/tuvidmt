# -*- coding: utf-8 -*-
"""
Business logic và Service chuyển đổi cho API Tử Vi.
"""
import datetime
from typing import List, Tuple

from lasotuvi import lapDiaBan, lapThienBan, diaBan
from lasotuvi.Lich_HND import L2S, S2L
from api.models import LaSoRequest, LaSoResponse, ThienBanModel, CungModel, SaoModel


def convert_time_to_chi(hour: int, minute: int = 0) -> int:
    """
    Quy đổi giờ:phút (00:00 - 23:59) sang Chi giờ (1..12 theo quy ước của engine):
    1:  Tý    (23:00 - 00:59)
    2:  Sửu   (01:00 - 02:59)
    3:  Dần   (03:00 - 04:59)
    4:  Mão   (05:00 - 06:59)
    5:  Thìn  (07:00 - 08:59)
    6:  Tỵ    (09:00 - 10:59)
    7:  Ngọ   (11:00 - 12:59)
    8:  Mùi   (13:00 - 14:59)
    9:  Thân  (15:00 - 16:59)
    10: Dậu   (17:00 - 18:59)
    11: Tuất  (19:00 - 20:59)
    12: Hợi   (21:00 - 22:59)

    Quy ước ranh giới giờ Tý (23:00 - 01:00):
    - Khung giờ từ 23:00 đến 00:59 được tính là Giờ Tý (chi = 1).
    - Ngày sinh giữ nguyên theo ngày khai sinh / nhập vào của người dùng,
      không tự ý cộng/trừ ngày để bảo toàn tính nhất quán với engine lasotuvi.
    """
    if not (0 <= hour <= 23):
        raise ValueError(f"Giờ sinh không hợp lệ: {hour} (phải từ 0 đến 23).")
    if not (0 <= minute <= 59):
        raise ValueError(f"Phút sinh không hợp lệ: {minute} (phải từ 0 đến 59).")

    # Thuật toán chuyển đổi: ((hour + 1) // 2) % 12 + 1
    # 23h, 00h -> (24//2)%12 + 1 = 1 (Tý); (1//2)%12 + 1 = 1 (Tý)
    # 01h, 02h -> (2//2)%12 + 1 = 2 (Sửu); (3//2)%12 + 1 = 2 (Sửu)
    chi = ((hour + 1) // 2) % 12 + 1
    return chi


def validate_date(ngay: int, thang: int, nam: int, duong_lich: bool, thang_nhuan: bool = False, mui_gio: float = 7.0) -> None:
    """
    Xác thực tính hợp lệ của ngày tháng năm sinh (Dương lịch hoặc Âm lịch).
    Từ chối các ngày không tồn tại (ví dụ: 31/02, 29/02 năm không nhuận, tháng âm thiếu).
    """
    if not (1000 <= nam <= 3000):
        raise ValueError(f"Năm sinh {nam} không nằm trong khoảng hợp lệ (1000 - 3000).")
    if not (1 <= thang <= 12):
        raise ValueError(f"Tháng sinh {thang} không hợp lệ (phải từ 1 đến 12).")

    if duong_lich:
        try:
            datetime.date(nam, thang, ngay)
        except ValueError:
            raise ValueError(f"Ngày dương lịch không hợp lệ: Ngày {ngay:02d}/{thang:02d}/{nam} không tồn tại trong lịch Gregorian.")
    else:
        # Kiểm tra ngày âm lịch
        if not (1 <= ngay <= 30):
            raise ValueError(f"Ngày âm lịch không hợp lệ: {ngay} (tháng âm lịch chỉ có từ 1 đến 30 ngày).")

        # Quy đổi sang dương lịch để kiểm tra ngày âm có thực sự tồn tại
        solar = L2S(ngay, thang, nam, 1 if thang_nhuan else 0, mui_gio)
        if not solar or solar == [0, 0, 0] or solar[0] == 0:
            if thang_nhuan:
                raise ValueError(f"Năm {nam} âm lịch không có tháng {thang} nhuận.")
            raise ValueError(f"Ngày âm lịch {ngay:02d}/{thang:02d}/{nam} không tồn tại.")

        # Kiểm tra đối xứng: đổi ngược solar sang âm lịch để xác minh tháng đủ/thiếu
        lunar_back = S2L(solar[0], solar[1], solar[2], mui_gio)
        if lunar_back[0] != ngay or lunar_back[1] != thang or lunar_back[2] != nam:
            raise ValueError(f"Tháng {thang} âm lịch năm {nam} không có ngày {ngay} (tháng thiếu chỉ có 29 ngày).")


def generate_laso(req: LaSoRequest) -> LaSoResponse:
    """
    Tiếp nhận request, validate, gọi engine lasotuvi và serialize response chuẩn hóa.
    """
    # 1. Kiểm tra tính hợp lệ của ngày tháng năm
    validate_date(
        ngay=req.ngay_sinh,
        thang=req.thang_sinh,
        nam=req.nam_sinh,
        duong_lich=req.duong_lich,
        thang_nhuan=req.thang_nhuan,
        mui_gio=req.mui_gio
    )

    # 2. Quy đổi giờ phút sang Chi giờ sinh (1..12)
    gio_chi = convert_time_to_chi(req.gio_sinh, req.phut_sinh)

    # 3. Gọi engine lập Địa Bàn
    db = lapDiaBan(
        diaBan=diaBan,
        nn=req.ngay_sinh,
        tt=req.thang_sinh,
        nnnn=req.nam_sinh,
        gioSinh=gio_chi,
        gioiTinh=req.gioi_tinh,
        duongLich=req.duong_lich,
        timeZone=req.mui_gio
    )

    # 4. Gọi engine lập Thiên Bàn
    tb = lapThienBan(
        nn=req.ngay_sinh,
        tt=req.thang_sinh,
        nnnn=req.nam_sinh,
        gioSinh=gio_chi,
        gioiTinh=req.gioi_tinh,
        ten=req.ho_ten,
        diaBan=db,
        duongLich=req.duong_lich,
        timeZone=req.mui_gio
    )

    # 5. Serialize Địa Bàn: Lấy đúng 12 cung (thapNhiCung[1:13]), loại bỏ hoàn toàn index 0
    dia_ban_list: List[CungModel] = []
    for c in db.thapNhiCung[1:13]:
        sao_list: List[SaoModel] = []
        for s in c.cungSao:
            sao_list.append(
                SaoModel(
                    sao_id=s["saoID"],
                    ten_sao=s["saoTen"],
                    ngu_hanh=s["saoNguHanh"],
                    loai_sao=s["saoLoai"],
                    phuong_vi=s.get("saoPhuongVi", ""),
                    am_duong=s.get("saoAmDuong", ""),
                    vong_trang_sinh=s.get("vongTrangSinh", 0),
                    css_sao=s.get("cssSao", ""),
                    dac_tinh=s.get("saoDacTinh", None)
                )
            )

        cung_model = CungModel(
            cung_so=c.cungSo,
            ten_cung=c.cungTen,
            cung_chu=c.cungChu,
            hanh_cung=c.hanhCung,
            am_duong=c.cungAmDuong,
            is_than=bool(c.cungThan),
            dai_han=c.cungDaiHan,
            tieu_han=c.cungTieuHan,
            tuan=bool(getattr(c, "tuanTrung", False)),
            triet=bool(getattr(c, "trietLo", False)),
            sao=sao_list
        )
        dia_ban_list.append(cung_model)

    # 6. Serialize Thiên Bàn
    chi_gio_ten = tb.chiGioSinh["tenChi"] if isinstance(tb.chiGioSinh, dict) else str(tb.chiGioSinh)
    thien_ban_model = ThienBanModel(
        ho_ten=tb.ten,
        gioi_tinh=tb.gioiTinh,
        nam_nu=tb.namNu,
        ngay_duong=tb.ngayDuong,
        thang_duong=tb.thangDuong,
        nam_duong=tb.namDuong,
        ngay_am=tb.ngayAm,
        thang_am=tb.thangAm,
        nam_am=tb.namAm,
        thang_nhuan=getattr(tb, "thangNhuan", 1 if req.thang_nhuan else 0),
        gio_sinh_can_chi=tb.gioSinh,
        can_gio_sinh=tb.canGioSinh,
        chi_gio_sinh=chi_gio_ten,
        can_ngay=tb.canNgayTen,
        chi_ngay=tb.chiNgayTen,
        can_thang=tb.canThangTen,
        chi_thang=tb.chiThangTen,
        can_nam=tb.canNamTen,
        chi_nam=tb.chiNamTen,
        am_duong_nam_sinh=tb.amDuongNamSinh,
        am_duong_menh=tb.amDuongMenh,
        hanh_cuc=tb.hanhCuc,
        ten_cuc=tb.tenCuc,
        menh_chu=tb.menhChu,
        than_chu=tb.thanChu,
        menh=tb.menh,
        ban_menh=tb.banMenh,
        sinh_khac=tb.sinhKhac,
        mui_gio=float(tb.timeZone)
    )

    return LaSoResponse(
        thien_ban=thien_ban_model,
        dia_ban=dia_ban_list
    )

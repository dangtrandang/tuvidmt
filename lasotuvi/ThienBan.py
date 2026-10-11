# -*- coding: utf-8 -*-
"""
(c) 2016 doanguyen <dungnv2410@gmail.com>.
"""
from lasotuvi.AmDuong import (canChiNgay, diaChi, ngayThangNam, ngayThangNamCanChi,
                     nguHanh, nguHanhNapAm, thienCan, timCuc, sinhKhac)
import time
from lasotuvi.Lich_HND import jdFromDate


class lapThienBan(object):
    def __init__(self, nn, tt, nnnn, gioSinh, gioiTinh, ten, diaBan,
                 duongLich=True, timeZone=7):
        super(lapThienBan, self).__init__()
        self.gioiTinh = 1 if gioiTinh == 1 else -1
        self.namNu = "Nam" if gioiTinh == 1 else "Nữ"

        chiGioSinh = diaChi[gioSinh]
        canGioSinh = ((jdFromDate(nn, tt, nnnn) - 1) * 2 % 10 + gioSinh) % 10
        if canGioSinh == 0:
            canGioSinh = 10
        self.chiGioSinh = chiGioSinh
        self.canGioSinh = canGioSinh
        self.gioSinh = "{} {}".format(thienCan[canGioSinh]['tenCan'],
                                      chiGioSinh['tenChi'])

        self.timeZone = timeZone
        self.today = time.strftime("%d/%m/%Y")
        self.ngayDuong, self.thangDuong, self.namDuong, self.ten = \
            nn, tt, nnnn, ten
        if duongLich is True:
            self.ngayAm, self.thangAm, self.namAm, self.thangNhuan = \
                ngayThangNam(self.ngayDuong, self.thangDuong, self.namDuong,
                             True, self.timeZone)
        else:
            self.ngayAm, self.thangAm, self.namAm = self.ngayDuong,\
                self.thangDuong, self.namDuong

        self.canThang, self.canNam, self.chiNam = \
            ngayThangNamCanChi(self.ngayAm, self.thangAm,
                               self.namAm, False, self.timeZone)
        # [TLCT 2026-08-03] Bản gốc gán thẳng self.thangAm (1-12) làm index
        # vào diaChi (1=Tý,2=Sửu,3=Dần...) — SAI, coi tháng 1 âm lịch là Tý.
        # Chi tháng phải theo "kiến nguyệt" (tháng Giêng luôn là Dần), khớp
        # công thức đã dùng đúng ở run_bazi/_tinh_truc trong engine.py:
        # chi_thang_idx(0-based, Tý=0) = (thangAm+1) % 12 → quy sang index
        # 1-based của diaChi (Tý=1) là +1. Verify: mùng 1 Tết Giáp Thìn
        # 2024-02-10 và Ất Tỵ 2025-01-29 khớp "Bính Dần"/"Mậu Dần" (2 nguồn
        # độc lập: thitruongtaichinhtiente.vn, sites.google.com/site/
        # huynhhieunghia0206), thay vì "...Tý" như bản gốc.
        self.chiThang = ((self.thangAm + 1) % 12) + 1
        self.canThangTen = thienCan[self.canThang]['tenCan']
        self.canNamTen = thienCan[self.canNam]['tenCan']
        self.chiThangTen = diaChi[self.chiThang]['tenChi']
        self.chiNamTen = diaChi[self.chiNam]['tenChi']

        self.canNgay, self.chiNgay = canChiNgay(
            self.ngayDuong, self.thangDuong, self.namDuong,
            duongLich, timeZone)
        self.canNgayTen = thienCan[self.canNgay]['tenCan']
        self.chiNgayTen = diaChi[self.chiNgay]['tenChi']

        cungAmDuong = 1 if (diaBan.cungMenh % 2 == 1) else -1
        self.amDuongNamSinh = "Dương" if (self.chiNam % 2 == 1) else "Âm"
        if (cungAmDuong * self.gioiTinh == 1):
            self.amDuongMenh = "Âm dương thuận lý"
        else:
            self.amDuongMenh = "Âm dương nghịch lý"

        cuc = timCuc(diaBan.cungMenh, self.canNam)
        self.hanhCuc = nguHanh(cuc)['id']
        self.tenCuc = nguHanh(cuc)['tenCuc']

        # [TLCT 2026-07-03] Bản gốc tra diaChi[canNam] — SAI: can (1-10) index
        # vào bảng địa chi (1-12). Mệnh chủ/Thân chủ an theo CHI năm sinh.
        # TODO đối chiếu: xem-tuvi.com hiện "Chủ Mệnh Văn xương" cho năm Dậu
        # (bảng phổ thông = Văn khúc) — vùng "3 thuyết" mơ hồ, cần thêm lá số
        # mẫu để chốt; tạm theo bảng phổ thông (Tham-Cự-Lộc-Văn-Liêm-Vũ-Phá).
        self.menhChu = diaChi[self.chiNam]['menhChu']
        self.thanChu = diaChi[self.chiNam]['thanChu']

        self.menh = nguHanhNapAm(self.chiNam, self.canNam)
        menhId = nguHanh(self.menh)['id']
        menhCuc = sinhKhac(menhId, self.hanhCuc)
        if menhCuc == 1:
            self.sinhKhac = "Bản Mệnh sinh Cục"
        elif menhCuc == -1:
            self.sinhKhac = "Bản Mệnh khắc Cục"
        elif menhCuc == -1j:
            self.sinhKhac = "Cục khắc Bản Mệnh"
        elif menhCuc == 1j:
            self.sinhKhac = "Cục sinh Bản mệnh"
        else:
            self.sinhKhac = "Cục hòa Bản Mệnh"

        self.banMenh = nguHanhNapAm(self.chiNam, self.canNam, True)

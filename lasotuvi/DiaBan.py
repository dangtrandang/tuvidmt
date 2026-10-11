# -*- coding: utf-8 -*-
"""
(c) 2016 doanguyen <dungnv2410@gmail.com>.
"""

import copy
from lasotuvi.AmDuong import diaChi, dichCung, khoangCachCung


class cungDiaBan(object):
    """docstring for cungDiaBan"""
    def __init__(self, cungID):
        # super(cungDiaBan, self).__init__()
        hanhCung = [None, "Thủy", "Thổ", "Mộc", "Mộc", "Thổ", "Hỏa",
                    "Hỏa", "Thổ", "Kim", "Kim", "Thổ", "Thủy"]
        self.cungSo = cungID
        self.hanhCung = hanhCung[cungID]
        self.cungSao = []
        self.cungAmDuong = -1 if (self.cungSo % 2 == 0) else 1
        self.cungTen = diaChi[self.cungSo]['tenChi']
        self.cungThan = False

    def themSao(self, sao):
        # [TLCT 2026-10-11] Tạo bản sao độc lập của sao để tránh nhiễm chéo
        # thuộc tính saoDacTinh giữa các lần lập lá số trong cùng process.
        sao_copy = copy.copy(sao)
        dacTinhSao(self.cungSo, sao_copy)
        self.cungSao.append(sao_copy.__dict__)
        return self

    def cungChu(self, tenCungChu):
        self.cungChu = tenCungChu
        return self

    def daiHan(self, daiHan):
        self.cungDaiHan = daiHan
        return self

    def tieuHan(self, tieuHan):
        self.cungTieuHan = diaChi[tieuHan + 1]['tenChi']
        return self

    def anCungThan(self):
        self.cungThan = True

    def anTuan(self):
        self.tuanTrung = True

    def anTriet(self):
        self.trietLo = True


class diaBan(object):
    def __init__(self, thangSinhAmLich, gioSinhAmLich):
        super(diaBan, self).__init__()
        self.thangSinhAmLich = thangSinhAmLich
        self.gioSinhAmLich = gioSinhAmLich
        self.thapNhiCung = [cungDiaBan(i) for i in range(13)]
        self.nhapCungChu()
        self.nhapCungThan()

    def cungChu(self, thangSinhAmLich, gioSinhAmLich):
        self.cungThan = dichCung(3, thangSinhAmLich - 1, gioSinhAmLich - 1)
        self.cungMenh = dichCung(3, thangSinhAmLich - 1, - (gioSinhAmLich) + 1)
        cungPhuMau = dichCung(self.cungMenh, 1)
        cungPhucDuc = dichCung(self.cungMenh, 2)
        cungDienTrach = dichCung(self.cungMenh, 3)
        cungQuanLoc = dichCung(self.cungMenh, 4)
        self.cungNoboc = dichCung(self.cungMenh, 5)  # Để an sao Thiên thương
        cungThienDi = dichCung(self.cungMenh, 6)
        self.cungTatAch = dichCung(self.cungMenh, 7)  # an sao Thiên sứ
        cungTaiBach = dichCung(self.cungMenh, 8)
        cungTuTuc = dichCung(self.cungMenh, 9)
        cungTheThiep = dichCung(self.cungMenh, 10)
        cungHuynhDe = dichCung(self.cungMenh, 11)

        cungChuThapNhiCung = [
            {
                'cungId': 1,
                'tenCung': "Mệnh",
                'cungSoDiaBan': self.cungMenh
            },
            {
                'cungId': 2,
                'tenCung': "Phụ mẫu",
                'cungSoDiaBan': cungPhuMau

            },
            {
                'cungId': 3,
                'tenCung': "Phúc đức",
                'cungSoDiaBan': cungPhucDuc

            },
            {
                'cungId': 4,
                'tenCung': "Điền trạch",
                'cungSoDiaBan': cungDienTrach

            },
            {
                'cungId': 5,
                'tenCung': "Quan lộc",
                'cungSoDiaBan': cungQuanLoc

            },
            {
                'cungId': 6,
                'tenCung': "Nô bộc",
                'cungSoDiaBan': self.cungNoboc

            },
            {
                'cungId': 7,
                'tenCung': "Thiên di",
                'cungSoDiaBan': cungThienDi

            },
            {
                'cungId': 8,
                'tenCung': "Tật Ách",
                'cungSoDiaBan': self.cungTatAch

            },
            {
                'cungId': 9,
                'tenCung': "Tài Bạch",
                'cungSoDiaBan': cungTaiBach

            },
            {
                'cungId': 10,
                'tenCung': "Tử tức",
                'cungSoDiaBan': cungTuTuc

            },
            {
                'cungId': 11,
                'tenCung': "Phu thê",
                'cungSoDiaBan': cungTheThiep

            },
            {
                'cungId': 12,
                'tenCung': "Huynh đệ",
                'cungSoDiaBan': cungHuynhDe

            }
        ]
        return cungChuThapNhiCung

    def nhapCungChu(self):
        for cung in self.cungChu(self.thangSinhAmLich, self.gioSinhAmLich):
            self.thapNhiCung[cung['cungSoDiaBan']].cungChu(cung['tenCung'])
        return self

    def nhapDaiHan(self, cucSo, gioiTinh):
        """Nhap dai han

        Args:
            cucSo (TYPE): Description
            gioiTinh (TYPE): Description

        Returns:
            TYPE: Description
        """
        for cung in self.thapNhiCung:
            khoangCach = khoangCachCung(cung.cungSo, self.cungMenh, gioiTinh)
            cung.daiHan(cucSo + khoangCach * 10)
        return self

    def nhapTieuHan(self, khoiTieuHan, gioiTinh, chiNam):
        # Vị trí khởi tiểu Hạn là của năm sinh theo chi
        # vì vậy cần phải tìm vị trí cung Tý của năm đó
        viTriCungTy1 = dichCung(khoiTieuHan, -gioiTinh * (chiNam - 1))

        # Tiếp đó là nhập hạn
        for cung in self.thapNhiCung:
            khoangCach = khoangCachCung(cung.cungSo, viTriCungTy1, gioiTinh)
            cung.tieuHan(khoangCach)
        return self

    def nhapCungThan(self):
        self.thapNhiCung[self.cungThan].anCungThan()

    def nhapSao(self, cungSo, *args):
        for sao in args:
            self.thapNhiCung[cungSo].themSao(sao)
        return self

    def nhapTuan(self, *args):
        for cung in args:
            self.thapNhiCung[cung].anTuan()
        return self

    def nhapTriet(self, *args):
        for cung in args:
            self.thapNhiCung[cung].anTriet()
        return self


def dacTinhSao(viTriDiaBan, sao):
    saoId = sao.saoID
    maTranDacTinh = {
        1: ["Tử vi", "B", "Đ", "M", "B", "V", "M", "M", "Đ", "M", "B", "V",
            "B"],
        2: ["Liêm trinh", "V", "Đ", "V", "H", "M", "H", "V", "Đ", "V", "H",
            "M", "H"],
        3: ["Thiên đồng", "V", "H", "M", "Đ", "H", "Đ", "H", "H", "M", "H",
            "H", "Đ"],
        4: ["Vũ khúc", "V", "M", "V", "Đ", "M", "H", "V", "M", "V", "Đ", "M",
            "H"],
        5: ["Thái dương", "H", "Đ", "V", "V", "V", "M", "M", "Đ", "H", "H",
            "H", "H"],
        6: ["Thiên cơ", "Đ", "Đ", "H", "M", "M", "V", "Đ", "Đ", "V", "M", "M",
            "H"],
        # [TLCT 2026-07-03] Bản gốc THIẾU Thiên phủ (chính tinh!). Điền theo
        # QUAN SÁT golden charts xem-tuvi.com (6 lá): Sửu=B, Dần=M, Mùi=Đ,
        # Hợi=Đ. (Bảng prose trong skill 14-chinh-tinh.md MÂU THUẪN với
        # xem-tuvi ở Sửu/Dần/Mùi -> theo xem-tuvi vì đó là chuẩn hiệu chỉnh
        # engine.) Vị trí chưa quan sát để None, bổ sung khi có lá mẫu.
        7: ["Thiên phủ", None, "B", "M", None, None, None, None, "Đ", None,
            None, None, "Đ"],
        8: ["Thái âm", "V", "Đ", "H", "H", "H", "H", "H", "Đ", "V", "M",
            "M", "M"],
        9: ["Tham lang", "H", "M", "Đ", "H", "V", "H", "H", "M", "Đ", "H",
            "V", "H"],
        10: ["Cự môn", "V", "H", "V", "M", "H", "H", "V", "H", "Đ", "M", "H",
             "Đ"],
        11: ["Thiên tướng", "V", "Đ", "M", "H", "V", "Đ", "V", "Đ", "M", "H",
             "V", "Đ"],
        12: ["Thiên lương", "V", "Đ", "V", "V", "M", "H", "M", "Đ", "V", "H",
             "M", "H"],
        13: ["Thất sát", "M", "Đ", "M", "H", "H", "V", "M", "Đ", "M", "H",
             "H", "V"],
        14: ["Phá quân", "M", "V", "H", "H", "Đ", "H", "M", "V", "H", "H",
             "Đ", "H"],
        51: ["Đà la", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ",
             "H"],
        52: ["Kình dương", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ", "H", "H",
             "Đ", "H"],
        55: ["Linh tinh", "H", "H", "Đ", "Đ", "Đ", "Đ", "Đ", "H", "H", "H",
             "H", "H"],
        56: ["Hỏa tinh", "H", "H", "Đ", "Đ", "Đ", "Đ", "Đ", "H", "H", "H",
             "H", "H"],
        57: ["Văn xương", "H", "Đ", "H", "Đ", "H", "Đ", "H", "Đ", "H", "H",
             "Đ", "Đ"],
        58: ["Văn khúc", "H", "Đ", "H", "Đ", "H", "Đ", "H", "Đ", "H", "H",
             "Đ", "Đ"],
        53: ["Địa không", "H", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ", "H",
             "H", "Đ"],
        54: ["Địa kiếp", "H", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ", "H", "H",
             "Đ"],
        95: ["Hóa kỵ", None, "Đ", None, None, "Đ", None, None, "Đ", None, None,
             "Đ", None],
        # [TLCT 2026-07-03] Mở rộng Đại/Tiểu hao + thêm các sao vòng Thái Tuế/
        # Lộc Tồn/đôi theo QUAN SÁT 6 golden charts xem-tuvi.com. Ô chưa có
        # bằng chứng = None (không suy diễn).
        36: ["Đại hao", None, None, "Đ", "Đ", None, None, "H", None, "Đ", "Đ",
             None, "Đ"],
        30: ["Tiểu Hao", "H", None, "Đ", "Đ", None, "H", None, None, "Đ",
             "Đ", None, None],
        16: ["Thiếu dương", None, "H", None, "Đ", None, None, "Đ", None, None,
             None, "H", "H"],
        17: ["Tang môn", "H", None, "Đ", None, "H", None, None, "H", None,
             None, None, "H"],
        18: ["Thiếu âm", "Đ", "H", None, "H", None, "H", None, None, "Đ",
             None, None, None],
        23: ["Bạch hổ", None, "H", None, None, None, "H", "H", None, "Đ",
             None, "H", None],
        29: ["Thanh long", None, "Đ", None, "H", None, None, "H", None, None,
             None, "Đ", None],
        79: ["Hồng loan", None, None, None, "Đ", None, None, "Đ", None, None,
             None, None, None],
        78: ["Đào hoa", None, None, None, "Đ", None, None, None, None, None,
             None, None, None],
        63: ["Long trì", None, None, None, None, None, None, None, None, None,
             "Đ", None, None],
        69: ["Thiên khốc", "Đ", "Đ", None, "Đ", None, None, "Đ", "Đ", None,
             "Đ", None, None],
        70: ["Thiên hư", "Đ", "Đ", None, "Đ", None, None, "Đ", "Đ", None, "Đ",
             None, None],
        98: ["Thiên mã", None, None, "Đ", None, None, "Đ", None, None, None,
             None, None, None],
        # [TLCT 2026-07-03] Thiên hình: bản gốc chỉ đánh dấu Đắc (Dần Mão Thân
        # Dậu), bỏ trống chỗ khác. Chuẩn phổ thông + xem-tuvi.com: các cung
        # còn lại là Hãm (sát tinh, vd Thiên hình (H) tại Tỵ trong lá số mẫu).
        73: ["Thiên Hình", "H", "H", "Đ", "Đ", "H", "H", "H", "H", "Đ",
             "Đ", "H", "H"],
        74: ["Thiên riêu", None, None, "Đ", "Đ", None, None, None, None, None,
             "Đ", "Đ", None],

    }
    # [TLCT 2026-10-11] Gán rõ ràng None khi sao không có đắc hãm tại cung
    # để bảo đảm trạng thái luôn được định nghĩa chính xác.
    if sao.saoID in maTranDacTinh.keys():
        dt = maTranDacTinh[sao.saoID][viTriDiaBan]
        if dt in ["M", "V", "Đ", "B", "H"]:
            sao.anDacTinh(dt)
        else:
            sao.saoDacTinh = None
    else:
        sao.saoDacTinh = None

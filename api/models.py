# -*- coding: utf-8 -*-
"""
Pydantic Models cho FastAPI Backend API Tử Vi.
"""
from typing import List, Optional, Union
from pydantic import BaseModel, Field, field_validator


class LaSoRequest(BaseModel):
    ho_ten: str = Field(default="Vô danh", description="Họ và tên của đương số")
    ngay_sinh: int = Field(..., ge=1, le=31, description="Ngày sinh (1-31)")
    thang_sinh: int = Field(..., ge=1, le=12, description="Tháng sinh (1-12)")
    nam_sinh: int = Field(..., ge=1000, le=3000, description="Năm sinh (ví dụ: 1990)")
    gio_sinh: int = Field(..., ge=0, le=23, description="Giờ sinh theo đồng hồ 24h (0-23)")
    phut_sinh: int = Field(default=0, ge=0, le=59, description="Phút sinh (0-59)")
    gioi_tinh: Union[int, str] = Field(..., description="Giới tính: 1 / 'nam' cho Nam, -1 / 'nu' cho Nữ")
    duong_lich: bool = Field(default=True, description="True nếu là Dương lịch, False nếu là Âm lịch")
    thang_nhuan: bool = Field(default=False, description="True nếu sinh vào tháng nhuận (chỉ dùng cho Âm lịch)")
    mui_gio: float = Field(default=7.0, ge=-12.0, le=14.0, description="Múi giờ sinh (mặc định +7 cho Việt Nam)")

    @field_validator("gioi_tinh", mode="before")
    @classmethod
    def normalize_gioi_tinh(cls, v):
        if isinstance(v, str):
            v_lower = v.strip().lower()
            if v_lower in ["nam", "1", "male", "m"]:
                return 1
            elif v_lower in ["nu", "nữ", "-1", "female", "f"]:
                return -1
            raise ValueError("Giới tính không hợp lệ. Vui lòng nhập 1 (Nam) hoặc -1 (Nữ).")
        if v not in [1, -1]:
            raise ValueError("Giới tính phải là 1 (Nam) hoặc -1 (Nữ).")
        return v


class SaoModel(BaseModel):
    sao_id: int = Field(..., description="Mã ID của sao trong engine")
    ten_sao: str = Field(..., description="Tên sao tiếng Việt")
    ngu_hanh: str = Field(..., description="Hành của sao (K, M, T, H, O)")
    loai_sao: int = Field(..., description="Phân loại sao (1: Chính tinh, 2+: Phụ tinh)")
    phuong_vi: str = Field(..., description="Phương vị (Bắc đẩu tinh, Nam đẩu tinh...)")
    am_duong: Union[int, str] = Field(..., description="Âm dương của sao")
    vong_trang_sinh: int = Field(..., description="1 nếu thuộc vòng Tràng Sinh, 0 nếu không")
    css_sao: str = Field(..., description="Tên class CSS theo ngũ hành")
    dac_tinh: Optional[str] = Field(default=None, description="Đặc tính đắc hãm: M, V, Đ, B, H hoặc None")


class CungModel(BaseModel):
    cung_so: int = Field(..., description="Số cung trên địa bàn (1..12 tương ứng Tý..Hợi)")
    ten_cung: str = Field(..., description="Tên địa chi của cung (Tý, Sửu...)")
    cung_chu: str = Field(..., description="Cung chức cai quản (Mệnh, Phụ mẫu, Phúc đức...)")
    hanh_cung: str = Field(..., description="Ngũ hành của cung (Thủy, Thổ, Mộc, Hỏa, Kim)")
    am_duong: int = Field(..., description="1 là Dương cung, -1 là Âm cung")
    is_than: bool = Field(..., description="True nếu cung này là Cung Thân cư")
    dai_han: int = Field(..., description="Số tuổi khởi đại hạn tại cung")
    tieu_han: str = Field(..., description="Địa chi tiểu hạn tương ứng")
    tuan: bool = Field(default=False, description="True nếu dính Tuần Không")
    triet: bool = Field(default=False, description="True nếu dính Triệt Lộ")
    sao: List[SaoModel] = Field(default_factory=list, description="Danh sách các sao an tại cung này")


class ThienBanModel(BaseModel):
    ho_ten: str = Field(..., description="Họ và tên đương số")
    gioi_tinh: int = Field(..., description="1: Nam, -1: Nữ")
    nam_nu: str = Field(..., description="'Nam' hoặc 'Nữ'")
    ngay_duong: int = Field(..., description="Ngày dương lịch")
    thang_duong: int = Field(..., description="Tháng dương lịch")
    nam_duong: int = Field(..., description="Năm dương lịch")
    ngay_am: int = Field(..., description="Ngày âm lịch")
    thang_am: int = Field(..., description="Tháng âm lịch")
    nam_am: int = Field(..., description="Năm âm lịch")
    thang_nhuan: int = Field(..., description="1 nếu là tháng nhuận, 0 nếu không")
    gio_sinh_can_chi: str = Field(..., description="Can Chi của giờ sinh")
    can_gio_sinh: int = Field(..., description="ID Can giờ sinh")
    chi_gio_sinh: str = Field(..., description="Tên Chi giờ sinh")
    can_ngay: str = Field(..., description="Tên Can ngày sinh")
    chi_ngay: str = Field(..., description="Tên Chi ngày sinh")
    can_thang: str = Field(..., description="Tên Can tháng sinh")
    chi_thang: str = Field(..., description="Tên Chi tháng sinh")
    can_nam: str = Field(..., description="Tên Can năm sinh")
    chi_nam: str = Field(..., description="Tên Chi năm sinh")
    am_duong_nam_sinh: str = Field(..., description="'Dương' hoặc 'Âm'")
    am_duong_menh: str = Field(..., description="'Âm dương thuận lý' hoặc 'Âm dương nghịch lý'")
    hanh_cuc: int = Field(..., description="ID hành của Cục")
    ten_cuc: str = Field(..., description="Tên Cục (Hỏa lục Cục, Thổ ngũ Cục...)")
    menh_chu: str = Field(..., description="Mệnh chủ")
    than_chu: str = Field(..., description="Thân chủ")
    menh: str = Field(..., description="Ký hiệu ngũ hành bản mệnh (K, M, T, H, O)")
    ban_menh: str = Field(..., description="Tên ngũ hành nạp âm bản mệnh (ví dụ: LỘ BÀN THỔ)")
    sinh_khac: str = Field(..., description="Tương quan giữa Bản Mệnh và Cục")
    mui_gio: float = Field(..., description="Múi giờ")


class LaSoResponse(BaseModel):
    thien_ban: ThienBanModel
    dia_ban: List[CungModel]

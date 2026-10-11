# -*- coding: utf-8 -*-
"""
FastAPI Routes cho API Tử Vi Đẩu Số.
"""
import logging
from fastapi import APIRouter, HTTPException, status
from api.models import LaSoRequest, LaSoResponse
from api.service import generate_laso

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Tử Vi API"])


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """
    Endpoint kiểm tra trạng thái hoạt động của backend API.
    Không tính toán hay gọi engine an sao.
    """
    return {
        "status": "ok",
        "message": "Tu Vi Backend API is running",
        "version": "1.0.0"
    }


@router.post(
    "/laso",
    response_model=LaSoResponse,
    status_code=status.HTTP_200_OK,
    summary="Lập lá số Tử Vi",
    description="Nhận thông tin sinh, kiểm tra dữ liệu và trả về cấu trúc Thiên Bàn và 12 cung Địa Bàn."
)
def create_laso(req: LaSoRequest):
    """
    Endpoint tiếp nhận thông tin sinh và trả về dữ liệu lá số Tử Vi hoàn chỉnh.
    """
    try:
        return generate_laso(req)
    except ValueError as ve:
        # Bắt các lỗi validation nghiệp vụ (ví dụ: ngày 31/02, giờ không hợp lệ...)
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except Exception as e:
        # Bắt các lỗi ngoại lệ không mong muốn, không để lộ traceback ra client
        logger.error(f"Internal server error while creating laso: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Đã xảy ra lỗi nội bộ trong quá trình tính toán lá số. Vui lòng thử lại sau."
        )

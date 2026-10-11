# -*- coding: utf-8 -*-
"""
Entry point cho ứng dụng FastAPI Backend Tử Vi.
"""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes import router

app = FastAPI(
    title="Tử Vi Đẩu Số API",
    description="Backend API cung cấp dịch vụ an sao và lập lá số Tử Vi Đẩu Số cho ứng dụng PWA.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Cho phép CORS để frontend PWA có thể kết nối thuận tiện
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Chuẩn hóa thông báo lỗi validation thành tiếng Việt, cấu trúc rõ ràng.
    """
    errors = []
    for err in exc.errors():
        loc = " -> ".join([str(x) for x in err.get("loc", [])])
        msg = err.get("msg", "Dữ liệu không hợp lệ")
        errors.append({"field": loc, "message": msg})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Dữ liệu yêu cầu không hợp lệ hoặc thiếu trường bắt buộc.",
            "errors": errors
        }
    )


# Đăng ký routes
app.include_router(router)


@app.get("/", tags=["Thông tin chung"])
def root():
    return {
        "app": "Tử Vi Đẩu Số API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/api/v1/health",
            "laso": "/api/v1/laso"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# Sử dụng Python 3.11-slim nhẹ và ổn định
FROM python:3.11-slim

# Ngăn chặn ghi file .pyc và bật unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Cài đặt dependencies trước để tận dụng Docker cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn ứng dụng
COPY lasotuvi/ /app/lasotuvi/
COPY api/ /app/api/
COPY main.py /app/

# Tạo non-root user để tăng tính bảo mật
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose cổng 8000
EXPOSE 8000

# Khởi chạy Uvicorn bind 0.0.0.0
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

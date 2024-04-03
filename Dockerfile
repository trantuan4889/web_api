# Sử dụng image python:latest làm base image
FROM python:latest

# Thư mục làm việc
WORKDIR /app

# Sao chép mã nguồn ứng dụng vào thư mục /app trong container
COPY . /app

# Cài đặt các dependencies từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mở cổng 5000 để kết nối với Flask
EXPOSE 5000

# Khởi chạy Flask server
CMD ["python", "app.py"]

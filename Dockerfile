# Python imajı
FROM python:3.10-slim

# Ortam değişkenleri
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Gereksinimleri yükle
COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Proje dosyaları
COPY backend/* .
COPY models/*.h5 ./models

# Port
EXPOSE 8000

# Başlatma komutu
CMD ["MODELS_DIR=/app/models", "gunicorn", "music_backend.wsgi:application", "--bind", "0.0.0.0:8000"]

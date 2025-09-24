# Python 3.12 の slim
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# psycopg2系がビルド/実行に必要な依存を入れる
RUN apt-get update && apt-get install -y --no-install-recommends \
      gcc \
      libpq-dev \
      build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 先に依存だけ入れてレイヤーをキャッシュさせる
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# アプリ
COPY . .

# 本番は gunicorn を使うのがおすすめ
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

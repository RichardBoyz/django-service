FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-mysql-client \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8000

RUN cd turing_backend

CMD ["/app/backend-entrypoint.sh"]
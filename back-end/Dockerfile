FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y pkg-config \
    && apt-get install -y gcc \
    && apt-get install -y default-libmysqlclient-dev \
    && apt-get install -y python3-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev g++ openssl-dev
COPY backend/requirements.txt backend/requirements.txt
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev g++ openssl-dev \
    && pip3 install --no-cache-dir -U -r backend/requirements.txt \
    && apk del gcc musl-dev linux-headers libffi-dev g++ openssl-dev

EXPOSE 5000
# COPY . .
CMD ["flask", "run"]
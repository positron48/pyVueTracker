# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev g++ openssl-dev
COPY backend/requirements.txt backend/requirements.txt
RUN pip3 install -U -r backend/requirements.txt
EXPOSE 5000
# COPY . .
CMD ["flask", "run"]
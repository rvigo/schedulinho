FROM ghcr.io/rvigo/alpine-s6-base-image:latest

RUN apk add --no-cache py3-pip
COPY root /
COPY /app /app
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

FROM alpine-s6-base-image:test

ENV S6_KEEP_ENV=1 \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    S6_SERVICES_GRACETIME=0 \
    S6_KILL_GRACETIME=0

RUN apk add --no-cache py3-pip

COPY root /

WORKDIR /app

COPY /app .
COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

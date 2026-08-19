FROM python:3.12-alpine

WORKDIR /app
COPY app.py /app/app.py
RUN addgroup -S dsg && adduser -S -G dsg dsg && mkdir -p /data && chown -R dsg:dsg /data /app
USER dsg

ENV PORT=8080 \
    DSG_RELAY_STORE_PATH=/data/observatory-status.json \
    DSG_RELAY_AUTHORIZED_SOURCE=EAGLE30154 \
    DSG_RELAY_MAX_BODY_BYTES=65536

EXPOSE 8080
VOLUME ["/data"]
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD wget -q -O - http://127.0.0.1:8080/health >/dev/null || exit 1

CMD ["python", "/app/app.py"]

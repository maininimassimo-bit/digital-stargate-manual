FROM python:3.13-slim-bookworm
WORKDIR /app
COPY infrastructure/pixinsight-pilot/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY tools /app/tools
COPY infrastructure/pixinsight-pilot/app.py /app/app.py
USER 65532:65532
CMD ["python", "app.py"]

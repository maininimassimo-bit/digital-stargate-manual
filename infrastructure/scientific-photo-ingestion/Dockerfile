FROM python:3.13-slim-bookworm
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends clamav clamav-freshclam ca-certificates && rm -rf /var/lib/apt/lists/*
COPY infrastructure/scientific-photo-ingestion/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY tools /app/tools
COPY docs/contracts/pixinsight-workflow-provenance.schema.json /app/docs/contracts/pixinsight-workflow-provenance.schema.json
COPY docs/data/scientific-session-catalog.json /app/docs/data/scientific-session-catalog.json
COPY infrastructure/scientific-photo-ingestion/app.py /app/app.py
USER clamav
CMD ["python", "app.py"]

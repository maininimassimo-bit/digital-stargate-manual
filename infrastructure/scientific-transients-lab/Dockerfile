FROM python:3.13-slim-bookworm
WORKDIR /app
ENV DISABLE_GCS_PYTHON_CLIENT_OTEL_BUCKET_METADATA=true
COPY infrastructure/scientific-transients-lab/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY tools /app/tools
COPY source-revision.txt /app/source-revision.txt
USER 65532:65532
CMD ["python", "-m", "tools.scientific_transients.lab_runtime"]

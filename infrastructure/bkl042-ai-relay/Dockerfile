FROM python:3.12-alpine
WORKDIR /app
RUN pip install --no-cache-dir "google-cloud-firestore>=2.16,<3"
COPY app.py .
USER nobody
CMD ["python", "app.py"]

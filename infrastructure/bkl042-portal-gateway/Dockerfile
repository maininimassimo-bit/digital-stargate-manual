FROM python:3.12-alpine
WORKDIR /app
RUN pip install --no-cache-dir "google-auth>=2.30,<3"
COPY app.py .
USER nobody
CMD ["python", "app.py"]

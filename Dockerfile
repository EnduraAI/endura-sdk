FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir endura-sdk

COPY src/main.py /app/src/main.py

CMD ["python", "/app/src/main.py"]
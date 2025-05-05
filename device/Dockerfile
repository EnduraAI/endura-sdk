FROM python:3.9-slim

WORKDIR /app

COPY device/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY sdk /app/sdk
COPY device /app/device

WORKDIR /app/device

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y gcc python3-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py /app/main.py
COPY sdk /app/sdk

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
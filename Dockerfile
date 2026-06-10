FROM python:3.11

WORKDIR /app
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app/logs && chmod 777 /app/logs


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

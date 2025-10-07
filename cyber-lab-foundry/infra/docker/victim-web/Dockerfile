FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/app.py
COPY templates /app/templates
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV ENABLE_RISKY=false

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]

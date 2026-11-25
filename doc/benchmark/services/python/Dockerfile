FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

EXPOSE 8080

# WEB_CONCURRENCY = number of uvicorn worker processes.
# Python's GIL prevents one process from using several cores for CPU work,
# so we run one worker per core to give Python a realistic multi-core config.
ENV WEB_CONCURRENCY=1
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8080 --workers ${WEB_CONCURRENCY} --no-access-log"]

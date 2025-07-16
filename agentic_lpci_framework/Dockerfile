FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    redis-server \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional production dependencies
RUN pip install --no-cache-dir \
    pinecone-client \
    weaviate-client \
    prometheus-client \
    celery \
    gunicorn \
    flask

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p /app/data/redis /app/data/vectors /app/logs

# Expose ports
EXPOSE 8080 6379 9090

# Start script
CMD ["python", "real_production_demo.py"]
# Use official Python 3.12 slim image as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (阿里云镜像加速)
RUN sed -i 's|deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y gcc g++ pkg-config libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies (阿里云 pip 镜像)
COPY requirements.txt .
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir langchain langchain-openai pgvector psycopg2-binary

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Create non-root user to run application
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8006

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8006/api/v1/config/health')" || exit 1

# Start command
CMD ["python", "main.py"]
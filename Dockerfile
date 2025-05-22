# Gabby Bot Dockerfile
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (if exists) and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy Gabby bot code
COPY . .

# Set environment variables (override in docker run or compose)
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "gabby_main.py"]

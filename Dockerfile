"""Dockerfile for containerized deployment."""

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install chromium

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p data logs reports

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_HEADLESS=true

# Run application
CMD ["python", "main.py", "schedule"]

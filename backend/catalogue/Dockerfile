FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/catalogue/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy config, gateway (for security dependencies), and catalogue code
COPY backend/config /app/backend/config
COPY backend/gateway /app/backend/gateway
COPY backend/catalogue /app/backend/catalogue

EXPOSE 8002

CMD ["python", "-m", "backend.catalogue.main"]


# =============== Build stage ===============
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt



# =============== Runtime stage ===============
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY --from=builder /install /usr/local

# Copy project
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
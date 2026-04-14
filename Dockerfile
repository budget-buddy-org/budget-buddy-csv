# Builder stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies for building psycopg2
RUN apt-get update && apt-get install -y     libpq-dev     gcc     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y     libpq5     && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
COPY app.py utils.py .

# Ensure the local bin is in PATH
ENV PATH=/root/.local/bin:$PATH
# Ensure logs are sent straight to terminal without buffering
ENV PYTHONUNBUFFERED=1

# Use environment variables for DB connection
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DB_NAME=budget_buddy_db
ENV DB_USER=budget_buddy_user
ENV DB_PASSWORD=password

ENTRYPOINT ["python3", "app.py"]

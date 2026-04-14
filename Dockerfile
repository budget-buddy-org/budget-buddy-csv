FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Use environment variables for DB connection
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DB_NAME=budget_buddy_db
ENV DB_USER=budget_buddy_user
ENV DB_PASSWORD=password

ENTRYPOINT ["python", "app.py"]

FROM cgr.dev/chainguard/python:latest-dev AS builder

USER root
RUN apk add --no-cache build-base postgresql-18-dev

WORKDIR /app
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM cgr.dev/chainguard/python:latest-dev

USER root
RUN apk add --no-cache libpq-18

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY app.py utils.py ./

ENV PATH=/opt/venv/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    DB_HOST=localhost \
    DB_PORT=5432 \
    DB_NAME=budget_buddy_db \
    DB_USER=budget_buddy_user

USER nonroot
ENTRYPOINT ["/opt/venv/bin/python", "/app/app.py"]

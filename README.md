# Budget Buddy CSV Importer

A simple Python tool to import budget transactions from CSV into a PostgreSQL database.

## Features

- Imports transactions from CSV.
- Deduplication: Skips already existing transactions for the user.
- Category synchronization: Automatically creates missing categories.
- Robust parsing: Handles European format for amounts and dates.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   Copy `.env.example` to `.env` and fill in your database credentials.

## Usage

```bash
python app.py <file_path> <username>
```

Example:
```bash
python app.py transactions.csv alice
```

## Running with Docker

The project is automatically built and published to GHCR (GitHub Container Registry) on every push to the `main` branch.

**Image:** `ghcr.io/budget-buddy-org/budget-buddy-csv:latest`

### Running the published image

```bash
docker run --rm \
  --env-file .env \
  -v $(pwd):/app/data \
  ghcr.io/budget-buddy-org/budget-buddy-csv:latest /app/data/transactions.csv <username>
```

### Local build and run

1. Build the Docker image:
   ```bash
   docker build -t budget-buddy-csv .
   ```

2. Run the importer:
   ```bash
   docker run --rm \
     --env-file .env \
     -v $(pwd):/app/data \
     budget-buddy-csv /app/data/transactions.csv <username>
   ```

**Note:** Ensure that `DB_HOST` in your `.env` file is accessible from the container (e.g., use your machine's local IP or `host.docker.internal` instead of `localhost`).
   
### Running with Docker Compose (Integration)

If you are using the main deployment from the `budget-buddy-deployment` directory, the importer is already integrated as a service.

1. Navigate to the deployment directory:
   ```bash
   cd ../budget-buddy-deployment
   ```

2. Run the importer as a one-off task:
   ```bash
   docker compose run --rm csv-importer /app/data/transactions.csv <username>
   ```

This will use the same database and credentials configured for the entire application stack.

## Running Tests

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

Run tests:
```bash
python3 -m pytest test_utils.py
```

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
python app.py <file_path> <user_id>
```

Example:
```bash
python app.py test-data.csv 09a00c76-e6c7-494c-9dd1-cbe92e6528ae
```

## Running Tests

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

Run tests:
```bash
python3 -m pytest test_utils.py
```

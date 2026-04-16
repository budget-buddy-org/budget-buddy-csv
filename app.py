from utils import parse_amount, parse_date, get_now, load_transactions_from_csv
import argparse
import csv
import logging
import os
import sys
import uuid
from typing import List, Dict, Optional

import psycopg2
from dotenv import load_dotenv
from psycopg2 import extras

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Import budget-buddy CSV transactions into PostgreSQL.")
    parser.add_argument("file_path", help="Path to the CSV file.")
    parser.add_argument("username", help="Username of the user owner.")
    args = parser.parse_args()

    # Validate file existence
    if not os.path.exists(args.file_path):
        logger.error(f"File not found: {args.file_path}")
        sys.exit(1)

    # DB Connection params from ENV
    db_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }

    if not all([db_params['database'], db_params['user'], db_params['password']]):
        logger.error("Database environment variables (DB_NAME, DB_USER, DB_PASSWORD) must be set.")
        sys.exit(1)

    try:
        conn = psycopg2.connect(**db_params)
        logger.info("Connected to the database.")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        sys.exit(1)

    try:
        with conn:
            with conn.cursor() as cur:
                # 1. Verify user exists and fetch ID
                cur.execute("SELECT id FROM users WHERE username = %s", (args.username,))
                row = cur.fetchone()
                if row is None:
                    logger.error(f"User with username '{args.username}' not found in database.")
                    sys.exit(1)
                
                user_uuid = str(row[0])

                # 2. Read CSV and prepare data
                transactions_data, categories_in_csv = load_transactions_from_csv(args.file_path)

                if not transactions_data:
                    logger.info("No valid transactions found in CSV.")
                    return

                # 3. Synchronize categories
                # Fetch existing categories for the user
                cur.execute("SELECT id, name FROM categories WHERE owner_id = %s", (user_uuid,))
                existing_categories = {name: str(cat_id) for cat_id, name in cur.fetchall()}

                missing_categories = [name for name in categories_in_csv if name not in existing_categories]
                
                if missing_categories:
                    logger.info(f"Inserting {len(missing_categories)} missing categories.")
                    now = get_now()
                    category_inserts = [
                        (str(uuid.uuid4()), 1, name, user_uuid, now, now)
                        for name in missing_categories
                    ]
                    extras.execute_values(
                        cur,
                        "INSERT INTO categories (id, version, name, owner_id, created_at, updated_at) VALUES %s",
                        category_inserts
                    )
                    
                    # Update category mapping
                    for cat_id, version, name, owner_id, ca, ua in category_inserts:
                        existing_categories[name] = cat_id

                # 4. Fetch existing transactions to avoid duplicates
                cur.execute(
                    "SELECT date, amount, description, category_id, type FROM transactions WHERE owner_id = %s",
                    (user_uuid,)
                )
                existing_tx_keys = set()
                for row in cur.fetchall():
                    # PostgreSQL date might be a date object
                    tx_date = row[0].strftime('%Y-%m-%d') if hasattr(row[0], 'strftime') else str(row[0])
                    existing_tx_keys.add((tx_date, row[1], row[2], row[3], row[4]))

                # 5. Batch insert transactions
                transaction_inserts = []
                skipped_count = 0
                now = get_now()
                
                for row in transactions_data:
                    category_id = existing_categories[row['category']]
                    key = (row['date'], row['amount'], row['description'], category_id, row['type'])
                    
                    if key in existing_tx_keys:
                        skipped_count += 1
                        continue
                        
                    transaction_inserts.append((
                        str(uuid.uuid4()), 
                        1, 
                        category_id, 
                        row['amount'], 
                        row['type'], 
                        'EUR', 
                        row['date'], 
                        row['description'], 
                        user_uuid, 
                        now, 
                        now
                    ))

                if skipped_count > 0:
                    logger.info(f"Skipped {skipped_count} duplicate transactions.")

                if not transaction_inserts:
                    logger.info("No new transactions to insert.")
                    return

                logger.info(f"Inserting {len(transaction_inserts)} new transactions.")
                extras.execute_values(
                    cur,
                    "INSERT INTO transactions (id, version, category_id, amount, type, currency, date, description, owner_id, created_at, updated_at) VALUES %s",
                    transaction_inserts
                )

        logger.info("Import completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred during import. Transaction rolled back: {e}")
        # The 'with conn' block will automatically rollback on exception if not handled, 
        # but we log it and exit with error code.
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    main()

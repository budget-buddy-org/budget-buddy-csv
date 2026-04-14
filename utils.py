from datetime import datetime, timezone
from decimal import Decimal
import csv
import logging

logger = logging.getLogger(__name__)

def parse_amount(amount_str: str) -> int:
    """Parses EUR amount string like '250,00 €' into cents."""
    try:
        # Remove currency symbol and whitespace
        clean_str = amount_str.replace('€', '').strip()
        
        # If there are both dot and comma, comma is decimal, dot is thousand separator
        if ',' in clean_str and '.' in clean_str:
            clean_str = clean_str.replace('.', '').replace(',', '.')
        elif ',' in clean_str:
            clean_str = clean_str.replace(',', '.')
            
        # Convert to Decimal for precision, then to cents
        amount_decimal = Decimal(clean_str)
        return int(amount_decimal * 100)
    except Exception as e:
        raise ValueError(f"Invalid amount format: {amount_str}") from e

def parse_date(date_str: str) -> str:
    """Parses date string 'DD/MM/YYYY' into 'YYYY-MM-DD'."""
    try:
        dt = datetime.strptime(date_str, '%d/%m/%Y')
        return dt.strftime('%Y-%m-%d')
    except Exception as e:
        raise ValueError(f"Invalid date format: {date_str}") from e

def get_now() -> datetime:
    """Returns current UTC timestamp."""
    return datetime.now(timezone.utc)

def load_transactions_from_csv(file_path: str):
    """Reads transactions from CSV and returns a list of dictionaries and a set of categories."""
    transactions_data = []
    categories_in_csv = set()
    
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        row_num = 1
        for row in reader:
            row_num += 1
            try:
                # Basic validation
                if not all(k in row for k in ('date', 'amount', 'category')):
                    logger.warning(f"Row {row_num} is missing required columns. Skipping.")
                    continue
                    
                category_name = row['category'].strip()
                if not category_name:
                    logger.warning(f"Row {row_num} has empty category. Skipping.")
                    continue
                
                categories_in_csv.add(category_name)
                
                transactions_data.append({
                    'date': parse_date(row['date'].strip()),
                    'amount': parse_amount(row['amount'].strip()),
                    'description': row.get('description', '').strip() or None,
                    'category': category_name
                })
            except ValueError as ve:
                logger.warning(f"Skipping row {row_num} due to data format error: {ve}")
                continue
    return transactions_data, categories_in_csv

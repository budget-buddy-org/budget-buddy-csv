from datetime import datetime, timezone
from decimal import Decimal

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

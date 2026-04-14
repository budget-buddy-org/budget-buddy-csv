import pytest
from utils import load_transactions_from_csv

def test_csv_structure_and_count():
    """Verify that test.csv results in exactly 10 valid transactions."""
    transactions, categories = load_transactions_from_csv('test.csv')
    assert len(transactions) == 10
    # Categories: Lunch, Groceries, Services, Eating out, Transport, Subscriptions, Income, Health/medical, Entertainment
    # Transport appears twice. So 9 unique categories.
    assert len(categories) == 9

def test_csv_parsing_integrity():
    """Verify that the parsed data matches the expected values from test.csv."""
    transactions, _ = load_transactions_from_csv('test.csv')
    
    # Row 1: 01/01/2026,"10,00 €",Lunch,Lunch
    assert transactions[0]['date'] == '2026-01-01'
    assert transactions[0]['amount'] == 1000
    assert transactions[0]['description'] == 'Lunch'
    assert transactions[0]['category'] == 'Lunch'
    
    # Row 8: 08/01/2026,"1.200,00 €",Salary,Income
    assert transactions[7]['date'] == '2026-01-08'
    assert transactions[7]['amount'] == 120000
    assert transactions[7]['category'] == 'Income'

def test_csv_categories():
    """Verify that the categories are correctly extracted from test.csv."""
    _, categories = load_transactions_from_csv('test.csv')
    expected_categories = {
        'Lunch', 'Groceries', 'Services', 'Eating out', 
        'Transport', 'Subscriptions', 'Income', 'Health/medical', 'Entertainment'
    }
    assert categories == expected_categories


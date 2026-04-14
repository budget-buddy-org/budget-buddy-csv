import pytest
from utils import parse_amount, parse_date

def test_parse_amount_valid():
    assert parse_amount("10,15") == 1015
    assert parse_amount("10.15") == 1015
    assert parse_amount("0,01") == 1
    assert parse_amount("0.01") == 1
    assert parse_amount("-10,15") == -1015
    assert parse_amount("1.000,50") == 100050 # Hmm, does it handle dots? No, wait.
    # Actually, parse_amount only replaces comma with dot.
    # So "1.000,50" -> "1.000.50" which is invalid.

def test_parse_amount_with_euro():
    assert parse_amount("10,15 €") == 1015
    assert parse_amount("€ 10,15") == 1015

def test_parse_amount_invalid():
    with pytest.raises(ValueError):
        parse_amount("abc")

def test_parse_date_valid():
    assert parse_date("31/03/2026") == "2026-03-31"
    assert parse_date("01/04/2026") == "2026-04-01"

def test_parse_date_invalid():
    with pytest.raises(ValueError):
        parse_date("2026-03-31")
    with pytest.raises(ValueError):
        parse_date("31-03-2026")

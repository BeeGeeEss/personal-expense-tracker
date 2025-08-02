import csv
import os
import pytest
from app import Transaction, ExpenseTracker, ExpenseTrackerCLI
from datetime import datetime
from typing import List, Dict, Optional
from tabulate import tabulate

def test_transaction_creation_expense():
    """Test for creating a basic expense transaction"""
    transaction = Transaction("01/07/2025", "Food", "Lunch at cafe", 15.50, "expense")
    
    assert transaction.date == "01/07/2025"
    assert transaction.category == "Food"
    assert transaction.description == "Lunch at cafe"
    assert transaction.amount == 15.50
    assert transaction.is_expense() == True

def test_transaction_creation_income():
    """Test for creating a basic income transaction"""
    transaction = Transaction("14/07/2025", "Wages", "Pay from work", 1000.00, "income")
    
    assert transaction.date == "14/07/2025"
    assert transaction.category == "Wages"
    assert transaction.description == "Pay from work"
    assert transaction.amount == 1000.00
    assert transaction.is_income() == True

def test_transaction_default_type():
    """Test that default transaction type is expense"""
    transaction = Transaction("02/07/2025", "Takeaway", "Coffee", 7.50)
    
    assert transaction.transaction_type == "expense"
    assert transaction.is_expense() == True
    assert transaction.is_income() == False

def test_transaction_signed_amount():
    """Test that signed amounts work correctly for income(+) and expense(-) transactions"""
    income = Transaction("14/06/2025", "Wages", "Pay from work", 1000.00, "income")
    assert income.get_signed_amount() == +1000.00
    
    expense = Transaction("03/08/2025", "Bills", "Phone bill", 73.00, "expense")
    assert expense.get_signed_amount() == -73.00

def test_transaction_invalid_date():
    """Test that invalid date formats raise an error"""
    with pytest.raises(ValueError, match="Date must be in DD/MM/YYYY format"):
        Transaction("2025-01-25", "Food", "Restaurant dinner", 37.80, "expense")

def test_transaction_invalid_type():
    """Test that invalid transaction types raise an error"""
    with pytest.raises(ValueError, match="Transaction type must be 'income' or 'expense'"):
        Transaction("31/07/2025", "Groceries", "Shopping for dinner", 34.56, "food")
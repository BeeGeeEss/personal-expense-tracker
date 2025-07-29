import csv
import os
from datetime import datetime
from typing import List, Dict, Optional
from tabulate import tabulate


class Transaction:
    """Class to represent a financial transaction"""
    
    def __init__(self, date: str, category: str, description: str, amount: float, transaction_type: str = "expense"):
        self.date = self._validate_date(date)
        self.category = category.strip().title()
        self.description = description.strip()
        self.amount = abs(float(amount))
        self.transaction_type = transaction_type.lower()
        
        # Validate transaction type
        if self.transaction_type not in ["income", "expense"]:
            raise ValueError("Transaction type must be 'income' or 'expense'")
    
    def _validate_date(self, date_str: str) -> str:
        """Validate and format date string in the format DD/MM/YYYY"""
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return date_str
        except ValueError:
            raise ValueError("Date must be in DD/MM/YYYY format")
    
    def get_signed_amount(self) -> float:
        """Return amount with proper sign: positive (+) for income or negative (-) for expense"""
        return self.amount if self.transaction_type == "income" else -self.amount

   def is_income(self) -> bool:
        """Check if this is an income transaction"""
        return self.transaction_type == "income"

    def is_expense(self) -> bool:
        """Check if this is an expense transaction"""
        return self.transaction_type == "expense"
   
    def to_list(self) -> List:
        """Convert transaction to list format for storage in CSV"""
        return [self.date, self.category, self.description, self.amount, self.transaction_type]
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary format"""
        return {
            'date': self.date,
            'category': self.category,
            'description': self.description,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'signed_amount': self.get_signed_amount()
        }
    
    def __str__(self) -> str:
        """String representation of transaction"""
        sign = "+" if self.is_income() else "-"
        return f"{self.date} | {self.category} | {self.description} | {sign}${self.amount:.2f}"


class ExpenseTracker:
    """Main class to manage expense tracking functionality"""
    
    def __init__(self, csv_file: str = "transactions.csv"):
        self.csv_file = csv_file
        self.transactions: List[Transaction] = []
        self.csv_headers = ["date", "category", "description", "amount", "transaction_type"]
        
        # Load existing transactions on startup
        self.load_transactions()
        
    def add_transaction(self, transaction: Transaction) -> None:
        """Add a new transaction to the tracker"""
        self.transactions.append(transaction)
        self.save_transactions()
    
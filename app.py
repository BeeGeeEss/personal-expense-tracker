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
    
    def load_transactions(self) -> None:
        """Load transactions from CSV file"""
        try:
            if os.path.exists(self.csv_file):
                with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        try:
                            transaction = Transaction(
                                date=row['date'],
                                category=row['category'],
                                description=row['description'],
                                amount=float(row['amount']),
                                transaction_type=row['transaction_type']
                            )
                            self.transactions.append(transaction)
                        except (ValueError, KeyError) as e:
                            print(f"Warning: Skipping invalid transaction in CSV: {e}")
                            continue
                print("\n" + "=" * 50 + "\n")
                print(f"Loaded {len(self.transactions)} transactions from {self.csv_file}" + "\n")
            else:
                print(f"No existing data file found. Now creating a new file...")
        except Exception as e:
            print(f"Error loading transactions: {e}")
    
    def save_transactions(self) -> None:
        """Save all transactions to CSV file"""
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.csv_headers)
                for transaction in self.transactions:
                    writer.writerow(transaction.to_list())
        except Exception as e:
            print(f"Error saving transactions: {e}")
    
    def get_all_transactions(self) -> List[Transaction]:
        """Get all transactions"""
        return self.transactions.copy()
    
    def get_transactions_by_category(self, category: str) -> List[Transaction]:
        """Get transactions filtered by category"""
        return [t for t in self.transactions if t.category.lower() == category.lower()]
    
    def get_transactions_by_date_range(self, start_date: str, end_date: str) -> List[Transaction]:
        """Get transactions within a date range"""
        try:
            # Validate date format and convert to datetime for comparison
            start_dt = datetime.strptime(start_date, "%d/%m/%Y")
            end_dt = datetime.strptime(end_date, "%d/%m/%Y")
            
            # Filter transactions by converting their dates to datetime objects
            filtered_transactions = []
            for t in self.transactions:
                t_dt = datetime.strptime(t.date, "%d/%m/%Y")
                if start_dt <= t_dt <= end_dt:
                    filtered_transactions.append(t)
            
            return filtered_transactions
        except ValueError:
            raise ValueError("Dates must be in DD/MM/YYYY format")
    
    def get_transactions_by_type(self, transaction_type: str) -> List[Transaction]:
        """Get transactions by type (income or expense)"""
        return [t for t in self.transactions if t.transaction_type == transaction_type.lower()]
    
    def get_categories(self) -> List[str]:
        """Get unique categories from all transactions"""
        return list(set(t.category for t in self.transactions))
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics"""
        if not self.transactions:
            return {
                'total_transactions': 0,
                'total_income': 0,
                'total_expenses': 0,
                'net_balance': 0,
                'categories': []
            }
        
        income_transactions = self.get_transactions_by_type("income")
        expense_transactions = self.get_transactions_by_type("expense")
        
        total_income = sum(t.amount for t in income_transactions)
        total_expenses = sum(t.amount for t in expense_transactions)
        
        return {
            'total_transactions': len(self.transactions),
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': total_income - total_expenses,
            'categories': self.get_categories()
        }
   
    def get_category_summary(self) -> Dict[str, Dict]:
        """Get summary by category"""
        category_summary = {}
        
        for category in self.get_categories():
            category_transactions = self.get_transactions_by_category(category)
            income = sum(t.amount for t in category_transactions if t.is_income())
            expenses = sum(t.amount for t in category_transactions if t.is_expense())
            
            category_summary[category] = {
                'count': len(category_transactions),
                'income': income,
                'expenses': expenses,
                'net': income - expenses
            }
        
        return category_summary


class ExpenseTrackerCLI:
    """Command Line Interface for the Expense Tracker"""
    
    def __init__(self):
        self.tracker = ExpenseTracker()
    
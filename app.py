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
    
    def display_menu(self) -> None:
        """Display the main menu options"""
        print("\n" + "="*50)
        print("$ Personal Expense Tracker $")
        print("="*50)
        print("1. Add New Transaction")
        print("2. View All Transactions")
        print("3. View Transactions by Category")
        print("4. View Transactions by Date Range")
        print("5. View Summary Statistics")
        print("6. View Category Summary")
        print("7. Exit")
        print("="*50)
    
    def get_user_choice(self) -> str:
        """Get and validate user menu choice"""
        while True:
            try:
                choice = input("Enter your choice (1-7): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7']:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 7.")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                exit()
    
    def get_date_input(self, prompt: str) -> str:
        """Get and validate date input from user"""
        while True:
            try:
                date_str = input(prompt).strip()
                if not date_str:
                    date_str = datetime.now().strftime("%d/%m/%Y")
                    print(f"Using today's date: {date_str}")
                
                # Validate date format
                datetime.strptime(date_str, "%d/%m/%Y")
                return date_str
            except ValueError:
                print("Invalid date format. Please use DD/MM/YYYY (e.g., 01/01/2025)")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                exit()
    
    def get_amount_input(self, prompt: str) -> float:
        """Get and validate amount input from user"""
        while True:
            try:
                amount_str = input(prompt).strip()
                amount = float(amount_str)
                if amount <= 0:
                    print("Amount must be greater than 0.")
                    continue
                return amount
            except ValueError:
                print("Invalid amount. Please enter a valid number.")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                exit()
    
    def get_transaction_type(self) -> str:
        """Get transaction type from user"""
        while True:
            try:
                print("\nTransaction Type:")
                print("1. Income")
                print("2. Expense")
                choice = input("Choose transaction type (1 or 2): ").strip()
                
                if choice == '1':
                    return "income"
                elif choice == '2':
                    return "expense"
                else:
                    print("Invalid choice. Please enter 1 or 2.")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                exit()
    
    def add_transaction(self) -> None:
        """Add a new transaction through CLI"""
        print("\n" + "-" * 50)
        print("Add New Transaction")
        print("-" * 50)
        
        try:
            # Get transaction details
            date = self.get_date_input("Enter date (DD/MM/YYYY), or press Enter for today: ")
            category = input("Enter category: ").strip()
            description = input("Enter description: ").strip()
            amount = self.get_amount_input("Enter amount: $")
            transaction_type = self.get_transaction_type()
            
            # Validate required fields
            if not category or not description:
                print("Category and description are required.")
                return
            
            # Create and add transaction
            transaction = Transaction(date, category, description, amount, transaction_type)
            self.tracker.add_transaction(transaction)
            
            print(f"Transaction added successfully!")
            print(f"{transaction}")
            
        except Exception as e:
            print(f"Error adding transaction: {e}")
    
    def display_transactions(self, transactions: List[Transaction], title: str = "Transactions") -> None:
        """Display transactions in a formatted table"""
        if not transactions:
            print(f"\n{title}")
            print("No transactions found.")
            return
        
        # Sort transactions by date (newest to oldest)
        sorted_transactions = sorted(transactions, key=lambda t: datetime.strptime(t.date, "%d/%m/%Y"), reverse=True)
        
        print(f"\n{title}")
        print("-" * 80)
        
        # Convert to list of dictionaries for tabulate
        data = []
        total_income = 0
        total_expenses = 0
        
        for t in sorted_transactions:
            # Format amount with sign (+ or -) at the end for both income and expenses
            if t.is_expense():
                amount_display = f"${t.amount:.2f}-"
                total_expenses += t.amount
            else:
                amount_display = f"${t.amount:.2f}+"
                total_income += t.amount
            
            data.append([
                t.date,
                t.category,
                t.description,
                t.transaction_type.title(),
                amount_display
            ])
        
        headers = ["Date", "Category", "Description", "Type", "Amount"]
        print(tabulate(data, headers=headers, tablefmt="grid"))
        
        # Add summary information at the bottom
        if sorted_transactions:
            net_balance = total_income - total_expenses
            print(f"\nTransaction Summary:")
            print(f"Total Income:   ${total_income:.2f}+")
            print(f"Total Expenses: ${total_expenses:.2f}-")
            if net_balance >= 0:
                print(f"Net Balance:    ${net_balance:.2f}+")
            else:
                print(f"Net Balance:    ${abs(net_balance):.2f}-")
    
    def view_all_transactions(self) -> None:
        """View all transactions"""
        transactions = self.tracker.get_all_transactions()
        self.display_transactions(transactions, "All Transactions")
    
    def view_transactions_by_category(self) -> None:
        """View transactions filtered by category"""
        categories = self.tracker.get_categories()
        
        if not categories:
            print("No categories found.")
            return
        
        print("\n" + "-" * 50)
        print("Available Categories:")
        print("-" * 50)
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        
        try:
            choice = input("\nEnter category number or type category name: ").strip()
            
            # Check if it's a number
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(categories):
                    selected_category = categories[choice_num - 1]
                else:
                    print("Invalid category number.")
                    return
            else:
                selected_category = choice
            
            transactions = self.tracker.get_transactions_by_category(selected_category)
            self.display_transactions(transactions, f"Transactions in '{selected_category}' Category")
            
        except Exception as e:
            print(f"Error viewing transactions by category: {e}")
    
    def view_transactions_by_date_range(self) -> None:
        """View transactions within a date range"""
        try:
            print("\n" + "-" * 50)
            print("Enter Date Range")
            print("-" * 50)
            start_date = self.get_date_input("Enter start date (DD/MM/YYYY): ")
            end_date = self.get_date_input("Enter end date (DD/MM/YYYY): ")
            
            if start_date > end_date:
                print("Start date must be before or equal to end date.")
                return
            
            transactions = self.tracker.get_transactions_by_date_range(start_date, end_date)
            self.display_transactions(transactions, f"Transactions from {start_date} to {end_date}")
            
        except Exception as e:
            print(f"Error viewing transactions by date range: {e}")
    
    def view_summary_statistics(self) -> None:
        """Display summary statistics"""
        stats = self.tracker.get_summary_stats()
        
        print("\n" + "-" * 50)
        print("Summary Statistics")
        print("-" * 50)
        print(f"Total Transactions: {stats['total_transactions']}")
        print(f"Total Income: ${stats['total_income']:.2f}")
        print(f"Total Expenses: ${stats['total_expenses']:.2f}")
        print(f"Net Balance: ${stats['net_balance']:.2f}")
        print(f"Categories: {len(stats['categories'])}")
        
        if stats['categories']:
            print(f"Category List: {', '.join(stats['categories'])}")
    
    def view_category_summary(self) -> None:
        """Display category summary"""
        category_summary = self.tracker.get_category_summary()
        
        if not category_summary:
            print("No categories found.")
            return
        
        print("\n" + "-" * 50)
        print("Category Summary")
        print("-" * 50)
        
        # Convert to table format
        data = []
        for category, stats in category_summary.items():
            # Format net amount with + or - at the end
            if stats['net'] >= 0:
                net_display = f"${stats['net']:.2f}+"
            else:
                net_display = f"${abs(stats['net']):.2f}-"
            
            data.append([
                category,
                stats['count'],
                f"${stats['income']:.2f}",
                f"${stats['expenses']:.2f}",
                net_display
            ])
        
        headers = ["Category", "Count", "Income", "Expenses", "Net"]
        print(tabulate(data, headers=headers, tablefmt="grid"))
    
# Personal Expense Tracker Application

The Personal Expense Tracker application is a Command Line Interface (CLI) application designed to help users manage their personal finances.

## Key Features

- Easy to use menu system with input validation and user-friendly error messages
- Multiple ways to view and analyse transaction data, including by date range or category
- Ability to future-date transactions for budget planning
- Consistent and clear table formatting for ease of use
- Transaction data is saved to (and loaded from) a CSV file, which can be used in spreadsheet applications

## Technical Pre-Requisites

- A functioning computer (e.g., laptop, desktop)
- A Command Line Interface (e.g., the terminal within VS Code)
- Installation of Python3

## Instructions for Use

### Application

1. Change directory (`cd`) to the root folder of the application.
2. Create a virtual environment: `python3 -m venv .venv`
3. Ensure the virtual environment is active. If it doesn't activate automatically, run: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the program: `python3 app.py`

### Automated Testing

1. Within the virtual environment (refer to steps 1 through 4 above), run: `pytest -v`
2. Test results will be displayed in the terminal.

## Navigating the Application

### Main Menu

Upon starting the application, the user is presented with a list of options:

1. Add New Transaction
2. View All Transactions
3. View Transactions by Category
4. View Transactions by Date Range
5. View Summary Statistics
6. View Category Summary
7. Exit

The user is prompted to `Enter your choice (1-7)`, with the number entered opening the corresponding menu item.

### 1. Add New Transaction

- Enter the date of the transaction in the format of `DD/MM/YYYY` (leave blank and press Enter if using today's date).
- Enter the category of the transaction (e.g., Food, Bills, Self-Care, Wages, etc.)
- Enter a description for the transaction (e.g., lunch with colleagues, motorcycle insurance, physio appointment etc.)
- Enter the value of the transaction.
- Confirm if the transaction is income (choose `1`) or an expense (choose `2`).
- The transaction will be recorded and viewable under the different menu options.

### 2. View All Transactions

- All of the entered transactions will be presented in a table.

- For each transaction, the table displays:
  - Date
  - Category
  - Description
  - Type (i.e., Income or Expense)
  - Amount (dollar value, + or -)
- The total values for Income, Expenses and Net Balance are displayed below the table.

### 3. View Transactions by Category

- User-defined categories are listed with a number beside them, in the same way the main menu is organised.
- Input the corresponding category number, or type the category's name.
- Transactions belonging to that category will be displayed in a table that presents the Date, Category, Description, Type and Amount.
- The Transaction Summary (totals for Income, Expenses and Net Balance) is displayed below the table.

### 4. View Transactions by Date Range

- Enter a start date for the date range, in the format of `DD/MM/YYYY`.
- Enter an end date for the date range, in the format of `DD/MM/YYYY`.
- All transactions made within the specified date range will be displayed in a table that presents the Date, Category, Description, Type and Amount.
- The Transaction Summary (totals for Income, Expenses and Net Balance) is displayed below the table.

### 5. View Summary Statistics

- A high level overview of all transaction data:
  - Total Transactions count
  - Total Income value
  - Total Expenses value
  - Net Balance (i.e., Income minus Expenses)
  - Categories count
  - Category List

### 6. View Category Summary

- All categories are presented in a table.
- For each category, the table displays:
  - Category name
  - Count of transactions in that category
  - Income value per category
  - Expense value per category
  - Net balance (+ or -) per category

### 7. Exit

- Upon exiting the application, the newly entered transaction data is saved to a CSV file.
- This data is loaded into the application when it is next run.

## Libraries Used

All libraries referenced within this application have been used ethically and in accordance with their respective licensing agreements, detailed below.

### Python Standard Library

The Python Standard Library is distributed under the [Python Software Foundation License](https://docs.python.org/3/license.html), which is an [open-source](https://opensource.org/osd) license (i.e., free to use, modify and distribute). The below libraries are part of the Python Standard Library.

#### `csv`

[This library](https://docs.python.org/3/library/csv.html) is used for reading and writing CSV (Comma Separated Values) files.

#### `datetime`

[This library](https://docs.python.org/3/library/datetime.html) is used for the validation and formatting of dates, as well as retrieving the current date.

#### `os`

[This library](https://docs.python.org/3/library/os.html) is used to check if the required CSV file already exists.

#### `typing`

[This library](https://docs.python.org/3/library/typing.html) provides support for type hints.

### Third-Party Libraries

#### `Tabulate`

[Tabulate](https://pypi.org/project/tabulate/) is distributed under the open-source [MIT License](https://opensource.org/license/mit). Per the [Tabulate license](https://github.com/aks/python-tabulate/blob/master/LICENSE), this software is free to use, modify and distribute.

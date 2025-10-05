import sqlite3
from datetime import datetime

DB_NAME = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            amount INTEGER,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(category, amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
        (category, amount, datetime.now().strftime("%Y-%m-%d"))
    )
    conn.commit()
    conn.close()

def get_all_expenses():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT category, amount FROM expenses")
    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_expenses():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()

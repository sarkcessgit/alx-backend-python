#!/usr/bin/env python3
"""
0-log_queries.py - Decorator that logs SQL queries with timestamp before execution.
"""

import sqlite3
import functools
from datetime import datetime  # ✅ Required import

def log_queries(func):
    """
    Decorator to log SQL queries with timestamp.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else "")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Executing SQL query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
users = fetch_all_users(query="SELECT * FROM users")


#!/usr/bin/env python3
"""
1-execute.py - Reusable context manager that executes a SQL query and manages connection.
"""

import sqlite3

class ExecuteQuery:
    """
    Custom context manager to execute a SQL query with parameters and return the results.
    Usage:
        with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
            # use results
    """
    def __init__(self, query, params=None, db_name="users.db"):
        self.query = query
        self.params = params or ()
        self.db_name = db_name
        self.connection = None
        self.results = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

# ✅ Example usage:
if __name__ == "__main__":
    with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
        for row in results:
            print(row)

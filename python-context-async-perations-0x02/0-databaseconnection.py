#!/usr/bin/env python3
"""
0-databaseconnection.py - Class-based context manager for handling DB connections.
"""

import sqlite3

class DatabaseConnection:
    """
    Custom context manager for opening and closing a SQLite database connection.
    Usage:
        with DatabaseConnection('users.db') as conn:
            # use conn
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()

# ✅ Example usage:
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)

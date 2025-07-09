#!/usr/bin/env python3
"""
1-with_db_connection.py - Decorator to handle opening and closing SQLite DB connections.
"""

import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator that automatically opens and closes the database connection.
    Passes the connection as the first argument to the wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetches a user from the database by ID.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Example usage
user = get_user_by_id(user_id=1)
print(user)

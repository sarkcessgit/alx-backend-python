#!/usr/bin/env python3
"""
2-transactional.py - Decorators for database connection and transaction management.
"""

import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator that opens a SQLite connection, passes it to the wrapped function,
    and ensures it is closed afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def transactional(func):
    """
    Decorator that wraps the function in a database transaction.
    - Commits if the function completes successfully.
    - Rolls back if an exception occurs.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed and rolled back: {e}")
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Updates a user's email in the users table by ID.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Example usage
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')

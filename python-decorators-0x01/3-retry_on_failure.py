#!/usr/bin/env python3
"""
3-retry_on_failure.py - Retry decorator for handling transient DB query failures.
"""

import time
import sqlite3
import functools

def with_db_connection(func):
    """
    Opens a SQLite connection and passes it to the function.
    Closes the connection afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Retries a function call if it raises an exception.
    Waits `delay` seconds between each retry, up to `retries` times.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[Attempt {attempt}] Error: {e}")
                    last_exception = e
                    time.sleep(delay)
            print(f"All {retries} retries failed.")
            raise last_exception
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetches all users from the users table, retrying on failure.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Example usage
users = fetch_users_with_retry()
print(users)

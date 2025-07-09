#!/usr/bin/env python3
"""
4-cache_query.py - Caches results of database queries to avoid redundant executions.
"""

import time
import sqlite3
import functools

query_cache = {}

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

def cache_query(func):
    """
    Decorator that caches the result of a query based on the SQL string.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else "")
        if query in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[query]
        print(f"Cache miss for query: {query}. Executing and caching result.")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Executes the given SQL query and returns the results.
    Uses caching to prevent redundant queries.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call: executes and caches the query
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call: uses cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

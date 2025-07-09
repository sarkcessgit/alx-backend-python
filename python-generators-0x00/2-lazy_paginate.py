#!/usr/bin/env python3
"""
2-lazy_paginate.py - Lazily loads paginated user data from database using a generator.
"""

from seed import connect_to_prodev

def paginate_users(page_size, offset):
    """
    Fetches a single page of users from the database with limit and offset.
    Returns a list of user dictionaries.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches paginated data from user_data table.
    Only loads the next page when needed.

    Yields: list of user records (page_size at a time)
    """
    offset = 0
    while True:  # 1 loop only (allowed)
        page = paginate_users(page_size, offset)
        if not page:
            break  # Stop if no more data
        yield page
        offset += page_size

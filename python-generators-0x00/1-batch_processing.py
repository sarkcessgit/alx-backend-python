#!/usr/bin/env python3
"""
1-batch_processing.py - Batch data streaming and filtering users over age 25
"""

import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Generator that fetches users in batches from user_data table.
    Yields: list of user dictionaries (length ≤ batch_size)
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',  # Replace with your MySQL username
            password='your_mysql_password',  # Replace with your MySQL password
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:
            yield batch  # Yield remaining users

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error in stream_users_in_batches: {e}")
        return


def batch_processing(batch_size):
    """
    Processes batches of users, filters those over age 25,
    and prints them one by one.
    """
    for batch in stream_users_in_batches(batch_size):  # Loop 1
        for user in batch:  # Loop 2
            if float(user.get("age", 0)) > 25:
                print(user)  # Output matching user

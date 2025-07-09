#!/usr/bin/env python3
"""
0-stream_users.py - Generator function that streams rows from user_data table.
"""

import mysql.connector
from mysql.connector import Error

def stream_users():
    """
    Generator that yields one user row at a time from the user_data table
    in the ALX_prodev database.
    Yields: dict containing user_id, name, email, and age
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

        for row in cursor:
            yield row  # Yield each row as a dictionary

        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error while streaming users: {e}")
        return  # Gracefully exit if there's a connection issue


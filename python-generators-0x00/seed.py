#!/usr/bin/env python3
"""
seed.py - Sets up MySQL database ALX_prodev with user_data table
and populates it from user_data.csv for generator-based processing.
"""

import mysql.connector
from mysql.connector import Error
import csv

def connect_db():
    """
    Connects to the MySQL server (no database selected).
    Returns: connection object or None
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',  # Replace with your MySQL username
            password='your_mysql_password'  # Replace with your MySQL password
        )
        return connection
    except Error as e:
        print(f"Connection error: {e}")
        return None

def create_database(connection):
    """
    Creates the ALX_prodev database if it does not exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Database creation error: {e}")

def connect_to_prodev():
    """
    Connects directly to the ALX_prodev database.
    Returns: connection object or None
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',  # Replace with your MySQL username
            password='your_mysql_password',  # Replace with your MySQL password
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Connection to ALX_prodev error: {e}")
        return None

def create_table(connection):
    """
    Creates the user_data table in the ALX_prodev database.
    Fields:
    - user_id (Primary Key, UUID, Indexed)
    - name (VARCHAR, NOT NULL)
    - email (VARCHAR, NOT NULL)
    - age (DECIMAL, NOT NULL)
    """
    try:
        cursor = connection.cursor()
        create_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        );
        """
        cursor.execute(create_query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Table creation error: {e}")

def insert_data(connection, file_path):
    """
    Reads user_data.csv and inserts data into user_data table.
    Skips duplicate user_ids.
    """
    try:
        cursor = connection.cursor()
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s", (row['user_id'],))
                if cursor.fetchone():
                    continue  # Skip if user already exists
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (row['user_id'], row['name'], row['email'], row['age']))
        connection.commit()
        cursor.close()
        print("Data inserted successfully.")
    except Error as e:
        print(f"Data insertion error: {e}")
    except FileNotFoundError:
        print(f"CSV file '{file_path}' not found.")


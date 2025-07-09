#!/usr/bin/env python3
"""
4-stream_ages.py - Streams user ages from database and calculates memory-efficient average.
"""

from seed import connect_to_prodev

def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    try:
        connection = connect_to_prodev()
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        for (age,) in cursor:  # Single loop
            yield float(age)
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error streaming ages: {e}")


def compute_average_age():
    """
    Computes average age using the stream_user_ages generator without loading all data into memory.
    """
    total_age = 0
    count = 0
    for age in stream_user_ages():  # Second loop
        total_age += age
        count += 1
    average = total_age / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")

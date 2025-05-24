# This script tests the `get_connection` function by connecting to the MySQL database using credentials from the `.env` file.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db import get_connection

def test_connection():
    try:
        connection = get_connection()
        if connection.is_connected():
            print("Database connection successful!")
            connection.close()
        else:
            print("Failed to connect to the database.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()

import mysql.connector
from mysql.connector import pooling
import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'bmsit_AI.049',
    'database': 'college_leave_mgmt'
}

# Create a connection pool
connection_pool = None

def init_db():
    """Initialize the database connection pool."""
    global connection_pool
    try:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name="leave_management_pool",
            pool_size=5,
            **DB_CONFIG
        )
        print("Database connection pool created successfully")
        return True
    except Exception as e:
        print(f"Error creating database connection pool: {str(e)}")
        return False

def get_connection():
    """Get a connection from the pool."""
    if connection_pool:
        return connection_pool.get_connection()
    else:
        raise Exception("Database connection pool not initialized")

def execute_query(query, params=None, fetch=True):
    """Execute a query and return results if needed."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            connection.commit()
            return cursor.lastrowid
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Database error: {str(e)}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def execute_many(query, params_list):
    """Execute a query with multiple parameter sets."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.executemany(query, params_list)
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Database error: {str(e)}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
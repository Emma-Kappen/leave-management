import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """Establish a connection to the MySQL database."""
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "college_leave_mgmt")
        )
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        raise

def init_db():
    """Initialize the database with required tables."""
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Create staff table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                ID VARCHAR(10) PRIMARY KEY,
                Name VARCHAR(100),
                E_Mail VARCHAR(100),
                Designation VARCHAR(50)
            )
        """)

        # Create student table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student (
                USN VARCHAR(10) PRIMARY KEY,
                Name VARCHAR(100),
                E_Mail VARCHAR(100)
            )
        """)

        # Create leave_requests table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leave_requests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(10),
                start_date DATE,
                end_date DATE,
                reason TEXT,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()
        cursor.close()
        connection.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {str(e)}")
        raise
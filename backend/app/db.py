import mysql.connector
import os
from dotenv import load_dotenv
import time

load_dotenv()

def get_connection(max_retries=3, retry_delay=1):
    """Establish a connection to the MySQL database with retry logic."""
    retries = 0
    last_error = None
    
    while retries < max_retries:
        try:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "bmsit_AI.049"),
                database=os.getenv("DB_NAME", "college_leave_mgmt")
            )
            # Test the connection
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            return connection
        except Exception as e:
            last_error = e
            print(f"Database connection attempt {retries+1} failed: {str(e)}")
            retries += 1
            if retries < max_retries:
                time.sleep(retry_delay)
    
    print(f"All database connection attempts failed: {str(last_error)}")
    raise last_error

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
        
        # Create Department table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Department (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                HOD VARCHAR(10)
            )
        """)
        
        # Add Dept_ID column to Student table if it doesn't exist
        try:
            cursor.execute("SHOW COLUMNS FROM student LIKE 'Dept_ID'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE student ADD COLUMN Dept_ID INT")
            
            # Add Join_Date column to Student table if it doesn't exist
            cursor.execute("SHOW COLUMNS FROM student LIKE 'Join_Date'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE student ADD COLUMN Join_Date DATE")
                
            # Create user_password table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_password (
                    user_id VARCHAR(10) PRIMARY KEY,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL
                )
            """)
            
            # Insert sample data if tables are empty
            cursor.execute("SELECT COUNT(*) FROM Department")
            if cursor.fetchone()[0] == 0:
                # Insert departments
                departments = [
                    ("Computer Science", "FAC001"),
                    ("Electrical Engineering", "FAC002"),
                    ("Mechanical Engineering", "FAC003")
                ]
                cursor.executemany(
                    "INSERT INTO Department (Name, HOD) VALUES (%s, %s)",
                    departments
                )
                
            # Insert admin if not exists
            cursor.execute("SELECT COUNT(*) FROM staff WHERE ID = 'ADMIN001'")
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO staff (ID, Name, E_Mail, Designation) VALUES (%s, %s, %s, %s)",
                    ("ADMIN001", "Admin User", "admin@example.com", "Administrator")
                )
                
        except Exception as e:
            print(f"Error setting up database: {str(e)}")

        connection.commit()
        cursor.close()
        connection.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {str(e)}")
        raise
from backend.app.db import get_connection
import json
import os

def seed_database():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Create staff table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                ID VARCHAR(10) PRIMARY KEY,
                Name VARCHAR(100),
                E_Mail VARCHAR(100),
                Designation VARCHAR(50)
            )
        """)

        # Create student table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student (
                USN VARCHAR(10) PRIMARY KEY,
                Name VARCHAR(100),
                E_Mail VARCHAR(100)
            )
        """)

        # Create leave_requests table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leave_requests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(20),
                start_date DATE,
                end_date DATE,
                reason TEXT,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                leave_type VARCHAR(20)
            )
        """)

        # Create leave_approvers table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leave_approvers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                leave_id INT,
                approver_id VARCHAR(10),
                approval_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Check if admin exists
        cursor.execute("SELECT ID FROM staff WHERE ID = 'ADMIN001'")
        if not cursor.fetchone():
            # Seed admin user
            cursor.execute("""
                INSERT INTO staff (ID, Name, E_Mail, Designation)
                VALUES (%s, %s, %s, %s)
            """, ('ADMIN001', 'Admin User', 'admin@college.edu', 'Administrator'))

        # Check if faculty exists
        cursor.execute("SELECT ID FROM staff WHERE ID = 'FAC001'")
        if not cursor.fetchone():
            # Seed faculty user
            cursor.execute("""
                INSERT INTO staff (ID, Name, E_Mail, Designation)
                VALUES (%s, %s, %s, %s)
            """, ('FAC001', 'John Doe', 'john.doe@college.edu', 'Professor'))

        # Check if student exists
        cursor.execute("SELECT USN FROM student WHERE USN = 'STU001'")
        if not cursor.fetchone():
            # Seed student user
            cursor.execute("""
                INSERT INTO student (USN, Name, E_Mail)
                VALUES (%s, %s, %s)
            """, ('STU001', 'Jane Smith', 'jane.smith@college.edu'))

        # Add sample leave requests
        cursor.execute("SELECT COUNT(*) as count FROM leave_requests")
        if cursor.fetchone()['count'] == 0:
            # Add sample leave requests
            cursor.execute("""
                INSERT INTO leave_requests 
                (user_id, start_date, end_date, reason, status, leave_type)
                VALUES 
                ('STU001', DATE_ADD(CURDATE(), INTERVAL 1 DAY), DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'Medical appointment', 'pending', 'sick')
            """)

        # Commit the changes
        connection.commit()
        print('Database seeded successfully.')

    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    seed_database()
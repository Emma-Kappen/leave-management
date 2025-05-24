from backend.app.db import get_connection
import datetime

def seed_faculty_data():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
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
        
        # Add sample leave requests
        today = datetime.date.today()
        
        # Check if leave requests already exist
        cursor.execute("SELECT COUNT(*) FROM leave_requests")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Add sample leave requests
            leave_requests = [
                ('1CS21CS001', today + datetime.timedelta(days=1), today + datetime.timedelta(days=3), 'Fever and cold', 'pending', 'sick'),
                ('1CS21CS002', today + datetime.timedelta(days=2), today + datetime.timedelta(days=5), 'Family function', 'approved', 'casual'),
                ('1CS21CS003', today + datetime.timedelta(days=1), today + datetime.timedelta(days=2), 'Severe headache', 'rejected', 'sick'),
                ('1CS21CS004', today + datetime.timedelta(days=3), today + datetime.timedelta(days=6), 'Flu symptoms', 'pending', 'sick'),
                ('1CS21CS005', today + datetime.timedelta(days=4), today + datetime.timedelta(days=7), 'Wedding', 'approved', 'casual')
            ]
            
            cursor.executemany("""
                INSERT INTO leave_requests 
                (user_id, start_date, end_date, reason, status, leave_type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, leave_requests)
            
            # Add sample students if they don't exist
            cursor.execute("SELECT COUNT(*) FROM student")
            student_count = cursor.fetchone()[0]
            
            if student_count == 0:
                students = [
                    ('1CS21CS001', 'Aditi Kumar', 'aditi.k@example.edu'),
                    ('1CS21CS002', 'Rahul Verma', 'rahul.v@example.edu'),
                    ('1CS21CS003', 'Sneha Patil', 'sneha.p@example.edu'),
                    ('1CS21CS004', 'Nikhil Rao', 'nikhil.r@example.edu'),
                    ('1CS21CS005', 'Divya Shah', 'divya.s@example.edu')
                ]
                
                cursor.executemany("""
                    INSERT INTO student (USN, Name, E_Mail)
                    VALUES (%s, %s, %s)
                """, students)
        
        connection.commit()
        print("Faculty data seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding faculty data: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    seed_faculty_data()
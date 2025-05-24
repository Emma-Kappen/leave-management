from backend.app.db import get_connection

def test_db_connection():
    try:
        print("Testing database connection...")
        connection = get_connection()
        
        if connection.is_connected():
            print("Database connection successful!")
            
            # Test if student table exists and has data
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor]
            print(f"Tables in database: {tables}")
            
            # Check if student table exists
            if 'student' in tables:
                cursor.execute("SELECT COUNT(*) as count FROM student")
                result = cursor.fetchone()
                print(f"Number of students in database: {result['count']}")
                
                # Check if specific student exists
                cursor.execute("SELECT * FROM student WHERE USN = '1CS21CS001'")
                student = cursor.fetchone()
                if student:
                    print(f"Found student: {student['Name']}")
                else:
                    print("Student 1CS21CS001 not found in database")
            else:
                print("Student table not found in database")
                
            cursor.close()
            connection.close()
        else:
            print("Failed to connect to database")
    except Exception as e:
        print(f"Database test error: {str(e)}")

if __name__ == "__main__":
    test_db_connection()
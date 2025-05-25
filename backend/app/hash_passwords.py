from werkzeug.security import generate_password_hash
from db import execute_query, init_db

def hash_all_passwords():
    """Hash all plaintext passwords in the database."""
    print("Starting password hashing process...")
    
    # Hash student passwords
    print("Hashing student passwords...")
    students = execute_query("SELECT USN, Password FROM Student")
    for student in students:
        if not student['Password'].startswith('pbkdf2:sha256:'):
            hashed_password = generate_password_hash(student['Password'])
            execute_query(
                "UPDATE Student SET Password = %s WHERE USN = %s",
                (hashed_password, student['USN']),
                fetch=False
            )
            print(f"Hashed password for student {student['USN']}")
    
    # Hash staff passwords
    print("Hashing staff passwords...")
    staff = execute_query("SELECT ID, Password FROM Staff")
    for member in staff:
        if not member['Password'].startswith('pbkdf2:sha256:'):
            hashed_password = generate_password_hash(member['Password'])
            execute_query(
                "UPDATE Staff SET Password = %s WHERE ID = %s",
                (hashed_password, member['ID']),
                fetch=False
            )
            print(f"Hashed password for staff {member['ID']}")
    
    # Hash admin passwords
    print("Hashing admin passwords...")
    admins = execute_query("SELECT Admin_ID, Password FROM Admin")
    for admin in admins:
        if not admin['Password'].startswith('pbkdf2:sha256:'):
            hashed_password = generate_password_hash(admin['Password'])
            execute_query(
                "UPDATE Admin SET Password = %s WHERE Admin_ID = %s",
                (hashed_password, admin['Admin_ID']),
                fetch=False
            )
            print(f"Hashed password for admin {admin['Admin_ID']}")
    
    print("All passwords have been hashed.")

if __name__ == "__main__":
    init_db()
    hash_all_passwords()
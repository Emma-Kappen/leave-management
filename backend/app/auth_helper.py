from flask_login import UserMixin
import json
import os
from pathlib import Path

class User(UserMixin):
    """User class for Flask-Login."""
    def __init__(self, id, role):
        self.id = id
        self.role = role
    
    def get_id(self):
        return self.id

def get_user_password(user_id):
    """Get password for a user from the JSON file."""
    try:
        # Path to the users.json file
        users_file = Path(__file__).parent.parent / 'users.json'
        
        if not os.path.exists(users_file):
            # Create a default users file if it doesn't exist
            default_users = {
                "STUDENT1": "password123",
                "STUDENT2": "password123",
                "FAC1": "faculty123",
                "ADMIN1": "admin123"
            }
            with open(users_file, 'w') as f:
                json.dump(default_users, f, indent=4)
        
        # Read the users file
        with open(users_file, 'r') as f:
            users = json.load(f)
        
        return users.get(user_id)
    except Exception as e:
        print(f"Error getting user password: {str(e)}")
        return None

def authenticate_user(user_id, password):
    """Authenticate a user with user_id and password."""
    stored_password = get_user_password(user_id)
    
    if not stored_password:
        return False
    
    # For development, we're using plain text passwords
    return stored_password == password
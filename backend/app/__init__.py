import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from .db import init_db
import json
from werkzeug.security import check_password_hash

load_dotenv()
login_manager = LoginManager()

class User:
    def __init__(self, user_id, user_type, data):
        self.id = user_id
        self.user_type = user_type  # 'staff' or 'student'
        self.data = data
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return self.id

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/templates')),
        static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/static'))
    )
    # Enable CORS for all routes and origins
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

    # Initialize extensions
    login_manager.init_app(app)

    # Initialize the database
    init_db()

    # Set up the Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        from .db import get_connection
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            # Try to find in staff table
            if user_id.startswith(('ADMIN', 'FAC')):
                cursor.execute("SELECT * FROM staff WHERE ID = %s", (user_id,))
                user_data = cursor.fetchone()
                if user_data:
                    return User(user_id, 'staff', user_data)

            # Try to find in student table
            if user_id.startswith('STU'):
                cursor.execute("SELECT * FROM student WHERE USN = %s", (user_id,))
                user_data = cursor.fetchone()
                if user_data:
                    return User(user_id, 'student', user_data)

            return None
        finally:
            cursor.close()
            connection.close()

    # Configure login view
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.student import student_bp
    from .routes.faculty import faculty_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(faculty_bp, url_prefix='/faculty')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app
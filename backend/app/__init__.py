from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from .db import init_db
from .models import Student, Staff

# Initialize extensions
login_manager = LoginManager()
login_manager.login_view = 'auth.student_login'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    # Check if it's a student
    student = Student.get_by_id(user_id)
    if student:
        return student
    
    # Check if it's a staff member
    staff = Staff.get_by_id(user_id)
    if staff:
        return staff
    
    return None

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, 
                template_folder='../../frontend/templates',
                static_folder='../../frontend/static')
    
    # Basic configuration
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['CORS_HEADERS'] = 'Content-Type'
    
    # Initialize database
    init_db()
    
    # Initialize extensions with app
    login_manager.init_app(app)
    CORS(app, supports_credentials=True)
    
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
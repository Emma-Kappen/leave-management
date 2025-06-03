from flask import Flask, render_template
from flask_login import LoginManager
from .db import init_db
from .routes.auth import auth_bp
from .routes.student import student_bp
from .routes.faculty import faculty_bp
from .routes.admin import admin_bp, Admin
import os
from dotenv import load_dotenv

def create_app():
    # Load environment variables
    load_dotenv()
    
    app = Flask(__name__, 
                template_folder='../../frontend/templates',
                static_folder='../../frontend/static')
    
    # Configure app with SECRET_KEY
    app.config.from_object('config.Config')
    
    # Initialize database
    init_db()
    
    # Configure login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        # Check if user_id starts with a specific prefix to determine user type
        if user_id.isdigit():
            # Try to load as Admin (assuming Admin IDs are numeric)
            from .routes.admin import Admin
            admin = Admin.get_by_id(int(user_id))
            if admin:
                return admin
        elif user_id.startswith(('F', 'S')):
            # Try to load as Staff
            from .models import Staff
            return Staff.get_by_id(user_id)
        else:
            # Try to load as Student
            from .models import Student
            return Student.get_by_id(user_id)
        return None
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(faculty_bp, url_prefix='/faculty')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Home route
    @app.route('/')
    def index():
        return render_template('login/index.html')
    
    return app
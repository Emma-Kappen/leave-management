import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from .db import db
from .routes.auth import auth_bp
from .routes.student import student_bp
from .routes.faculty import faculty_bp
from .routes.admin import admin_bp
from backend.config import Config

load_dotenv()
login_manager = LoginManager()

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/templates')),
        static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/static'))
    )
    CORS(app)
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # Initialize the database and create tables
        from .db import init_db
        init_db(app)

    # Set up the Flask-Login user loader
    from .models import Staff, Student
    @login_manager.user_loader
    def load_user(user_id):
        # Try to load as student first
        if user_id.startswith('STU'):
            return Student.query.filter_by(USN=user_id).first()
        # Then try as faculty
        return Staff.query.filter_by(ID=user_id).first()

    # Configure login view
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    # Register your blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(faculty_bp, url_prefix='/faculty')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app

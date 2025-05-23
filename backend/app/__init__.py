import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from .routes.auth import auth_bp
from .routes.student import student_bp
from .routes.faculty import faculty_bp
from .routes.admin import admin_bp
from backend.config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

    db.init_app(app)
    login_manager.init_app(app)

    # Register your blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(faculty_bp, url_prefix='/faculty')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app

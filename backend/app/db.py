from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

def init_db(app):
    with app.app_context():
        db.create_all()

        # Import models here to avoid circular imports
        from .models import Staff, Student

        # Check if admin user exists, if not create one
        admin = Staff.query.filter_by(ID='ADMIN001').first()
        if not admin:
            admin = Staff(
                ID='ADMIN001',
                Name='Admin User',
                E_Mail='admin@college.edu',
                Designation='Administrator',
                password=generate_password_hash('admin123')
            )
            db.session.add(admin)

        # Add a test faculty member if not exists
        faculty = Staff.query.filter_by(ID='FAC001').first()
        if not faculty:
            faculty = Staff(
                ID='FAC001',
                Name='John Doe',
                E_Mail='john.doe@college.edu',
                Designation='Professor',
                password=generate_password_hash('password10')
            )
            db.session.add(faculty)

        # Add a test student if not exists
        student = Student.query.filter_by(USN='STU001').first()
        if not student:
            student = Student(
                USN='STU001',
                Name='Jane Smith',
                E_Mail='jane.smith@college.edu',
                password=generate_password_hash('password20')
            )
            db.session.add(student)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing database: {e}")

def init_db(app):
    with app.app_context():
        db.create_all()
        # Add initial admin user if it doesn't exist
        from .models import Staff
        from .utils import hash_password
        admin = Staff.query.filter_by(ID='ADMIN001').first()
        if not admin:
            admin = Staff(
                ID='ADMIN001',
                Name='Admin User',
                E_Mail='admin@college.edu',
                Designation='Administrator',
                password=hash_password('admin123')
            )
            db.session.add(admin)
            db.session.commit()

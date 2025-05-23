from flask import Blueprint, request, jsonify, render_template
from flask_login import login_user, logout_user, login_required, current_user
from ..models import Student, Staff
from ..utils import verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login/student', methods=['POST'])
def login_student():
    data = request.get_json()
    student = Student.query.filter_by(USN=data['usn']).first()
    if student and verify_password(data['password'], student.password):
        student.role = 'Student'  # Assign role
        login_user(student)
        return jsonify({'message': 'Student login successful'})
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/login/faculty', methods=['POST'])
def login_faculty():
    data = request.get_json()
    faculty = Staff.query.filter_by(ID=data['id']).first()
    if faculty and verify_password(data['password'], faculty.password):
        faculty.role = 'Faculty'  # Assign role
        login_user(faculty)
        return jsonify({'message': 'Faculty login successful'})
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@auth_bp.route('/user-role', methods=['GET'])
@login_required
def get_user_role():
    if hasattr(current_user, 'USN'):  # Check if the user is a student
        return jsonify({'role': 'Student'})
    elif hasattr(current_user, 'ID'):  # Check if the user is a faculty member
        return jsonify({'role': 'Faculty'})
    return jsonify({'role': 'Unknown'}), 400

@auth_bp.route('/student-login', methods=['GET'])
def student_login():
    return render_template('login/student_login.html')

from flask import Blueprint, request, jsonify, render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user
from ..models import Student, Staff
from ..utils import verify_password
from ..db import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'user_id' not in data or 'password' not in data:
            return jsonify({'error': 'Missing user_id or password'}), 400

        user_id = data['user_id']
        password = data['password']

        # Try to find the user as a student
        user = Student.query.filter_by(USN=user_id).first()
        role = 'Student'
        redirect_url = '/student/dashboard'
        
        # If not found as student, try as faculty
        if not user:
            user = Staff.query.filter_by(ID=user_id).first()
            role = 'Faculty'
            redirect_url = '/faculty/dashboard'

        if user and verify_password(password, user.password):
            login_user(user)
            return jsonify({
                'message': f'{role} login successful',
                'role': role,
                'redirect': redirect_url
            }), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        print(f"Login error: {str(e)}")  # Log the error
        return jsonify({'error': 'An error occurred during login. Please try again.'}), 500

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    if current_user.is_authenticated:
        role = 'Student' if hasattr(current_user, 'USN') else 'Faculty'
        return jsonify({
            'authenticated': True,
            'role': role,
            'redirect': f'/{role.lower()}/dashboard'
        })
    return jsonify({'authenticated': False}), 401

@auth_bp.route('/student-login', methods=['GET'])
def student_login():
    return render_template('/frontend/templates/login/student_login.html')

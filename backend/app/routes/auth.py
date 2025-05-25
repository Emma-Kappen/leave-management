from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from ..models import Student, Staff
import traceback

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
        
    try:
        data = request.get_json()
        if not data or 'user_id' not in data or 'password' not in data:
            return jsonify({'error': 'Missing user_id or password'}), 400

        user_id = data['user_id']
        password = data['password']
        
        # Debug output
        print(f"Login attempt: user_id={user_id}, password={'*' * len(password)}")
        
        # Check if user exists in database
        if user_id.startswith(('S')):
            # Faculty login
            user = Staff.get_by_id(user_id)
            if user and user.verify_password(password):
                login_user(user)
                role = user.role
                redirect_url = f'/{role}/dashboard'
                
                response = jsonify({
                    'message': f'{role} login successful',
                    'role': role,
                    'redirect': redirect_url,
                    'user_id': user_id
                })
                response.headers.add('Access-Control-Allow-Origin', '*')
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                response.set_cookie('user_id', user_id, max_age=86400, httponly=False)
                return response, 200
        else:
            # Student login
            user = Student.get_by_id(user_id)
            if user and user.verify_password(password):
                login_user(user)
                role = 'student'
                redirect_url = '/student/dashboard'
                
                response = jsonify({
                    'message': 'Student login successful',
                    'role': role,
                    'redirect': redirect_url,
                    'user_id': user_id
                })
                response.headers.add('Access-Control-Allow-Origin', '*')
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                response.set_cookie('user_id', user_id, max_age=86400, httponly=False)
                return response, 200
        
        # If we get here, authentication failed
        return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        print(f"Login error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'An error occurred during login. Please try again.'}), 500

@auth_bp.route('/logout', methods=['GET', 'POST', 'OPTIONS'])
def logout():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
        
    try:
        logout_user()
    except Exception as e:
        print(f"Logout error: {str(e)}")
    
    response = jsonify({'message': 'Logged out successfully'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.delete_cookie('user_id')
    return response, 200

@auth_bp.route('/check-auth', methods=['GET', 'OPTIONS'])
def check_auth():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
        
    if current_user.is_authenticated:
        response = jsonify({
            'authenticated': True,
            'role': current_user.role,
            'redirect': f'/{current_user.role}/dashboard',
            'user_id': current_user.get_id()
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 200
        
    response = jsonify({'authenticated': False})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response, 401

@auth_bp.route('/student-login', methods=['GET'])
def student_login():
    return render_template('login/student_login.html')

@auth_bp.route('/faculty-login', methods=['GET'])
def faculty_login():
    return render_template('login/faculty_login.html')

@auth_bp.route('/admin-login', methods=['GET'])
def admin_login():
    return render_template('login/admin_login.html')
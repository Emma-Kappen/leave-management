from flask import Blueprint, request, jsonify, render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from ..db import get_connection
import json
import os

auth_bp = Blueprint('auth', __name__)

def get_user_password(user_id):
    """Get user's password from users.json"""
    try:
        with open(os.path.join('backend', 'users.json'), 'r') as f:
            users = json.load(f)
            return users.get(user_id)
    except Exception as e:
        print(f"Error reading users.json: {e}")
        return None

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'user_id' not in data or 'password' not in data:
            return jsonify({'error': 'Missing user_id or password'}), 400

        user_id = data['user_id']
        password = data['password']
        
        # For admin login with default credentials
        if user_id == 'ADMIN001' and password == 'admin123':
            # Check if admin exists in database
            try:
                connection = get_connection()
                cursor = connection.cursor(dictionary=True)
                
                cursor.execute("SELECT * FROM staff WHERE ID = %s", (user_id,))
                user_data = cursor.fetchone()
                
                # If admin doesn't exist, create it
                if not user_data:
                    cursor.execute(
                        "INSERT INTO staff (ID, Name, E_Mail, Designation) VALUES (%s, %s, %s, %s)",
                        (user_id, "Admin User", "admin@example.com", "Administrator")
                    )
                    connection.commit()
                    
                    # Fetch the newly created admin
                    cursor.execute("SELECT * FROM staff WHERE ID = %s", (user_id,))
                    user_data = cursor.fetchone()
                
                cursor.close()
                connection.close()
                
                # Create user and login
                from .. import User
                user = User(user_id, 'staff', user_data)
                login_user(user)
                
                # Set cookie for user_id
                response = jsonify({
                    'message': 'Admin login successful',
                    'role': 'Admin',
                    'redirect': '/admin/dashboard',
                    'user_id': user_id
                })
                response.set_cookie('user_id', user_id, max_age=86400, httponly=False)
                return response, 200
                
            except Exception as e:
                print(f"Error during admin login: {str(e)}")
                return jsonify({'error': 'Database error during login'}), 500
        
        # Regular login flow
        # Get stored password
        stored_password = get_user_password(user_id)
        if not stored_password:
            return jsonify({'error': 'Invalid credentials'}), 401

        # Simple password check (not using hash verification)
        if stored_password != password:
            return jsonify({'error': 'Invalid credentials'}), 401

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Check if user exists in database
        if user_id.startswith(('ADMIN', 'FAC')):
            cursor.execute("SELECT * FROM staff WHERE ID = %s", (user_id,))
            user_data = cursor.fetchone()
            role = 'Admin' if user_id.startswith('ADMIN') else 'Faculty'
            redirect_url = '/admin/dashboard' if role == 'Admin' else '/faculty/dashboard'
        else:
            cursor.execute("SELECT * FROM student WHERE USN = %s", (user_id,))
            user_data = cursor.fetchone()
            role = 'Student'
            redirect_url = '/student/dashboard'

        cursor.close()
        connection.close()

        if user_data:
            from .. import User
            user = User(user_id, role.lower(), user_data)
            login_user(user)
            
            # Set cookie for user_id
            response = jsonify({
                'message': f'{role} login successful',
                'role': role,
                'redirect': redirect_url,
                'user_id': user_id
            })
            response.set_cookie('user_id', user_id, max_age=86400, httponly=False)
            return response, 200
        
        return jsonify({'error': 'User not found in database'}), 401

    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': 'An error occurred during login. Please try again.'}), 500

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'role': current_user.user_type,
            'redirect': f'/{current_user.user_type}/dashboard'
        })
    return jsonify({'authenticated': False}), 401

@auth_bp.route('/student-login', methods=['GET'])
def student_login():
    return render_template('login/student_login.html')
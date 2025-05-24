from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from datetime import datetime
from ..db import get_connection
import json

student_bp = Blueprint('student', __name__)

def require_role(role):
    """Check if the current user has the required role"""
    if not current_user.is_authenticated or current_user.user_type != role.lower():
        return jsonify({'error': 'Access denied'}), 403
    return None

@student_bp.before_request
@login_required
def restrict_to_students():
    if current_user.user_type != 'student':
        return jsonify({'error': 'Access denied'}), 403

@student_bp.route('/apply-leave', methods=['POST'])
@login_required
def apply_leave():
    data = request.get_json()

    # Validate required fields
    required_fields = ['leave_type', 'reason', 'start_date', 'end_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"'{field}' is required"}), 400

    # Validate date formats
    try:
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    # Validate date ranges
    if start_date < datetime.now():
        return jsonify({'error': 'Start_Date must be after the current date.'}), 400
    if end_date < start_date:
        return jsonify({'error': 'End_Date cannot be before Start_Date.'}), 400

    # Create the leave application
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            INSERT INTO leave_requests 
            (user_id, start_date, end_date, reason, status) 
            VALUES (%s, %s, %s, %s, %s)
        """, (
            current_user.id, 
            start_date.strftime('%Y-%m-%d'), 
            end_date.strftime('%Y-%m-%d'), 
            data['reason'], 
            'pending'
        ))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'Leave application submitted.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/leave-status', methods=['GET'])
@login_required
def leave_status():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM leave_requests 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """, (current_user.id,))
        
        leaves = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return jsonify(leaves), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/attendance', methods=['GET'])
@login_required
def get_attendance():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if attendance table exists
        cursor.execute("""
            SELECT COUNT(*) as count FROM information_schema.tables 
            WHERE table_schema = DATABASE() 
            AND table_name = 'attendance'
        """)
        
        if cursor.fetchone()['count'] == 0:
            # Create sample attendance data if table doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id VARCHAR(10),
                    subject_code VARCHAR(10),
                    subject_name VARCHAR(100),
                    classes_taken INT DEFAULT 0,
                    classes_attended INT DEFAULT 0
                )
            """)
            
            # Insert sample data for the current student
            cursor.execute("""
                INSERT INTO attendance 
                (student_id, subject_code, subject_name, classes_taken, classes_attended)
                VALUES 
                (%s, 'CS101', 'Computer Science Basics', 30, 28),
                (%s, 'MATH201', 'Advanced Mathematics', 25, 20),
                (%s, 'PHY101', 'Physics Fundamentals', 20, 18)
            """, (current_user.id, current_user.id, current_user.id))
            
            connection.commit()
        
        # Fetch attendance data
        cursor.execute("""
            SELECT subject_code, subject_name, classes_taken, classes_attended
            FROM attendance
            WHERE student_id = %s
        """, (current_user.id,))
        
        attendance_records = cursor.fetchall()
        
        # Calculate percentages
        for record in attendance_records:
            if record['classes_taken'] > 0:
                record['attendance_percentage'] = round((record['classes_attended'] / record['classes_taken']) * 100, 2)
            else:
                record['attendance_percentage'] = 0
        
        cursor.close()
        connection.close()
        
        return jsonify(attendance_records), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@student_bp.route('/dashboard', methods=['GET'])
@login_required
def student_dashboard():
    return render_template('student/dashboard.html')
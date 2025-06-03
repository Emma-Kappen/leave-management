from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from ..models import Student
from ..db import execute_query
from datetime import datetime
import os

student_bp = Blueprint('student', __name__)

# Helper function to get current user ID
def get_current_user_id():
    # Try to get from current_user if authenticated
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        return current_user.id
    
    # Otherwise get from request
    user_id = request.args.get('user_id') or request.cookies.get('user_id')
    return user_id

@student_bp.route('/user-info', methods=['GET'])
def get_user_info():
    user_id = get_current_user_id()
    
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        # Query the database for student info
        student = Student.get_by_id(user_id)
        
        if student:
            return jsonify(student.to_dict()), 200
        else:
            return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/leave-status', methods=['GET'])
def leave_status():
    user_id = get_current_user_id()
    
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        # Query the database for leave applications
        student = Student.get_by_id(user_id)
        if student:
            leaves = student.get_leaves()
            return jsonify([leave.to_dict() for leave in leaves]), 200
        else:
            return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/attendance', methods=['GET'])
def get_attendance():
    user_id = get_current_user_id()
    
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        # Query the database for attendance records
        student = Student.get_by_id(user_id)
        if student:
            attendance_records = student.get_attendance()
            return jsonify([record.to_dict() for record in attendance_records]), 200
        else:
            return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/subjects', methods=['GET'])
def get_subjects():
    user_id = get_current_user_id()
    
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        # Query to get subjects for the student from both Attendance and Teaches tables
        query = """
        SELECT DISTINCT s.Code, s.Title 
        FROM Subject s
        LEFT JOIN Attendance a ON s.Code = a.Subject_Code
        LEFT JOIN Teaches t ON s.Code = t.Subject_Code
        WHERE a.USN = %s OR t.USN = %s
        ORDER BY s.Title
        """
        
        subjects = execute_query(query, (user_id, user_id))
        
        if subjects:
            return jsonify(subjects), 200
        else:
            # Return empty list if no subjects found
            return jsonify([]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/apply-leave', methods=['POST'])
def apply_leave():
    user_id = get_current_user_id()
    
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['leaveType', 'subject', 'startDate', 'endDate', 'reason']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Insert leave application into database
        query = """
        INSERT INTO `Leave` (Applicant_ID, Leave_Type, Reason, Start_Date, End_Date, Submission_Date, Approval_Status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        execute_query(
            query, 
            (
                user_id, 
                data['leaveType'], 
                data['reason'], 
                data['startDate'], 
                data['endDate'], 
                datetime.now(),
                'PENDING'
            ),
            fetch=False
        )
        
        return jsonify({'message': 'Leave application submitted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/apply-leave-with-file', methods=['POST'])
def apply_leave_with_file():
    user_id = get_current_user_id()
    
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        # Get form data
        leave_type = request.form.get('leaveType')
        subject = request.form.get('subject')
        start_date = request.form.get('startDate')
        end_date = request.form.get('endDate')
        reason = request.form.get('reason')
        
        # Validate required fields
        if not all([leave_type, subject, start_date, end_date, reason]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Handle file upload if present
        file_path = None
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename:
                # Create uploads directory if it doesn't exist
                upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Save file with unique name
                filename = f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
        
        # Insert leave application into database
        query = """
        INSERT INTO `Leave` (Applicant_ID, Leave_Type, Reason, Start_Date, End_Date, Submission_Date, Approval_Status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        execute_query(
            query, 
            (
                user_id, 
                leave_type, 
                reason, 
                start_date, 
                end_date, 
                datetime.now(),
                'PENDING'
            ),
            fetch=False
        )
        
        return jsonify({'message': 'Leave application submitted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/dashboard', methods=['GET'])
@login_required
def student_dashboard():
    return render_template('student/dashboard.html')

@student_bp.route('/leave/<int:leave_id>', methods=['GET'])
@login_required
def leave_detail(leave_id):
    user_id = get_current_user_id()
    
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        # Query the database for leave details
        query = """
        SELECT l.*
        FROM `Leave` l
        WHERE l.Leave_ID = %s AND l.Applicant_ID = %s
        """
        
        result = execute_query(query, (leave_id, user_id))
        
        if result:
            return render_template('student/leave_detail.html', leave=result[0])
        else:
            return render_template('error/404.html', message="Leave request not found"), 404
    except Exception as e:
        return render_template('error/500.html', message=str(e)), 500

@student_bp.route('/apply-leave-page', methods=['GET'])
@login_required
def apply_leave_page():
    return render_template('student/apply_leave.html')

@student_bp.route('/leave-status-page', methods=['GET'])
@login_required
def leave_status_page():
    return render_template('student/leave_status.html')
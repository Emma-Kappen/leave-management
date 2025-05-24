from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..db import get_connection
from datetime import datetime

faculty_bp = Blueprint('faculty', __name__)

@faculty_bp.before_request
@login_required
def restrict_to_faculty():
    if current_user.user_type != 'staff' or not current_user.data.get('Designation') == 'Professor':
        return jsonify({'error': 'Access denied'}), 403

@faculty_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('faculty/faculty_dashboard.html')

@faculty_bp.route('/leave-requests', methods=['GET'])
@login_required
def leave_requests():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Get all pending leave requests
        cursor.execute("""
            SELECT lr.*, 
                   CASE 
                       WHEN lr.user_id LIKE 'STU%' THEN s.Name
                       ELSE st.Name
                   END as applicant_name
            FROM leave_requests lr
            LEFT JOIN student s ON lr.user_id = s.USN
            LEFT JOIN staff st ON lr.user_id = st.ID
            WHERE lr.status = 'pending'
            ORDER BY lr.created_at DESC
        """)
        
        pending_leaves = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return jsonify(pending_leaves), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@faculty_bp.route('/leave-requests/<int:leave_id>', methods=['POST'])
@login_required
def update_leave_status(leave_id):
    data = request.get_json()

    # Validate required fields
    if 'status' not in data:
        return jsonify({'error': "'status' is required"}), 400

    # Validate status value
    if data['status'] not in ['approved', 'rejected']:
        return jsonify({'error': 'Invalid status. Must be approved or rejected.'}), 400

    # Update the leave status
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Update leave request status
        cursor.execute("""
            UPDATE leave_requests 
            SET status = %s 
            WHERE id = %s
        """, (data['status'], leave_id))
        
        # Record the approver
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leave_approvers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                leave_id INT,
                approver_id VARCHAR(10),
                approval_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            INSERT INTO leave_approvers 
            (leave_id, approver_id) 
            VALUES (%s, %s)
        """, (leave_id, current_user.id))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'message': f"Leave {data['status']} successfully."}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@faculty_bp.route('/leave-history', methods=['GET'])
@login_required
def leave_history():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Create leave_approvers table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leave_approvers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                leave_id INT,
                approver_id VARCHAR(10),
                approval_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Get all leave requests processed by this faculty
        cursor.execute("""
            SELECT lr.*, 
                   CASE 
                       WHEN lr.user_id LIKE 'STU%' THEN s.Name
                       ELSE st.Name
                   END as applicant_name,
                   la.approval_date
            FROM leave_requests lr
            JOIN leave_approvers la ON lr.id = la.leave_id
            LEFT JOIN student s ON lr.user_id = s.USN
            LEFT JOIN staff st ON lr.user_id = st.ID
            WHERE la.approver_id = %s
            ORDER BY la.approval_date DESC
        """, (current_user.id,))
        
        history = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return jsonify(history), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
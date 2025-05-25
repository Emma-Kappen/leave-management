from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Staff
from ..db import execute_query
from datetime import datetime, date
import os

faculty_bp = Blueprint('faculty', __name__)

# Helper function to get current user ID
def get_current_user_id():
    # Try to get from current_user if authenticated
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        return current_user.id
    
    # Otherwise get from request
    user_id = request.args.get('user_id') or request.cookies.get('user_id')
    return user_id

@faculty_bp.route('/user-info', methods=['GET'])
def get_user_info():
    user_id = get_current_user_id()
    
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        # Query the database for faculty info
        query = "SELECT ID, Name, E_Mail, Designation FROM Staff WHERE ID = %s"
        result = execute_query(query, (user_id,))
        
        if result:
            faculty_data = result[0]
            return jsonify({
                'id': faculty_data['ID'],
                'name': faculty_data['Name'],
                'email': faculty_data['E_Mail'],
                'designation': faculty_data['Designation']
            }), 200
        else:
            return jsonify({'error': 'Faculty not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@faculty_bp.route('/all-leave-requests', methods=['GET'])
@login_required
def all_leave_requests():
    user_id = get_current_user_id()
    
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        # Query to get all leave requests for subjects taught by this faculty
        # Ordered by status (PENDING first) and then by submission date (newest first)
        query = """
        SELECT l.Leave_ID, l.Applicant_ID, s.Name AS Student_Name, 
               l.Leave_Type, l.Start_Date, l.End_Date, l.Submission_Date, l.Approval_Status,
               sub.Code AS Subject_Code, sub.Title AS Subject_Title
        FROM `Leave` l
        JOIN Student s ON l.Applicant_ID = s.USN
        JOIN Teaches t ON s.USN = t.USN
        JOIN Subject sub ON t.Subject_Code = sub.Code
        WHERE t.ID = %s
        ORDER BY 
            CASE WHEN l.Approval_Status = 'PENDING' THEN 0 ELSE 1 END,
            l.Submission_Date DESC
        """
        
        result = execute_query(query, (user_id,))
        
        if result:
            return jsonify(result), 200
        else:
            # Return empty list if no leave requests
            return jsonify([]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@faculty_bp.route('/pending-leaves', methods=['GET'])
@login_required
def pending_leaves():
    user_id = get_current_user_id()
    
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        # Query to get pending leave requests for subjects taught by this faculty
        query = """
        SELECT l.Leave_ID, l.Applicant_ID, s.Name AS Student_Name, 
               l.Leave_Type, l.Start_Date, l.End_Date, l.Reason,
               sub.Code AS Subject_Code, sub.Title AS Subject_Title
        FROM `Leave` l
        JOIN Student s ON l.Applicant_ID = s.USN
        JOIN Teaches t ON s.USN = t.USN
        JOIN Subject sub ON t.Subject_Code = sub.Code
        WHERE t.ID = %s AND l.Approval_Status = 'PENDING'
        ORDER BY l.Start_Date ASC
        """
        
        result = execute_query(query, (user_id,))
        
        if result:
            return jsonify(result), 200
        else:
            # Return empty list if no pending leaves
            return jsonify([]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@faculty_bp.route('/assigned-students', methods=['GET'])
@login_required
def assigned_students():
    user_id = get_current_user_id()
    
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        # Query to get all students assigned to this faculty
        query = """
        SELECT DISTINCT s.USN, s.Name, s.E_Mail, d.Name AS Department_Name,
               sub.Code AS Subject_Code, sub.Title AS Subject_Title
        FROM Student s
        JOIN Teaches t ON s.USN = t.USN
        JOIN Subject sub ON t.Subject_Code = sub.Code
        JOIN Department d ON s.Dept_ID = d.ID
        WHERE t.ID = %s
        ORDER BY s.Name
        """
        
        result = execute_query(query, (user_id,))
        
        if result:
            return jsonify(result), 200
        else:
            # Return empty list if no students found
            return jsonify([]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@faculty_bp.route('/student-details')
@login_required
def student_details():
    user_id = get_current_user_id()
    
    try:
        # Query to get all students assigned to this faculty
        query = """
        SELECT DISTINCT s.USN, s.Name, s.E_Mail, d.Name AS Department_Name,
               sub.Code AS Subject_Code, sub.Title AS Subject_Title
        FROM Student s
        JOIN Teaches t ON s.USN = t.USN
        JOIN Subject sub ON t.Subject_Code = sub.Code
        JOIN Department d ON s.Dept_ID = d.ID
        WHERE t.ID = %s
        ORDER BY s.Name
        """
        
        students = execute_query(query, (user_id,))
        
        # Get faculty info
        faculty_query = "SELECT Name, Designation FROM Staff WHERE ID = %s"
        faculty_info = execute_query(faculty_query, (user_id,))
        
        if faculty_info:
            faculty_name = faculty_info[0]['Name']
            faculty_designation = faculty_info[0]['Designation']
        else:
            faculty_name = "Faculty"
            faculty_designation = ""
        
        return render_template('faculty/student_details.html', 
                              students=students, 
                              faculty_name=faculty_name,
                              faculty_designation=faculty_designation)
    except Exception as e:
        print(f"Error fetching student details: {str(e)}")
        return render_template('faculty/student_details.html', students=[], error=str(e))

@faculty_bp.route('/review-leaves')
@login_required
def review_leaves():
    user_id = get_current_user_id()
    
    try:
        # Query to get all leave requests (pending, approved, rejected) for subjects taught by this faculty
        query = """
        SELECT l.Leave_ID, l.Applicant_ID, s.Name AS Student_Name, 
               l.Leave_Type, l.Start_Date, l.End_Date, l.Approval_Status,
               sub.Code AS Subject_Code, sub.Title AS Subject_Title
        FROM `Leave` l
        JOIN Student s ON l.Applicant_ID = s.USN
        JOIN Teaches t ON s.USN = t.USN
        JOIN Subject sub ON t.Subject_Code = sub.Code
        WHERE t.ID = %s
        ORDER BY l.Submission_Date DESC
        """
        
        leave_requests = execute_query(query, (user_id,))
        
        return render_template('faculty/review_leaves.html', leave_requests=leave_requests)
    except Exception as e:
        print(f"Error fetching leave requests: {str(e)}")
        return render_template('faculty/review_leaves.html', leave_requests=[], error=str(e))

@faculty_bp.route('/leave/<int:leave_id>')
@login_required
def leave_detail(leave_id):
    user_id = get_current_user_id()
    
    try:
        # Query to get detailed leave request information
        query = """
        SELECT l.Leave_ID, l.Applicant_ID, s.Name AS Student_Name, s.E_Mail AS Student_Email,
               l.Leave_Type, l.Reason, l.Start_Date, l.End_Date, l.Submission_Date, l.Approval_Status,
               sub.Code AS Subject_Code, sub.Title AS Subject_Title,
               d.Name AS Department_Name
        FROM `Leave` l
        JOIN Student s ON l.Applicant_ID = s.USN
        JOIN Department d ON s.Dept_ID = d.ID
        JOIN Teaches t ON s.USN = t.USN
        JOIN Subject sub ON t.Subject_Code = sub.Code
        WHERE l.Leave_ID = %s AND t.ID = %s
        """
        
        result = execute_query(query, (leave_id, user_id))
        
        if not result:
            return render_template('faculty/leave_review.html', error="Leave request not found or you don't have permission to view it")
        
        leave_data = result[0]
        
        # Check if leave is in the future
        today = date.today()
        start_date = leave_data['Start_Date']
        is_future_leave = start_date > today
        
        # Check if there's an attachment
        attachment_path = None
        uploads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')
        possible_attachment = os.path.join(uploads_dir, f"{leave_data['Applicant_ID']}_{leave_id}.pdf")
        
        if os.path.exists(possible_attachment):
            attachment_path = f"/uploads/{leave_data['Applicant_ID']}_{leave_id}.pdf"
        
        # Get approver information if the leave has been reviewed
        approver_info = None
        if leave_data['Approval_Status'] in ['APPROVED', 'REJECTED']:
            query = """
            SELECT la.Decision_Date, s.Name AS Approver_Name
            FROM Leave_Approver la
            JOIN Staff s ON la.Approver_ID = s.ID
            WHERE la.Leave_ID = %s
            """
            
            approver_result = execute_query(query, (leave_id,))
            if approver_result:
                approver_info = approver_result[0]
        
        return render_template('faculty/leave_review.html', 
                              leave=leave_data, 
                              attachment_path=attachment_path,
                              approver_info=approver_info,
                              is_future_leave=is_future_leave)
    except Exception as e:
        print(f"Error fetching leave details: {str(e)}")
        return render_template('faculty/leave_review.html', error=str(e))

@faculty_bp.route('/leave/<int:leave_id>/review', methods=['POST'])
@login_required
def review_leave(leave_id):
    user_id = get_current_user_id()
    
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        # Get action from form data or JSON
        action = None
        if request.is_json:
            data = request.get_json()
            action = data.get('action')
        else:
            action = request.form.get('action')
        
        if not action or action not in ['approve', 'reject', 'reset']:
            return jsonify({'error': 'Invalid action'}), 400
        
        # Map action to status
        if action == 'approve':
            status = 'APPROVED'
        elif action == 'reject':
            status = 'REJECTED'
        else:  # reset
            status = 'PENDING'
        
        # Check if leave is in the future
        query = "SELECT Start_Date FROM `Leave` WHERE Leave_ID = %s"
        result = execute_query(query, (leave_id,))
        
        if not result:
            return redirect(url_for('faculty.leave_detail', leave_id=leave_id, error="Leave request not found"))
        
        start_date = result[0]['Start_Date']
        today = date.today()
        
        if start_date <= today and action != 'approve':
            return redirect(url_for('faculty.leave_detail', leave_id=leave_id, error="Cannot modify status for past or current leave requests"))
        
        # Update leave status
        query = """
        UPDATE `Leave` 
        SET Approval_Status = %s
        WHERE Leave_ID = %s
        """
        
        execute_query(query, (status, leave_id), fetch=False)
        
        # Handle approver information
        if action == 'reset':
            # Remove from Leave_Approver table if resetting to pending
            query = "DELETE FROM Leave_Approver WHERE Leave_ID = %s"
            execute_query(query, (leave_id,), fetch=False)
        else:
            # Insert into Leave_Approver table
            query = """
            INSERT INTO Leave_Approver (Leave_ID, Approver_ID, Decision_Date)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE Approver_ID = %s, Decision_Date = %s
            """
            
            now = datetime.now()
            execute_query(query, (leave_id, user_id, now, user_id, now), fetch=False)
        
        # Redirect back to the leave detail page
        action_message = "reset to pending" if action == "reset" else f"{action}d"
        return redirect(url_for('faculty.leave_detail', leave_id=leave_id, success=f'Leave request {action_message} successfully'))
    
    except Exception as e:
        print(f"Error reviewing leave: {str(e)}")
        return redirect(url_for('faculty.leave_detail', leave_id=leave_id, error=str(e)))

@faculty_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    user_id = get_current_user_id()
    
    try:
        # Get faculty info
        faculty_query = "SELECT Name, Designation FROM Staff WHERE ID = %s"
        faculty_info = execute_query(faculty_query, (user_id,))
        
        if faculty_info:
            faculty_name = faculty_info[0]['Name']
            faculty_designation = faculty_info[0]['Designation']
        else:
            faculty_name = "Faculty"
            faculty_designation = ""
        
        # Get assigned subjects
        subjects_query = """
        SELECT DISTINCT sub.Code, sub.Title
        FROM Subject sub
        JOIN Teaches t ON sub.Code = t.Subject_Code
        WHERE t.ID = %s
        ORDER BY sub.Title
        """
        
        subjects = execute_query(subjects_query, (user_id,))
        
        # Get student count
        student_count_query = """
        SELECT COUNT(DISTINCT s.USN) as student_count
        FROM Student s
        JOIN Teaches t ON s.USN = t.USN
        WHERE t.ID = %s
        """
        
        student_count_result = execute_query(student_count_query, (user_id,))
        student_count = student_count_result[0]['student_count'] if student_count_result else 0
        
        # Query to get all leave requests for subjects taught by this faculty
        # Ordered by status (PENDING first) and then by submission date (newest first)
        leave_query = """
        SELECT l.Leave_ID, l.Applicant_ID, s.Name AS Student_Name, 
               l.Leave_Type, l.Start_Date, l.End_Date, l.Submission_Date, l.Approval_Status,
               sub.Code AS Subject_Code, sub.Title AS Subject_Title
        FROM `Leave` l
        JOIN Student s ON l.Applicant_ID = s.USN
        JOIN Teaches t ON s.USN = t.USN
        JOIN Subject sub ON t.Subject_Code = sub.Code
        WHERE t.ID = %s
        ORDER BY 
            CASE WHEN l.Approval_Status = 'PENDING' THEN 0 ELSE 1 END,
            l.Submission_Date DESC
        LIMIT 10
        """
        
        leave_requests = execute_query(leave_query, (user_id,))
        
        return render_template('faculty/faculty_dashboard.html', 
                              faculty_name=faculty_name,
                              faculty_designation=faculty_designation,
                              subjects=subjects,
                              student_count=student_count,
                              leave_requests=leave_requests)
    except Exception as e:
        print(f"Error fetching dashboard data: {str(e)}")
        return render_template('faculty/faculty_dashboard.html', 
                              leave_requests=[], 
                              subjects=[],
                              student_count=0,
                              error=str(e))
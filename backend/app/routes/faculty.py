from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import db, Leave, LeaveApprover, Student
from app.utils import current_user_id, require_role
from flask_login import login_required, current_user

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')

@faculty_bp.before_request
@login_required
def restrict_to_faculty():
    require_role('Faculty')

@faculty_bp.route('/dashboard')
def dashboard():
    return render_template('faculty/dashboard.html')

@faculty_bp.route('/leave-requests', methods=['GET'])
def leave_requests():
    try:
        pending_leaves = Leave.query.filter_by(Approval_Status='PENDING').all()
        leave_data = [
            {
                "leave_id": leave.Leave_ID,
                "student_name": leave.Applicant_ID,  # Replace with actual student name if needed
                "leave_type": leave.Leave_Type,
                "subject": "-",  # Replace with actual subject if applicable
                "start_date": leave.Start_Date.strftime('%Y-%m-%d'),
                "end_date": leave.End_Date.strftime('%Y-%m-%d'),
                "reason": leave.Reason,
                "status": leave.Approval_Status
            }
            for leave in pending_leaves
        ]
        return jsonify(leave_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@faculty_bp.route('/leave/<int:leave_id>', methods=['GET', 'POST'])
def view_leave_request(leave_id):
    leave = Leave.query.get_or_404(leave_id)
    if request.method == 'POST':
        action = request.form.get('action')
        if action in ['APPROVED', 'REJECTED']:
            leave.Approval_Status = action
            approver = LeaveApprover(Leave_ID=leave_id, Approver_ID=current_user_id())
            db.session.add(approver)
            db.session.commit()
            flash(f"Leave {action.lower()} successfully.")
            return redirect(url_for('faculty.leave_requests'))
    return render_template('faculty/view_request_detail.html', leave=leave)

@faculty_bp.route('/leave-history', methods=['GET'])
def leave_history():
    try:
        # Fetch leave requests processed by the logged-in faculty
        leave_history = Leave.query.join(LeaveApprover, Leave.Leave_ID == LeaveApprover.Leave_ID) \
            .filter(LeaveApprover.Approver_ID == current_user.id).all()
        
        history_data = [
            {
                "student_name": leave.Applicant_ID,  # Replace with actual student name if needed
                "leave_type": leave.Leave_Type,
                "subject": "-",  # Replace with actual subject if applicable
                "start_date": leave.Start_Date.strftime('%Y-%m-%d'),
                "end_date": leave.End_Date.strftime('%Y-%m-%d'),
                "reason": leave.Reason,
                "status": leave.Approval_Status,
                "action_taken_on": leave.Submission_Date.strftime('%Y-%m-%d %H:%M:%S')
            }
            for leave in leave_history
        ]
        return jsonify(history_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@faculty_bp.route('/leave-requests/<int:leave_id>', methods=['POST'])
def update_leave_status(leave_id):
    data = request.get_json()

    # Validate required fields
    if 'status' not in data:
        return jsonify({'error': "'status' is required"}), 400

    # Validate status value
    if data['status'] not in ['APPROVED', 'REJECTED']:
        return jsonify({'error': 'Invalid status. Must be APPROVED or REJECTED.'}), 400

    # Update the leave status
    try:
        leave = Leave.query.get_or_404(leave_id)
        leave.Approval_Status = data['status']
        approver = LeaveApprover(Leave_ID=leave_id, Approver_ID=current_user.id)
        db.session.add(approver)
        db.session.commit()
        return jsonify({'message': f"Leave {data['status'].lower()} successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

from flask import Blueprint, request, jsonify
from app.models import db, Leave
from flask_login import login_required, current_user
from datetime import datetime
from app.utils import require_role

student_bp = Blueprint('student', __name__)

@student_bp.before_request
@login_required
def restrict_to_students():
    require_role('Student')

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
        new_leave = Leave(
            Applicant_ID=current_user.id,
            Leave_Type=data['leave_type'],
            Reason=data['reason'],
            Start_Date=start_date,
            End_Date=end_date
        )
        db.session.add(new_leave)
        db.session.commit()
        return jsonify({'message': 'Leave application submitted.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@student_bp.route('/leave-status', methods=['GET'])
@login_required
def leave_status():
    require_role('Student')
    leaves = Leave.query.filter_by(Applicant_ID=current_user.id).all()
    return jsonify([leave.to_dict() for leave in leaves])

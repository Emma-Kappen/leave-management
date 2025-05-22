from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import db, Student, Staff, Leave, Department
from app.utils import is_admin_user, hash_password, require_role
from flask_login import login_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
def restrict_to_admins():
    require_role('Admin')

@admin_bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/students', methods=['GET', 'POST'])
def view_students():
    if request.method == 'POST':
        data = request.get_json()
        try:
            new_student = Student(
                USN=data['usn'],
                Name=data['name'],
                E_Mail=data['email'],
                Join_Date=data.get('join_date'),
                Dept_ID=data.get('dept_id'),
                password=hash_password(data['password'])
            )
            db.session.add(new_student)
            db.session.commit()
            return jsonify({'message': 'Student added successfully.'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 400

    students = Student.query.all()
    return render_template('admin/edit_students.html', students=students)

@admin_bp.route('/faculty', methods=['POST'])
def add_faculty():
    data = request.get_json()
    try:
        new_faculty = Staff(
            ID=data['id'],  # Matches 'id' from frontend
            Name=data['name'],  # Matches 'name' from frontend
            E_Mail=data['email'],  # Matches 'email' from frontend
            Designation=data.get('designation'),  # Matches 'designation' from frontend
            Supervisor_ID=data.get('supervisor_id'),  # Matches 'supervisor_id' from frontend
            password=hash_password(data['password'])  # Securely hash the password
        )
        db.session.add(new_faculty)
        db.session.commit()
        return jsonify({'message': 'Faculty added successfully.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@admin_bp.route('/leaves', methods=['GET'])
def get_all_leaves():
    try:
        leaves = Leave.query.all()
        leave_data = [
            {
                "user_type": "Student",  # Assuming all leaves are from students
                "name": leave.Applicant_ID,  # Replace with actual name if needed
                "leave_type": leave.Leave_Type,
                "subject": "-",  # Replace with actual subject if applicable
                "start_date": leave.Start_Date.strftime('%Y-%m-%d'),
                "end_date": leave.End_Date.strftime('%Y-%m-%d'),
                "reason": leave.Reason,
                "status": leave.Approval_Status,
                "submitted_on": leave.Submission_Date.strftime('%Y-%m-%d %H:%M:%S')
            }
            for leave in leaves
        ]
        return jsonify(leave_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/departments-users', methods=['GET'])
def get_departments_and_users():
    try:
        departments = Department.query.all()
        department_data = []
        for department in departments:
            users = []
            # Fetch students in the department
            students = Student.query.filter_by(Dept_ID=department.ID).all()
            users.extend([{"name": student.Name, "role": "Student"} for student in students])
            # Fetch faculty in the department
            faculty = Staff.query.filter(Staff.Designation.isnot(None)).all()
            users.extend([{"name": staff.Name, "role": "Faculty"} for staff in faculty])
            department_data.append({"name": department.Name, "users": users})
        return jsonify(department_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Check if the user is a student
        user = Student.query.filter_by(USN=user_id).first()
        if user:
            return jsonify({
                "user_id": user.USN,
                "name": user.Name,
                "email": user.E_Mail,
                "role": "student",
                "department": user.Dept_ID
            }), 200

        # Check if the user is a faculty member
        user = Staff.query.filter_by(ID=user_id).first()
        if user:
            return jsonify({
                "user_id": user.ID,
                "name": user.Name,
                "email": user.E_Mail,
                "role": "faculty",
                "department": None  # Faculty may not have a department
            }), 200

        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"'{field}' is required"}), 400

    # Validate email format
    if '@' not in data['email']:
        return jsonify({'error': 'Invalid email format'}), 400

    # Update the user
    try:
        user = Student.query.filter_by(USN=user_id).first() or Staff.query.filter_by(ID=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user.Name = data['name']
        user.E_Mail = data['email']
        if 'dept_id' in data:
            user.Dept_ID = data['dept_id']
        db.session.commit()
        return jsonify({'message': 'User updated successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        students = Student.query.all()
        faculty = Staff.query.all()

        users = [
            {
                "user_id": student.USN,
                "name": student.Name,
                "email": student.E_Mail,
                "role": "Student",
                "department": student.Dept_ID
            }
            for student in students
        ] + [
            {
                "user_id": staff.ID,
                "name": staff.Name,
                "email": staff.E_Mail,
                "role": "Faculty",
                "department": None  # Faculty may not have a department
            }
            for staff in faculty
        ]

        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # Check if the user is a student
        user = Student.query.filter_by(USN=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "Student deleted successfully"}), 200

        # Check if the user is a faculty member
        user = Staff.query.filter_by(ID=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "Faculty deleted successfully"}), 200

        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()

    # Validate required fields
    required_fields = ['usn', 'name', 'email', 'password', 'dept_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"'{field}' is required"}), 400

    # Validate email format
    if '@' not in data['email']:
        return jsonify({'error': 'Invalid email format'}), 400

    # Create the student
    try:
        new_student = Student(
            USN=data['usn'],
            Name=data['name'],
            E_Mail=data['email'],
            Dept_ID=data['dept_id'],
            password=hash_password(data['password'])
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'message': 'Student added successfully.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

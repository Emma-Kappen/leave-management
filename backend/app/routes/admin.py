from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from ..db import execute_query
from ..utils import verify_password
import traceback

admin_bp = Blueprint('admin', __name__)

class Admin:
    """Admin model for authentication and data access."""
    
    def __init__(self, admin_id, name, email, password=None):
        self.admin_id = admin_id
        self.name = name
        self.email = email
        self.password = password
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.admin_id)
    
    @property
    def role(self):
        return 'admin'
    
    @property
    def id(self):
        return self.admin_id
    
    @staticmethod
    def get_by_email(email):
        """Get admin by email."""
        query = "SELECT * FROM Admin WHERE E_Mail = %s"
        result = execute_query(query, (email,))
        if result:
            admin_data = result[0]
            return Admin(
                admin_id=admin_data['ID'],
                name=admin_data['Name'],
                email=admin_data['E_Mail'],
                password=admin_data['Password']
            )
        return None
    
    @staticmethod
    def get_by_id(admin_id):
        """Get admin by ID."""
        query = "SELECT * FROM Admin WHERE ID = %s"
        result = execute_query(query, (admin_id,))
        if result:
            admin_data = result[0]
            return Admin(
                admin_id=admin_data['ID'],
                name=admin_data['Name'],
                email=admin_data['E_Mail'],
                password=admin_data['Password']
            )
        return None
    
    def verify_password(self, password):
        """Verify the password."""
        return verify_password(self.password, password)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('auth.index'))
    
    return render_template('admin/dashboard.html')

@admin_bp.route('/users')
@login_required
def manage_users():
    if current_user.role != 'admin':
        return redirect(url_for('auth.index'))
    
    return render_template('admin/manage_users.html')

@admin_bp.route('/departments')
@login_required
def manage_departments():
    if current_user.role != 'admin':
        return redirect(url_for('auth.index'))
    
    return render_template('admin/department_view.html')

@admin_bp.route('/subjects')
@login_required
def manage_subjects():
    if current_user.role != 'admin':
        return redirect(url_for('auth.index'))
    
    return render_template('admin/subjects.html')

@admin_bp.route('/reports')
@login_required
def view_reports():
    if current_user.role != 'admin':
        return redirect(url_for('auth.index'))
    
    return render_template('admin/reports.html')
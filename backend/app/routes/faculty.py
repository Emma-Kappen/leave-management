from flask import Blueprint, render_template
from flask_login import login_required

faculty_bp = Blueprint('faculty', __name__)

@faculty_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('faculty/faculty_dashboard.html')
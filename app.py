from flask import Flask, render_template, send_from_directory, redirect, url_for
from backend.app import create_app
import os

app = create_app()

@app.route('/')
def index():
    return render_template('login/index.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')

@app.route('/admin/department_view')
def admin_department_view():
    return render_template('admin/department_view.html')

@app.route('/admin/manage_users')
def admin_manage_users():
    return render_template('admin/manage_users.html')

@app.route('/admin/all_leaves')
def admin_all_leaves():
    return render_template('admin/all_leaves.html')

if __name__ == '__main__':
    app.run(debug=True)
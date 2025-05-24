from flask import request, jsonify
import traceback

def register_user_management_routes(app, get_connection, handle_preflight):
    @app.route('/admin/users/<user_id>', methods=['DELETE', 'OPTIONS'])
    def delete_user(user_id):
        if request.method == 'OPTIONS':
            return handle_preflight()
            
        try:
            print(f"Deleting user: {user_id}")
            admin_id = request.cookies.get('user_id')
            
            if not admin_id or not admin_id.startswith('ADMIN'):
                return jsonify({'error': 'Unauthorized access'}), 403
                
            conn = get_connection()
            cursor = conn.cursor()
            
            # Determine user type based on ID prefix
            if user_id.startswith('FAC'):
                # Delete from Staff table
                cursor.execute("DELETE FROM Staff WHERE ID = %s", (user_id,))
            elif user_id.startswith('ADMIN'):
                # Don't allow deleting admin accounts
                cursor.close()
                conn.close()
                return jsonify({'error': 'Cannot delete admin accounts'}), 403
            else:
                # Delete from Student table
                cursor.execute("DELETE FROM Student WHERE USN = %s", (user_id,))
                
            # Delete from user_password table
            cursor.execute("DELETE FROM user_password WHERE user_id = %s", (user_id,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return jsonify({'message': f'User {user_id} deleted successfully'}), 200
            
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'error': str(e)}), 500

    @app.route('/admin/users', methods=['POST', 'OPTIONS'])
    def add_user():
        if request.method == 'OPTIONS':
            return handle_preflight()
            
        try:
            data = request.get_json()
            print(f"Adding new user: {data}")
            
            admin_id = request.cookies.get('user_id')
            if not admin_id or not admin_id.startswith('ADMIN'):
                return jsonify({'error': 'Unauthorized access'}), 403
                
            # Validate required fields
            required_fields = ['id', 'name', 'email', 'password', 'role']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
                    
            user_id = data['id']
            name = data['name']
            email = data['email']
            password = data['password']
            role = data['role']
            department = data.get('department')
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT COUNT(*) FROM user_password WHERE user_id = %s", (user_id,))
            if cursor.fetchone()[0] > 0:
                cursor.close()
                conn.close()
                return jsonify({'error': 'User ID already exists'}), 400
                
            # Add user based on role
            if role == 'Student':
                # Get department ID
                dept_id = None
                if department:
                    cursor.execute("SELECT ID FROM Department WHERE Name = %s", (department,))
                    result = cursor.fetchone()
                    if result:
                        dept_id = result[0]
                        
                # Add to Student table
                cursor.execute("""
                    INSERT INTO Student (USN, Name, E_Mail, Join_Date, Dept_ID)
                    VALUES (%s, %s, %s, CURDATE(), %s)
                """, (user_id, name, email, dept_id))
                
            elif role == 'Faculty':
                # Add to Staff table
                cursor.execute("""
                    INSERT INTO Staff (ID, Name, E_Mail, Designation)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name, email, department))
                
            # Add to user_password table
            cursor.execute("""
                INSERT INTO user_password (user_id, password, role)
                VALUES (%s, %s, %s)
            """, (user_id, password, role))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return jsonify({'message': f'User {user_id} added successfully'}), 201
            
        except Exception as e:
            print(f"Error adding user: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'error': str(e)}), 500

    @app.route('/admin/users/<user_id>', methods=['PUT', 'OPTIONS'])
    def update_user(user_id):
        if request.method == 'OPTIONS':
            return handle_preflight()
            
        try:
            data = request.get_json()
            print(f"Updating user {user_id}: {data}")
            
            admin_id = request.cookies.get('user_id')
            if not admin_id or not admin_id.startswith('ADMIN'):
                return jsonify({'error': 'Unauthorized access'}), 403
                
            # Validate required fields
            required_fields = ['name', 'email', 'role']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
                    
            name = data['name']
            email = data['email']
            role = data['role']
            department = data.get('department')
            password = data.get('password')
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Update user based on role
            if role == 'Student':
                # Get department ID
                dept_id = None
                if department:
                    cursor.execute("SELECT ID FROM Department WHERE Name = %s", (department,))
                    result = cursor.fetchone()
                    if result:
                        dept_id = result[0]
                        
                # Update Student table
                cursor.execute("""
                    UPDATE Student 
                    SET Name = %s, E_Mail = %s, Dept_ID = %s
                    WHERE USN = %s
                """, (name, email, dept_id, user_id))
                
            elif role == 'Faculty':
                # Update Staff table
                cursor.execute("""
                    UPDATE Staff 
                    SET Name = %s, E_Mail = %s, Designation = %s
                    WHERE ID = %s
                """, (name, email, department, user_id))
                
            # Update password if provided
            if password:
                cursor.execute("""
                    UPDATE user_password 
                    SET password = %s
                    WHERE user_id = %s
                """, (password, user_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return jsonify({'message': f'User {user_id} updated successfully'}), 200
            
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'error': str(e)}), 500
            
    # API endpoint for all users (students, faculty, admin)
    @app.route('/admin/users', methods=['GET', 'OPTIONS'])
    def get_all_users():
        if request.method == 'OPTIONS':
            return handle_preflight()
            
        try:
            print("Fetching all users")
            faculty_id = request.args.get('faculty_id') or request.cookies.get('user_id')
            
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            if faculty_id and faculty_id.startswith('FAC'):
                print(f"Fetching students for faculty: {faculty_id}")
                # Get students taught by this faculty
                cursor.execute("""
                    SELECT DISTINCT s.USN as id, s.Name as name, s.E_Mail as email, 'Student' as role, d.Name as department
                    FROM Student s
                    JOIN Teaches t ON s.USN = t.USN
                    LEFT JOIN Department d ON s.Dept_ID = d.ID
                    WHERE t.ID = %s
                """, (faculty_id,))
                students = cursor.fetchall()
                return jsonify(students), 200
            else:
                # Get all students
                cursor.execute("""
                    SELECT USN as id, Name as name, E_Mail as email, 'Student' as role, 
                        (SELECT d.Name FROM Department d WHERE d.ID = s.Dept_ID) as department
                    FROM Student s
                """)
                students = cursor.fetchall()
                
                # Get all faculty
                cursor.execute("""
                    SELECT ID as id, Name as name, E_Mail as email, 'Faculty' as role, 
                        Designation as department
                    FROM Staff
                    WHERE ID LIKE 'FAC%'
                """)
                faculty = cursor.fetchall()
                
                # Get all admins
                cursor.execute("""
                    SELECT ID as id, Name as name, E_Mail as email, 'Admin' as role,
                        'Administration' as department
                    FROM Staff
                    WHERE ID LIKE 'ADMIN%'
                """)
                admins = cursor.fetchall()
                
                # Combine all users
                all_users = students + faculty + admins
                
                cursor.close()
                conn.close()
                
                return jsonify(all_users), 200
                
        except Exception as e:
            print(f"Error fetching users: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'error': str(e)}), 500
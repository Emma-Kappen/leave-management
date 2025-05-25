from flask_login import UserMixin
from datetime import datetime
from .db import execute_query

class Student(UserMixin):
    """Student model for authentication and data access."""
    
    def __init__(self, usn, name, email, dept_id, password=None, join_date=None):
        self.USN = usn
        self.Name = name
        self.E_Mail = email
        self.Dept_ID = dept_id
        self.Password = password
        self.Join_Date = join_date
    
    @staticmethod
    def get_by_id(usn):
        """Get student by USN."""
        query = "SELECT * FROM Student WHERE USN = %s"
        result = execute_query(query, (usn,))
        if result:
            student_data = result[0]
            return Student(
                usn=student_data['USN'],
                name=student_data['Name'],
                email=student_data['E_Mail'],
                dept_id=student_data['Dept_ID'],
                password=student_data['Password'],
                join_date=student_data['Join_Date']
            )
        return None
    
    def verify_password(self, password):
        """Verify the password."""
        # For simplicity, direct comparison (in production, use hashed passwords)
        return self.Password == password
    
    def get_id(self):
        """Return the user ID for Flask-Login."""
        return self.USN
    
    @property
    def role(self):
        """Return the user role."""
        return 'student'
    
    @property
    def id(self):
        """Return the user ID."""
        return self.USN
    
    def get_department_name(self):
        """Get the department name."""
        query = "SELECT Name FROM Department WHERE ID = %s"
        result = execute_query(query, (self.Dept_ID,))
        if result:
            return result[0]['Name']
        return None
    
    def get_leaves(self):
        """Get all leaves for this student."""
        query = """
            SELECT Leave_ID, Leave_Type, Reason, Start_Date, End_Date, 
                   Submission_Date, Approval_Status 
            FROM `Leave` 
            WHERE Applicant_ID = %s
        """
        result = execute_query(query, (self.USN,))
        return [Leave.from_db_row(row) for row in result]
    
    def get_attendance(self):
        """Get attendance records for this student."""
        query = """
            SELECT a.USN, a.Subject_Code, s.Title as Subject_Name, 
                   a.Classes_Taken, a.Classes_Attended
            FROM Attendance a
            JOIN Subject s ON a.Subject_Code = s.Code
            WHERE a.USN = %s
        """
        result = execute_query(query, (self.USN,))
        return [Attendance.from_db_row(row) for row in result]
    
    def get_subjects(self):
        """Get subjects for this student."""
        query = """
        SELECT DISTINCT s.Code, s.Title 
        FROM Subject s
        LEFT JOIN Attendance a ON s.Code = a.Subject_Code
        LEFT JOIN Teaches t ON s.Code = t.Subject_Code
        WHERE a.USN = %s OR t.USN = %s
        ORDER BY s.Title
        """
        result = execute_query(query, (self.USN, self.USN))
        return result
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'usn': self.USN,
            'name': self.Name,
            'email': self.E_Mail,
            'dept_id': self.Dept_ID,
            'dept_name': self.get_department_name()
        }

class Staff(UserMixin):
    """Staff model for authentication and data access."""
    
    def __init__(self, id, name, email, designation, password=None, supervisor_id=None):
        self.ID = id
        self.Name = name
        self.E_Mail = email
        self.Designation = designation
        self.Password = password
        self.Supervisor_ID = supervisor_id
    
    @staticmethod
    def get_by_id(id):
        """Get staff by ID."""
        query = "SELECT * FROM Staff WHERE ID = %s"
        result = execute_query(query, (id,))
        if result:
            staff_data = result[0]
            return Staff(
                id=staff_data['ID'],
                name=staff_data['Name'],
                email=staff_data['E_Mail'],
                designation=staff_data['Designation'],
                password=staff_data['Password'],
                supervisor_id=staff_data['Supervisor_ID']
            )
        return None
    
    def verify_password(self, password):
        """Verify the password."""
        # For simplicity, direct comparison (in production, use hashed passwords)
        return self.Password == password
    
    def get_id(self):
        """Return the user ID for Flask-Login."""
        return self.ID
    
    @property
    def role(self):
        """Return the user role."""
        if self.Designation == 'Administrator':
            return 'admin'
        return 'faculty'
    
    @property
    def id(self):
        """Return the user ID."""
        return self.ID

class Leave:
    """Leave model for data access."""
    
    def __init__(self, leave_id, applicant_id, leave_type, reason, start_date, end_date, 
                 submission_date=None, approval_status='PENDING'):
        self.Leave_ID = leave_id
        self.Applicant_ID = applicant_id
        self.Leave_Type = leave_type
        self.Reason = reason
        self.Start_Date = start_date
        self.End_Date = end_date
        self.Submission_Date = submission_date or datetime.now()
        self.Approval_Status = approval_status
    
    @staticmethod
    def from_db_row(row):
        """Create a Leave object from a database row."""
        return Leave(
            leave_id=row['Leave_ID'],
            applicant_id=row['Applicant_ID'] if 'Applicant_ID' in row else None,
            leave_type=row['Leave_Type'],
            reason=row['Reason'],
            start_date=row['Start_Date'],
            end_date=row['End_Date'],
            submission_date=row['Submission_Date'],
            approval_status=row['Approval_Status']
        )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'Leave_ID': self.Leave_ID,
            'Type': self.Leave_Type,
            'Reason': self.Reason,
            'Start_Date': self.Start_Date.strftime('%Y-%m-%d') if isinstance(self.Start_Date, datetime) else self.Start_Date,
            'End_Date': self.End_Date.strftime('%Y-%m-%d') if isinstance(self.End_Date, datetime) else self.End_Date,
            'Status': self.Approval_Status,
            'Submission_Date': self.Submission_Date.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self.Submission_Date, datetime) else self.Submission_Date
        }

class Attendance:
    """Attendance model for data access."""
    
    def __init__(self, usn, subject_code, classes_taken, classes_attended, subject_name=None):
        self.USN = usn
        self.Subject_Code = subject_code
        self.Classes_Taken = classes_taken
        self.Classes_Attended = classes_attended
        self.Subject_Name = subject_name
    
    @staticmethod
    def from_db_row(row):
        """Create an Attendance object from a database row."""
        return Attendance(
            usn=row['USN'],
            subject_code=row['Subject_Code'],
            classes_taken=row['Classes_Taken'],
            classes_attended=row['Classes_Attended'],
            subject_name=row['Subject_Name'] if 'Subject_Name' in row else None
        )
    
    def to_dict(self):
        """Convert to dictionary."""
        attendance_percentage = round((self.Classes_Attended / self.Classes_Taken) * 100, 2) if self.Classes_Taken > 0 else 0
        return {
            'subject_code': self.Subject_Code,
            'subject_name': self.Subject_Name or '',
            'classes_taken': self.Classes_Taken,
            'classes_attended': self.Classes_Attended,
            'attendance_percentage': attendance_percentage
        }
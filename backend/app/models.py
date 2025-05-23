from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = 'Department'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)

class Staff(UserMixin, db.Model):
    __tablename__ = 'Staff'
    ID = db.Column(db.String(12), primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    E_Mail = db.Column(db.String(100), unique=True, nullable=False)
    Designation = db.Column(db.String(50))
    Supervisor_ID = db.Column(db.String(12), db.ForeignKey('Staff.ID'))
    password = db.Column(db.String(128))  # hashed password

    @property
    def role(self):
        return 'Faculty'

    def get_id(self):
        return self.ID

class Student(UserMixin, db.Model):
    __tablename__ = 'Student'
    USN = db.Column(db.String(12), primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    E_Mail = db.Column(db.String(100), unique=True, nullable=False)
    Join_Date = db.Column(db.Date)
    Dept_ID = db.Column(db.Integer, db.ForeignKey('Department.ID'))
    password = db.Column(db.String(128))  # hashed password

    @property
    def role(self):
        return 'Student'

    def get_id(self):
        return self.USN

class Subject(db.Model):
    __tablename__ = 'Subject'
    Code = db.Column(db.String(20), primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    Dept_ID = db.Column(db.Integer, db.ForeignKey('Department.ID'))
    Semester = db.Column(db.Integer)

class Attendance(db.Model):
    __tablename__ = 'Attendance'
    USN = db.Column(db.String(12), db.ForeignKey('Student.USN'), primary_key=True)
    Subject_Code = db.Column(db.String(20), db.ForeignKey('Subject.Code'), primary_key=True)
    Classes_Taken = db.Column(db.Integer, default=0)
    Classes_Attended = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "USN": self.USN,
            "Subject_Code": self.Subject_Code,
            "Classes_Taken": self.Classes_Taken,
            "Classes_Attended": self.Classes_Attended
        }

class Leave(db.Model):
    __tablename__ = 'Leave'
    Leave_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Applicant_ID = db.Column(db.String(12), db.ForeignKey('Student.USN'))
    Leave_Type = db.Column(db.Enum('SICK', 'CASUAL', 'OTHER'))
    Reason = db.Column(db.Text)
    Start_Date = db.Column(db.Date)
    End_Date = db.Column(db.Date)
    Submission_Date = db.Column(db.DateTime)
    Approval_Status = db.Column(db.Enum('PENDING', 'APPROVED', 'REJECTED'), default='PENDING')

    def to_dict(self):
        return {
            "Leave_ID": self.Leave_ID,
            "Type": self.Leave_Type,
            "Reason": self.Reason,
            "Start_Date": self.Start_Date.strftime('%Y-%m-%d'),
            "End_Date": self.End_Date.strftime('%Y-%m-%d'),
            "Status": self.Approval_Status
        }

class LeaveApprover(db.Model):
    __tablename__ = 'Leave_Approver'
    Leave_ID = db.Column(db.Integer, db.ForeignKey('Leave.Leave_ID'), primary_key=True)
    Approver_ID = db.Column(db.String(12), db.ForeignKey('Staff.ID'), primary_key=True)
    Decision_Date = db.Column(db.DateTime)

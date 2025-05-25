-- Departments
INSERT INTO Department (Dept_ID, Dept_Name) VALUES
(1, 'Computer Science'),
(2, 'Electronics'),
(3, 'Mechanical');

-- Staff (Faculty)
INSERT INTO Staff (Staff_ID, Name, E_Mail, Password, Dept_ID) VALUES
(1, 'Dr. Anil Kumar', 'anil.kumar@college.edu', 'pass123', 1),
(2, 'Dr. Meena Reddy', 'meena.reddy@college.edu', 'pass123', 1),
(3, 'Mr. Rajiv Sharma', 'rajiv.sharma@college.edu', 'pass123', 2),
(4, 'Ms. Kavita Iyer', 'kavita.iyer@college.edu', 'pass123', 2),
(5, 'Mr. Arjun Nair', 'arjun.nair@college.edu', 'pass123', 3);

-- Admin
INSERT INTO Admin (Admin_ID, Name, E_Mail, Password) VALUES
(1, 'Principal Raghavan', 'principal@college.edu', 'adminpass');

-- Subjects
INSERT INTO Subject (Subject_Code, Subject_Name, Dept_ID) VALUES
('CS101', 'Data Structures', 1),
('CS102', 'Database Systems', 1),
('EC101', 'Digital Electronics', 2),
('ME101', 'Thermodynamics', 3),
('CS103', 'Operating Systems', 1);

-- Students
INSERT INTO Student (USN, Name, E_Mail, Password, Dept_ID) VALUES
('1RV21CS001', 'Aarav Patel', 'aarav.patel@college.edu', 'stud123', 1),
('1RV21CS002', 'Isha Rani', 'isha.rani@college.edu', 'stud123', 1),
('1RV21CS003', 'Rohan Mehta', 'rohan.mehta@college.edu', 'stud123', 1),
('1RV21CS004', 'Sneha Singh', 'sneha.singh@college.edu', 'stud123', 1),
('1RV21CS005', 'Vikram Joshi', 'vikram.joshi@college.edu', 'stud123', 1),
('1RV21CS006', 'Neha Verma', 'neha.verma@college.edu', 'stud123', 1),
('1RV21CS007', 'Kabir Das', 'kabir.das@college.edu', 'stud123', 1),
('1RV21CS008', 'Tanya Roy', 'tanya.roy@college.edu', 'stud123', 1),
('1RV21CS009', 'Aditya Rao', 'aditya.rao@college.edu', 'stud123', 1),
('1RV21CS010', 'Pooja Shetty', 'pooja.shetty@college.edu', 'stud123', 1),
('1RV21EC011', 'Sahil Jain', 'sahil.jain@college.edu', 'stud123', 2),
('1RV21EC012', 'Ritika Paul', 'ritika.paul@college.edu', 'stud123', 2),
('1RV21EC013', 'Anjali Das', 'anjali.das@college.edu', 'stud123', 2),
('1RV21EC014', 'Manav Kapoor', 'manav.kapoor@college.edu', 'stud123', 2),
('1RV21EC015', 'Divya Bhatt', 'divya.bhatt@college.edu', 'stud123', 2),
('1RV21ME016', 'Ramesh Gowda', 'ramesh.gowda@college.edu', 'stud123', 3),
('1RV21ME017', 'Sowmya Hegde', 'sowmya.hegde@college.edu', 'stud123', 3),
('1RV21ME018', 'Nikhil Menon', 'nikhil.menon@college.edu', 'stud123', 3),
('1RV21ME019', 'Lavanya Rao', 'lavanya.rao@college.edu', 'stud123', 3),
('1RV21ME020', 'Harish Nayak', 'harish.nayak@college.edu', 'stud123', 3);

-- Teaches (Faculty assigned to Subjects)
INSERT INTO Teaches (Staff_ID, Subject_Code) VALUES
(1, 'CS101'), (1, 'CS102'),
(2, 'CS102'), (2, 'CS103'),
(3, 'EC101'),
(4, 'ME101'),
(5, 'CS103');

-- Attendance records
INSERT INTO Attendance (Attendance_ID, USN, Subject_Code, Date, Status) VALUES
(1, '1RV21CS001', 'CS101', '2024-01-15', 'Present'),
(2, '1RV21CS001', 'CS102', '2024-01-15', 'Present'),
(3, '1RV21CS002', 'CS101', '2024-01-15', 'Present'),
(4, '1RV21CS002', 'CS102', '2024-01-15', 'Absent'),
(5, '1RV21CS003', 'CS101', '2024-01-15', 'Present'),
(6, '1RV21CS003', 'CS102', '2024-01-15', 'Present');

-- Leave Requests
INSERT INTO Leave_Request (Leave_ID, USN, Subject_Code, Leave_Type, Start_Date, End_Date, Status, Submission_Date) VALUES
(1, '1RV21CS001', 'CS101', 'Sick', '2024-02-10', '2024-02-12', 'Approved', '2024-02-09 08:30:00'),
(2, '1RV21CS002', 'CS102', 'Personal', '2024-02-15', '2024-02-16', 'Pending', '2024-02-12 10:00:00'),
(3, '1RV21EC011', 'EC101', 'Event', '2024-02-20', '2024-02-21', 'Approved', '2024-02-18 09:15:00');

-- Leave Approver Entries
INSERT INTO Leave_Approver (Approver_ID, Staff_ID, Leave_ID, Approval_Status, Approval_Date) VALUES
(1, 1, 1, 'Approved', '2024-02-09 15:00:00'),
(2, 2, 2, 'Pending', NULL),
(3, 3, 3, 'Approved', '2024-02-19 14:00:00');
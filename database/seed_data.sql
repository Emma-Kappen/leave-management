USE college_leave_mgmt;

-- Departments
INSERT INTO Department (Name) VALUES 
('Computer Science'), ('Electronics'), ('Mechanical');

-- Staff
INSERT INTO Staff (ID, Name, E_Mail, Designation, Supervisor_ID) VALUES
('FAC001', 'Dr. Anjali Rao', 'anjali.rao@example.edu', 'Professor', NULL),
('FAC002', 'Prof. Kiran Mehta', 'kiran.mehta@example.edu', 'Assistant Professor', 'FAC001'),
('FAC003', 'Dr. Neha Sharma', 'neha.sharma@example.edu', 'Associate Professor', 'FAC001'),
('FAC004', 'Prof. Arjun Dev', 'arjun.dev@example.edu', 'Assistant Professor', 'FAC003'),
('FAC005', 'Dr. Meera Iyer', 'meera.iyer@example.edu', 'Professor', NULL);

-- Students
INSERT INTO Student (USN, Name, E_Mail, Join_Date, Dept_ID) VALUES
('1CS21CS001', 'Aditi Kumar', 'aditi.k@example.edu', '2021-08-01', 1),
('1CS21CS002', 'Rahul Verma', 'rahul.v@example.edu', '2021-08-01', 1),
('1CS21CS003', 'Sneha Patil', 'sneha.p@example.edu', '2021-08-01', 1),
('1CS21CS004', 'Nikhil Rao', 'nikhil.r@example.edu', '2021-08-01', 1),
('1CS21CS005', 'Divya Shah', 'divya.s@example.edu', '2021-08-01', 1),
('1EC21EC006', 'Aman Gupta', 'aman.g@example.edu', '2021-08-01', 2),
('1EC21EC007', 'Pooja Joshi', 'pooja.j@example.edu', '2021-08-01', 2),
('1EC21EC008', 'Sagar Naik', 'sagar.n@example.edu', '2021-08-01', 2),
('1EC21EC009', 'Kriti Singh', 'kriti.s@example.edu', '2021-08-01', 2),
('1EC21EC010', 'Tanishq Reddy', 'tanishq.r@example.edu', '2021-08-01', 2),
('1ME21ME011', 'Neeraj Bhat', 'neeraj.b@example.edu', '2021-08-01', 3),
('1ME21ME012', 'Harshita Jain', 'harshita.j@example.edu', '2021-08-01', 3),
('1ME21ME013', 'Ravi Deshmukh', 'ravi.d@example.edu', '2021-08-01', 3),
('1ME21ME014', 'Priya Kale', 'priya.k@example.edu', '2021-08-01', 3),
('1ME21ME015', 'Anuj Nair', 'anuj.n@example.edu', '2021-08-01', 3),
('1CS21CS016', 'Shruti Rao', 'shruti.r@example.edu', '2021-08-01', 1),
('1CS21CS017', 'Varun Sinha', 'varun.s@example.edu', '2021-08-01', 1),
('1EC21EC018', 'Isha Kapoor', 'isha.k@example.edu', '2021-08-01', 2),
('1ME21ME019', 'Aditya Joshi', 'aditya.j@example.edu', '2021-08-01', 3),
('1CS21CS020', 'Rhea Mehta', 'rhea.m@example.edu', '2021-08-01', 1);

-- Subjects
INSERT INTO Subject (Code, Title, Dept_ID, Semester) VALUES
('CS101', 'Data Structures', 1, 3),
('CS102', 'Operating Systems', 1, 4),
('EC201', 'Analog Electronics', 2, 3),
('ME301', 'Thermodynamics', 3, 3);

-- Teaches (Faculty assigned to students for subjects)
INSERT INTO Teaches (ID, USN, Subject_Code) VALUES
('FAC001', '1CS21CS001', 'CS101'),
('FAC001', '1CS21CS002', 'CS101'),
('FAC001', '1CS21CS003', 'CS101'),
('FAC002', '1CS21CS004', 'CS102'),
('FAC002', '1CS21CS005', 'CS102'),
('FAC003', '1EC21EC006', 'EC201'),
('FAC003', '1EC21EC007', 'EC201'),
('FAC003', '1EC21EC008', 'EC201'),
('FAC004', '1ME21ME011', 'ME301'),
('FAC004', '1ME21ME012', 'ME301');

-- Attendance
INSERT INTO Attendance (USN, Subject_Code, Classes_Taken, Classes_Attended) VALUES
('1CS21CS001', 'CS101', 40, 35),
('1CS21CS002', 'CS101', 40, 38),
('1CS21CS003', 'CS101', 40, 30),
('1CS21CS004', 'CS102', 42, 41),
('1CS21CS005', 'CS102', 42, 40),
('1EC21EC006', 'EC201', 39, 37),
('1EC21EC007', 'EC201', 39, 35),
('1ME21ME011', 'ME301', 41, 39),
('1ME21ME012', 'ME301', 41, 38);

-- Leave Applications
INSERT INTO Leave (`Applicant_ID`, `Leave_Type`, `Reason`, `Start_Date`, `End_Date`, `Approval_Status`) VALUES
('1CS21CS001', 'SICK', 'Fever and cold', CURDATE() + INTERVAL

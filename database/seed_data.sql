-- Department
INSERT INTO Department (ID, Name) VALUES
(1, 'Computer Science'),
(2, 'Electronics'),
(3, 'Mechanical'),
(4, 'Civil'),
(5, 'Electrical');

-- Staff
INSERT INTO Staff (ID, Name, E_Mail, Designation, Supervisor_ID, Password) VALUES
('S001', 'Dr. Alice Rao', 'alice.rao@example.com', 'Professor', NULL, 'alice123'),
('S002', 'Mr. Bob Smith', 'bob.smith@example.com', 'Assistant Professor', 'S001', 'bob123'),
('S003', 'Ms. Clara John', 'clara.john@example.com', 'Lecturer', 'S001', 'clara123'),
('S004', 'Dr. David White', 'david.white@example.com', 'Professor', NULL, 'david123'),
('S005', 'Ms. Eva Green', 'eva.green@example.com', 'Lecturer', 'S004', 'eva123');

-- Student
INSERT INTO Student (USN, Name, E_Mail, Join_Date, Dept_ID, Password) VALUES
('CS001', 'John Doe', 'john.doe@example.com', '2022-08-01', 1, 'john123'),
('CS002', 'Jane Smith', 'jane.smith@example.com', '2022-08-01', 1, 'jane123'),
('CS003', 'Tom Brown', 'tom.brown@example.com', '2022-08-01', 1, 'tom123'),
('EC001', 'Sara Khan', 'sara.khan@example.com', '2022-08-01', 2, 'sara123'),
('EC002', 'Ali Patel', 'ali.patel@example.com', '2022-08-01', 2, 'ali123'),
('ME001', 'Mike Lee', 'mike.lee@example.com', '2022-08-01', 3, 'mike123'),
('ME002', 'Nina Roy', 'nina.roy@example.com', '2022-08-01', 3, 'nina123'),
('CV001', 'George Mathew', 'george.mathew@example.com', '2022-08-01', 4, 'george123'),
('CV002', 'Rita Paul', 'rita.paul@example.com', '2022-08-01', 4, 'rita123'),
('EE001', 'Sam Wilson', 'sam.wilson@example.com', '2022-08-01', 5, 'sam123');

-- Admin
INSERT INTO Admin (ID, Name, E_Mail, Password) VALUES
(1, 'System Admin', 'admin@example.com', 'admin123');

-- Subject
INSERT INTO Subject (Code, Title, Dept_ID, Semester) VALUES
('CS101', 'Data Structures', 1, 3),
('CS102', 'Algorithms', 1, 4),
('EC101', 'Digital Circuits', 2, 3),
('ME101', 'Thermodynamics', 3, 3),
('CV101', 'Structural Analysis', 4, 4),
('EE101', 'Power Systems', 5, 4);

-- Attendance
INSERT INTO Attendance (USN, Subject_Code, Classes_Taken, Classes_Attended) VALUES
('CS001', 'CS101', 40, 35),
('CS002', 'CS101', 40, 38),
('CS003', 'CS101', 40, 37),
('EC001', 'EC101', 40, 34),
('EC002', 'EC101', 40, 36),
('ME001', 'ME101', 40, 39),
('ME002', 'ME101', 40, 30),
('CV001', 'CV101', 40, 32),
('CV002', 'CV101', 40, 34),
('EE001', 'EE101', 40, 31);

-- Teaches
INSERT INTO Teaches (ID, USN, Subject_Code) VALUES
('S001', 'CS001', 'CS101'),
('S001', 'CS002', 'CS101'),
('S001', 'CS003', 'CS101'),
('S002', 'EC001', 'EC101'),
('S002', 'EC002', 'EC101'),
('S003', 'ME001', 'ME101'),
('S003', 'ME002', 'ME101'),
('S004', 'CV001', 'CV101'),
('S004', 'CV002', 'CV101'),
('S005', 'EE001', 'EE101');

-- Leave
INSERT INTO `Leave` (Leave_ID, Applicant_ID, Leave_Type, Reason, Start_Date, End_Date, Submission_Date, Approval_Status) VALUES
(1, 'CS001', 'SICK', 'Fever and cold', '2025-05-20', '2025-05-22', '2025-05-19 10:30:00', 'PENDING'),
(2, 'EC002', 'CASUAL', 'Family function', '2025-05-23', '2025-05-24', '2025-05-20 14:00:00', 'APPROVED'),
(3, 'ME002', 'OTHER', 'Project work', '2025-05-25', '2025-05-26', '2025-05-21 09:00:00', 'REJECTED');

-- Leave Approver
INSERT INTO Leave_Approver (Leave_ID, Approver_ID, Decision_Date) VALUES
(2, 'S002', '2025-05-21 16:00:00'),
(3, 'S003', '2025-05-22 12:30:00');

-- Create database
CREATE DATABASE IF NOT EXISTS college_leave_mgmt;
USE college_leave_mgmt;

-- Table: Department
CREATE TABLE Department (
    Dept_ID INT AUTO_INCREMENT PRIMARY KEY,
    Dept_Name VARCHAR(100) NOT NULL UNIQUE
);

-- Table: Staff (Faculty)
CREATE TABLE Staff (
    Staff_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    E_Mail VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Dept_ID INT,
    FOREIGN KEY (Dept_ID) REFERENCES Department(Dept_ID) ON DELETE SET NULL
);

-- Table: Student
CREATE TABLE Student (
    USN VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    E_Mail VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Dept_ID INT,
    FOREIGN KEY (Dept_ID) REFERENCES Department(Dept_ID) ON DELETE SET NULL
);

-- Table: Admin
CREATE TABLE Admin (
    Admin_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    E_Mail VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL
);

-- Table: Subject
CREATE TABLE Subject (
    Subject_Code VARCHAR(20) PRIMARY KEY,
    Subject_Name VARCHAR(100) NOT NULL,
    Dept_ID INT,
    FOREIGN KEY (Dept_ID) REFERENCES Department(Dept_ID) ON DELETE SET NULL
);

-- Table: Teaches (Faculty assigned to Subjects)
CREATE TABLE Teaches (
    Staff_ID INT,
    Subject_Code VARCHAR(20),
    PRIMARY KEY (Staff_ID, Subject_Code),
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID) ON DELETE CASCADE,
    FOREIGN KEY (Subject_Code) REFERENCES Subject(Subject_Code) ON DELETE CASCADE
);

-- Table: Leave (Leave requests)
CREATE TABLE Leave_Request (
    Leave_ID INT AUTO_INCREMENT PRIMARY KEY,
    USN VARCHAR(20),
    Subject_Code VARCHAR(20),
    Leave_Type VARCHAR(50),
    Start_Date DATE,
    End_Date DATE,
    Status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    Submission_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    Document_Path VARCHAR(255),  -- For uploaded documents
    FOREIGN KEY (USN) REFERENCES Student(USN) ON DELETE CASCADE,
    FOREIGN KEY (Subject_Code) REFERENCES Subject(Subject_Code) ON DELETE SET NULL
);

-- Table: Leave_Approver (who approves leaves, typically faculty)
CREATE TABLE Leave_Approver (
    Approver_ID INT AUTO_INCREMENT PRIMARY KEY,
    Staff_ID INT,
    Leave_ID INT,
    Approval_Status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    Approval_Date DATETIME,
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID) ON DELETE CASCADE,
    FOREIGN KEY (Leave_ID) REFERENCES Leave_Request(Leave_ID) ON DELETE CASCADE
);

-- (Optional) Table: Attendance (student attendance records)
CREATE TABLE Attendance (
    Attendance_ID INT AUTO_INCREMENT PRIMARY KEY,
    USN VARCHAR(20),
    Subject_Code VARCHAR(20),
    Date DATE,
    Status ENUM('Present', 'Absent') NOT NULL,
    FOREIGN KEY (USN) REFERENCES Student(USN) ON DELETE CASCADE,
    FOREIGN KEY (Subject_Code) REFERENCES Subject(Subject_Code) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_leave_status ON Leave_Request(Status);
CREATE INDEX idx_leave_submission ON Leave_Request(Submission_Date);



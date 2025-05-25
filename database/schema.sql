-- Drop existing tables
DROP TABLE IF EXISTS Leave_Approver;
DROP TABLE IF EXISTS `Leave`;
DROP TABLE IF EXISTS Teaches;
DROP TABLE IF EXISTS Attendance;
DROP TABLE IF EXISTS Subject;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Staff;
DROP TABLE IF EXISTS Department;

-- Department Table
CREATE TABLE Department (
    ID VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(50) NOT NULL
);

-- Staff Table
CREATE TABLE Staff (
    ID VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(100),
    E_Mail VARCHAR(100) UNIQUE,
    Designation VARCHAR(50),
    Supervisor_ID VARCHAR(10),
    Password VARCHAR(50),
    FOREIGN KEY (Supervisor_ID) REFERENCES Staff(ID) ON DELETE SET NULL
);

-- Student Table
CREATE TABLE Student (
    USN VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(100),
    E_Mail VARCHAR(100) UNIQUE,
    Join_Date DATE,
    Dept_ID VARCHAR(10),
    Password VARCHAR(50),
    FOREIGN KEY (Dept_ID) REFERENCES Department(ID)
);

-- Subject Table
CREATE TABLE Subject (
    Code VARCHAR(10) PRIMARY KEY,
    Title VARCHAR(100),
    Credits INT
);

-- Attendance Table
CREATE TABLE Attendance (
    USN VARCHAR(10),
    Subject_Code VARCHAR(10),
    Classes_Taken INT,
    Classes_Attended INT,
    PRIMARY KEY (USN, Subject_Code),
    FOREIGN KEY (USN) REFERENCES Student(USN) ON DELETE CASCADE,
    FOREIGN KEY (Subject_Code) REFERENCES Subject(Code)
);

-- Teaches Table
CREATE TABLE Teaches (
    ID VARCHAR(10),
    USN VARCHAR(10),
    Subject_Code VARCHAR(10),
    PRIMARY KEY (ID, USN, Subject_Code),
    FOREIGN KEY (ID) REFERENCES Staff(ID),
    FOREIGN KEY (USN) REFERENCES Student(USN),
    FOREIGN KEY (Subject_Code) REFERENCES Subject(Code)
);

-- Leave Table
CREATE TABLE `Leave` (
    Leave_ID INT PRIMARY KEY,
    Applicant_ID VARCHAR(10),
    Leave_Type VARCHAR(20),
    Reason TEXT,
    Start_Date DATE,
    End_Date DATE,
    Submission_Date DATETIME,
    Approval_Status VARCHAR(10) DEFAULT 'PENDING',
    FOREIGN KEY (Applicant_ID) REFERENCES Student(USN) ON DELETE CASCADE
);

-- Leave Approver Table
CREATE TABLE Leave_Approver (
    Leave_ID INT,
    Approver_ID VARCHAR(10),
    Decision_Date DATETIME,
    PRIMARY KEY (Leave_ID, Approver_ID),
    FOREIGN KEY (Leave_ID) REFERENCES `Leave`(Leave_ID) ON DELETE CASCADE,
    FOREIGN KEY (Approver_ID) REFERENCES Staff(ID)
);
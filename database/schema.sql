CREATE DATABASE IF NOT EXISTS `college_leave_mgmt`
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;
USE `college_leave_mgmt`;

-- ─── DEPARTMENT ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `Department` (
  `ID`       INT            NOT NULL AUTO_INCREMENT,
  `Name`     VARCHAR(100)   NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB;

-- ─── STAFF ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `Staff` (
  `ID`            VARCHAR(12)   NOT NULL,
  `Name`          VARCHAR(100)  NOT NULL,
  `E_Mail`        VARCHAR(100)  NOT NULL UNIQUE,
  `Designation`   VARCHAR(50),
  `Supervisor_ID` VARCHAR(12),
  `Password`      VARCHAR(255),
  PRIMARY KEY (`ID`),
  INDEX (`Supervisor_ID`),
  FOREIGN KEY (`Supervisor_ID`)
    REFERENCES `Staff` (`ID`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ─── STUDENT ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `Student` (
  `USN`        VARCHAR(12)    NOT NULL,
  `Name`       VARCHAR(100)   NOT NULL,
  `E_Mail`     VARCHAR(100)   NOT NULL UNIQUE,
  `Join_Date`  DATE,
  `Dept_ID`    INT,
  `Password`   VARCHAR(255),
  PRIMARY KEY (`USN`),
  FOREIGN KEY (`Dept_ID`)
    REFERENCES `Department` (`ID`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ─── ADMIN ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `Admin` (
  `ID`        INT           NOT NULL AUTO_INCREMENT,
  `Name`      VARCHAR(100)  NOT NULL,
  `E_Mail`    VARCHAR(100)  NOT NULL UNIQUE,
  `Password`  VARCHAR(255)  NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB;

-- ─── SUBJECT ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `Subject` (
  `Code`     VARCHAR(20)   NOT NULL,
  `Title`    VARCHAR(100)  NOT NULL,
  `Dept_ID`  INT,
  `Semester` INT,
  PRIMARY KEY (`Code`),
  FOREIGN KEY (`Dept_ID`)
    REFERENCES `Department` (`ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ─── ATTENDANCE ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `Attendance` (
  `USN`              VARCHAR(12)  NOT NULL,
  `Subject_Code`     VARCHAR(20)  NOT NULL,
  `Classes_Taken`    INT          NOT NULL DEFAULT 0,
  `Classes_Attended` INT          NOT NULL DEFAULT 0,
  PRIMARY KEY (`USN`, `Subject_Code`),
  FOREIGN KEY (`USN`)
    REFERENCES `Student` (`USN`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (`Subject_Code`)
    REFERENCES `Subject` (`Code`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ─── TEACHES ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `Teaches` (
  `ID`           VARCHAR(12)   NOT NULL,
  `USN`          VARCHAR(12)   NOT NULL,
  `Subject_Code` VARCHAR(20)   NOT NULL,
  PRIMARY KEY (`ID`, `USN`, `Subject_Code`),
  FOREIGN KEY (`ID`)
    REFERENCES `Staff` (`ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (`USN`)
    REFERENCES `Student` (`USN`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (`Subject_Code`)
    REFERENCES `Subject` (`Code`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ─── LEAVE ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `Leave` (
  `Leave_ID`        INT               NOT NULL AUTO_INCREMENT,
  `Applicant_ID`    VARCHAR(12)       NOT NULL,
  `Leave_Type`      ENUM('SICK','CASUAL','OTHER')   NOT NULL,
  `Reason`          TEXT              NOT NULL,
  `Start_Date`      DATE              NOT NULL,
  `End_Date`        DATE              NOT NULL,
  `Submission_Date` DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Approval_Status` ENUM('PENDING','APPROVED','REJECTED') NOT NULL DEFAULT 'PENDING',
  PRIMARY KEY (`Leave_ID`),
  INDEX (`Applicant_ID`),
  FOREIGN KEY (`Applicant_ID`)
    REFERENCES `Student` (`USN`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ─── LEAVE_APPROVER ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `Leave_Approver` (
  `Leave_ID`      INT           NOT NULL,
  `Approver_ID`   VARCHAR(12)   NOT NULL,
  `Decision_Date` DATETIME,
  PRIMARY KEY (`Leave_ID`, `Approver_ID`),
  FOREIGN KEY (`Leave_ID`)
    REFERENCES `Leave` (`Leave_ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (`Approver_ID`)
    REFERENCES `Staff` (`ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ─── USER_PASSWORD TABLE
CREATE TABLE IF NOT EXISTS `user_password` (
  `user_id` VARCHAR(12) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `role` ENUM('Student', 'Faculty', 'Admin') NOT NULL,
  PRIMARY KEY (`user_id`),
  FOREIGN KEY (`user_id`) REFERENCES `Student` (`USN`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`user_id`) REFERENCES `Staff` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ─── TRIGGERS FOR NEXT‑DAY RULE ────────────────────────────────────────
DELIMITER $
CREATE TRIGGER trg_leave_bi
BEFORE INSERT ON `Leave`
FOR EACH ROW
BEGIN
  IF NEW.Start_Date < CURRENT_DATE + INTERVAL 1 DAY THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Start_Date must be at least tomorrow';
  END IF;
END$

CREATE TRIGGER trg_leave_bu
BEFORE UPDATE ON `Leave`
FOR EACH ROW
BEGIN
  IF NEW.Start_Date < CURRENT_DATE + INTERVAL 1 DAY THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Start_Date must be at least tomorrow';
  END IF;
END$$
DELIMITER ;

-- ─── VIEWS ─────────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW `Student_Subjects_View` AS
SELECT
  s.USN,
  s.Name          AS Student_Name,
  subj.Code       AS Subject_Code,
  subj.Title      AS Subject_Title,
  subj.Semester,
  d.Name          AS Department
FROM `Student` s
JOIN `Teaches` t        ON s.USN            = t.USN
JOIN `Subject` subj     ON t.Subject_Code    = subj.Code
JOIN `Department` d     ON subj.Dept_ID      = d.ID;

CREATE OR REPLACE VIEW `Staff_Teach_View` AS
SELECT
  st.ID            AS Staff_ID,
  st.Name          AS Staff_Name,
  subj.Code        AS Subject_Code,
  subj.Title       AS Subject_Title,
  COUNT(DISTINCT t.USN) AS Student_Count
FROM `Staff` st
JOIN `Teaches` t       ON st.ID             = t.ID
JOIN `Subject` subj    ON t.Subject_Code    = subj.Code
GROUP BY st.ID, subj.Code, subj.Title;

CREATE OR REPLACE VIEW `Attendance_Summary_View` AS
SELECT
  a.USN,
  s.Name           AS Student_Name,
  a.Subject_Code,
  subj.Title       AS Subject_Title,
  a.Classes_Taken,
  a.Classes_Attended,
  CASE
    WHEN a.Classes_Taken = 0 THEN 0
    ELSE ROUND((a.Classes_Attended / a.Classes_Taken) * 100, 2)
  END AS Attendance_Percentage
FROM `Attendance` a
JOIN `Student` s      ON a.USN            = s.USN
JOIN `Subject` subj   ON a.Subject_Code    = subj.Code;

CREATE OR REPLACE VIEW `Pending_Leaves_View` AS
SELECT
  l.Leave_ID,
  s.Name            AS Student_Name,
  l.Leave_Type,
  l.Reason,
  l.Start_Date,
  l.End_Date,
  l.Submission_Date,
  l.Approval_Status
FROM `Leave` l
JOIN `Student` s    ON l.Applicant_ID     = s.USN
WHERE l.Approval_Status = 'PENDING';

CREATE OR REPLACE VIEW `Leave_Approval_Status_View` AS
SELECT
  l.Leave_ID,
  s.Name                                              AS Student_Name,
  GROUP_CONCAT(sa.Name ORDER BY sa.Name SEPARATOR ', ') AS Approvers,
  l.Approval_Status
FROM `Leave` l
JOIN `Student` s           ON l.Applicant_ID     = s.USN
JOIN `Leave_Approver` la   ON l.Leave_ID         = la.Leave_ID
JOIN `Staff` sa            ON la.Approver_ID     = sa.ID
GROUP BY l.Leave_ID, s.Name, l.Approval_Status;

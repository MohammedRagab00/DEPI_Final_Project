CREATE DATABASE StudentManagementSystem;

USE StudentManagementSystem;

-- Create Tables
CREATE TABLE Department (
    id INTEGER PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,
    head_id INTEGER NOT NULL DEFAULT 0
);

--ALTER TABLE Department
--ADD CONSTRAINT UQ_Department_Name UNIQUE (name);

CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    email_address VARCHAR(50) NOT NULL UNIQUE,
    ssn VARCHAR(200) NOT NULL UNIQUE,
    password_hash VARCHAR(150) NOT NULL,
    major INTEGER,
    role VARCHAR(10) NOT NULL DEFAULT 'Unassigned',
    FOREIGN KEY (major) REFERENCES Department(id),
    CHECK (role IN ('Student', 'Tutor', 'Admin', 'Unassigned'))
);

CREATE TABLE Grade (
    student_id INTEGER PRIMARY KEY,
    passed_credit_hours INTEGER NOT NULL DEFAULT 0,
    failed_credit_hours INTEGER DEFAULT 0,
    gpa FLOAT NOT NULL DEFAULT 0.0 CHECK (gpa >= 0 AND gpa <= 5.0),
    FOREIGN KEY (student_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE Courses (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,
    credit_hours INTEGER NOT NULL DEFAULT 3,
    department INTEGER,
    FOREIGN KEY (department) REFERENCES Department(id)
);

CREATE TABLE Course_prerequisite (
    course_id VARCHAR(10),
    prerequisite_id VARCHAR(10),
    PRIMARY KEY (course_id, prerequisite_id),
    FOREIGN KEY (course_id) REFERENCES Courses(id),
    FOREIGN KEY (prerequisite_id) REFERENCES Courses(id) ON DELETE CASCADE
);

CREATE TABLE Place (
    place_num INTEGER PRIMARY KEY,
    department INTEGER,
    capacity INTEGER NOT NULL DEFAULT 30,
    FOREIGN KEY (department) REFERENCES Department(id)
);

-- Create a table for valid days
CREATE TABLE ValidDays (
    day VARCHAR(10) PRIMARY KEY
);

-- Insert valid days into the table
INSERT INTO ValidDays (day) VALUES 
('SATURDAY'), ('SUNDAY'), ('MONDAY'), 
('TUESDAY'), ('WEDNESDAY'), ('THURSDAY');

CREATE TABLE Section (
    id INTEGER PRIMARY KEY,
    course_id VARCHAR(10),
    place INTEGER NOT NULL,
    semester VARCHAR(20) NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('THEORETICAL', 'TUTORIAL', 'LAB')),
    day VARCHAR(10) NOT NULL,
    FOREIGN KEY (day) REFERENCES ValidDays(day),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    group_num INTEGER NOT NULL,
    capacity INTEGER NOT NULL DEFAULT 26,
    instructor_id INTEGER,
    FOREIGN KEY (course_id) REFERENCES Courses(id),
    FOREIGN KEY (place) REFERENCES Place(place_num),
    FOREIGN KEY (instructor_id) REFERENCES Users(id)
);

CREATE TABLE Course_registered (
    student_id INTEGER,
    section_id INTEGER,
    PRIMARY KEY (student_id, section_id),
    FOREIGN KEY (student_id) REFERENCES Users(id),
    FOREIGN KEY (section_id) REFERENCES Section(id)
);

select * from Course_registered

CREATE TABLE Course_grade (
	semester DATE,
    course_id VARCHAR(10),
    student_id INTEGER,
    grade INTEGER NOT NULL,
    gpa_points DECIMAL(3,2),
    PRIMARY KEY (semester, course_id, student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(id),
    FOREIGN KEY (student_id) REFERENCES Users(id)
);

-- Update trigger for Course_grade to automatically calculate GPA points
-- First batch: Check if the trigger exists and drop it if it does
IF EXISTS (
    SELECT * 
    FROM sys.triggers 
    WHERE name = 'TR_CalculateGPAPoints'
)
BEGIN
    DROP TRIGGER TR_CalculateGPAPoints;
END
GO
-- Second batch: Create the trigger
CREATE TRIGGER TR_CalculateGPAPoints
ON Course_grade
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    UPDATE cg
    SET cg.gpa_points = CASE 
        WHEN i.grade BETWEEN 60 AND 64 THEN 1.0 + (i.grade - 60) * 0.1
        WHEN i.grade BETWEEN 65 AND 74 THEN 1.5 + (i.grade - 65) * 0.1
        WHEN i.grade BETWEEN 75 AND 84 THEN 2.5 + (i.grade - 75) * 0.1
        WHEN i.grade BETWEEN 85 AND 100 THEN 3.5 + (i.grade - 85) * 0.1
        ELSE 0.0
    END
    FROM Course_grade cg
    INNER JOIN inserted i 
        ON cg.semester = i.semester 
        AND cg.course_id = i.course_id 
        AND cg.student_id = i.student_id;
END;

-- Populate with sample data
INSERT INTO Department (id, name) VALUES 
(1, 'Computer Science'),
(2, 'Mathematics'),
(3, 'Physics');

INSERT INTO Users (id, first_name, last_name, email_address, ssn, password_hash, major, role) VALUES
(1, 'John', 'Doe', 'john@university.edu', '123-45-6789', 'hashed_password', 1, 'Student'), -- Student
(2, 'Jane', 'Smith', 'jane@university.edu', '987-65-4321', 'hashed_password', NULL, 'Tutor'), -- Tutor
(3, 'Bob', 'Johnson', 'bob@university.edu', '456-78-9012', 'hashed_password', NULL, 'Admin'), -- Admin
(4, 'John', 'Wagdie', 'wagdie@university.edu', '223-45-6789', 'hashed_password', 1, 'Student'), -- Student
(5, '3m', 'Gemi', 'gemi@university.edu', '333-45-6789', 'hashed_password', 1, 'Student'), -- Student
(6, 'Ahmed', 'Mohsen', 'mohsen@university.edu', '543-45-6789', 'hashed_password', 1, 'Student'); -- Student

--INSERT INTO Grade (student_id, passed_credit_hours, gpa) VALUES
--(1, 60, 4.2),
--(4, 70, 2.5),
--(5, 40, 2.4),
--(6, 20, 4.0);

INSERT INTO Courses (id, name, credit_hours, department) VALUES
('CS101', 'Intro to Programming', 3, 1),
('CS201', 'Data Structures', 3, 1),
('MATH101', 'Calculus I', 4, 2);

INSERT INTO Course_prerequisite (course_id, prerequisite_id) VALUES
('CS201', 'CS101');

INSERT INTO Place (place_num, department, capacity) VALUES
(101, 1, 30),
(102, 1, 25),
(201, 2, 40);

INSERT INTO Section (id, course_id, place, semester, type, day, start_time, end_time, group_num, instructor_id) VALUES
(1, 'CS101', 101, 'Fall 2024', 'THEORETICAL', 'MONDAY', '09:00', '10:30', 1, 2),
(2, 'CS201', 102, 'Fall 2024', 'THEORETICAL', 'TUESDAY', '11:00', '12:30', 1, 2),
(3, 'MATH101', 201, 'Fall 2024', 'THEORETICAL', 'WEDNESDAY', '14:00', '15:30', 1, 2);

INSERT INTO Course_registered (student_id, section_id) VALUES
(1, 1),
(1, 3);


-- 5. Trigger to calculate cumulative GPA
-- First, drop the existing trigger if it exists
IF EXISTS (
    SELECT * 
    FROM sys.triggers 
    WHERE name = 'TR_UpdateGradeTable'
)
BEGIN
    DROP TRIGGER TR_UpdateGradeTable;
END
GO
-- Create the trigger
CREATE TRIGGER TR_UpdateGradeTable
ON Course_grade
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Create a table to hold all affected student IDs
    DECLARE @affected_students TABLE (student_id INT);
    
    -- Create a table to hold student-section pairs to be deleted
    DECLARE @delete_registrations TABLE (
        student_id INT,
        section_id INT
    );
    
    -- Get all affected student IDs from inserted and deleted records
    INSERT INTO @affected_students (student_id)
    SELECT student_id FROM inserted
    UNION
    SELECT student_id FROM deleted;
    
    -- Get student-section pairs to delete from Course_registered
    INSERT INTO @delete_registrations (student_id, section_id)
    SELECT i.student_id, s.id
    FROM inserted i
    JOIN Section s ON i.course_id = s.course_id;
    
    -- Delete records from Course_registered
    DELETE cr
    FROM Course_registered cr
    JOIN @delete_registrations dr 
        ON cr.student_id = dr.student_id 
        AND cr.section_id = dr.section_id;
    
    -- Update passed_credit_hours, failed_credit_hours, and gpa for each student
    UPDATE g
    SET 
        passed_credit_hours = ISNULL(p.passed_hours, 0),
        failed_credit_hours = ISNULL(f.failed_hours, 0),
        gpa = CASE 
                WHEN ISNULL(p.passed_hours, 0) + ISNULL(f.failed_hours, 0) > 0 
                THEN ISNULL(gpa_calc.total_points, 0) / (ISNULL(p.passed_hours, 0) + ISNULL(f.failed_hours, 0))
                ELSE 0 
             END
    FROM Grade g
    JOIN @affected_students a ON g.student_id = a.student_id
    LEFT JOIN (
        -- Calculate passed hours
        SELECT cg.student_id, SUM(c.credit_hours) as passed_hours
        FROM Course_grade cg
        JOIN Courses c ON cg.course_id = c.id
        WHERE cg.grade >= 60
        GROUP BY cg.student_id
    ) p ON g.student_id = p.student_id
    LEFT JOIN (
        -- Calculate failed hours
        SELECT cg.student_id, SUM(c.credit_hours) as failed_hours
        FROM Course_grade cg
        JOIN Courses c ON cg.course_id = c.id
        WHERE cg.grade < 60
        GROUP BY cg.student_id
    ) f ON g.student_id = f.student_id
    LEFT JOIN (
        -- Calculate total points
        SELECT cg.student_id, SUM(c.credit_hours * cg.gpa_points) as total_points
        FROM Course_grade cg
        JOIN Courses c ON cg.course_id = c.id
        GROUP BY cg.student_id
    ) gpa_calc ON g.student_id = gpa_calc.student_id;

    -- Insert new records for students not already in Grade table
    INSERT INTO Grade (student_id, passed_credit_hours, failed_credit_hours, gpa)
    SELECT 
        a.student_id,
        ISNULL(p.passed_hours, 0),
        ISNULL(f.failed_hours, 0),
        CASE 
            WHEN ISNULL(p.passed_hours, 0) + ISNULL(f.failed_hours, 0) > 0 
            THEN ISNULL(gpa_calc.total_points, 0) / (ISNULL(p.passed_hours, 0) + ISNULL(f.failed_hours, 0))
            ELSE 0 
        END
    FROM @affected_students a
    LEFT JOIN Grade g ON a.student_id = g.student_id
    LEFT JOIN (
        -- Calculate passed hours
        SELECT cg.student_id, SUM(c.credit_hours) as passed_hours
        FROM Course_grade cg
        JOIN Courses c ON cg.course_id = c.id
        WHERE cg.grade >= 60
        GROUP BY cg.student_id
    ) p ON a.student_id = p.student_id
    LEFT JOIN (
        -- Calculate failed hours
        SELECT cg.student_id, SUM(c.credit_hours) as failed_hours
        FROM Course_grade cg
        JOIN Courses c ON cg.course_id = c.id
        WHERE cg.grade < 60
        GROUP BY cg.student_id
    ) f ON a.student_id = f.student_id
    LEFT JOIN (
        -- Calculate total points
        SELECT cg.student_id, SUM(c.credit_hours * cg.gpa_points) as total_points
        FROM Course_grade cg
        JOIN Courses c ON cg.course_id = c.id
        GROUP BY cg.student_id
    ) gpa_calc ON a.student_id = gpa_calc.student_id
    WHERE g.student_id IS NULL;
END
GO

INSERT INTO Course_grade (semester, course_id, student_id, grade) VALUES
('2024-01-01', 'MATH101', 1, 75);

select * from grade;
select * from Course_grade
select * from Course_registered

INSERT INTO Course_grade (semester, course_id, student_id, grade) VALUES
('2025-01-01', 'CS201', 1, 60);

select * from grade
select * from Course_grade
-- truncate table course_grade
-- Sample Queries for Analysis

-- 1. Get student's current course load
SELECT u.first_name, u.last_name, c.id as course_id, c.name as course_name, s.day, s.start_time, s.end_time
FROM Users u
JOIN Course_registered cr ON u.id = cr.student_id
JOIN Section s ON cr.section_id = s.id
JOIN Courses c ON s.course_id = c.id
WHERE u.id = 1;

-- 2. Calculate department enrollment statistics
SELECT d.name as department_name, COUNT(u.id) as student_count
FROM Department d
LEFT JOIN Users u ON d.id = u.major
WHERE u.role = 'Student'
GROUP BY d.id, d.name;

-- 3. Find courses with prerequisites
SELECT c.name as course_name, p.name as prerequisite_name
FROM Course_prerequisite cp
JOIN Courses c ON cp.course_id = c.id
JOIN Courses p ON cp.prerequisite_id = p.id;

-- 4. Get professor's teaching schedule
SELECT u.first_name, u.last_name, c.name as course_name, s.day, s.start_time, s.end_time, p.place_num
FROM Users u
JOIN Section s ON u.id = s.instructor_id
JOIN Courses c ON s.course_id = c.id
JOIN Place p ON s.place = p.place_num
WHERE u.role = 'Tutor';

-- 5. Find sections that are full
SELECT c.name as course_name, s.id as section_id, s.capacity,
       COUNT(cr.student_id) as enrolled_students
FROM Section s
JOIN Courses c ON s.course_id = c.id
LEFT JOIN Course_registered cr ON s.id = cr.section_id
GROUP BY s.id, c.name, s.capacity
HAVING COUNT(cr.student_id) >= s.capacity;

-- 6. Calculate GPA distribution
SELECT 
    CASE 
        WHEN gpa >= 4.5 THEN '4.5-5.0'
        WHEN gpa >= 4.0 THEN '4.0-4.49'
        WHEN gpa >= 3.5 THEN '3.5-3.99'
        WHEN gpa >= 3.0 THEN '3.0-3.49'
        WHEN gpa >= 2.5 THEN '2.5-2.99'
        WHEN gpa >= 2.0 THEN '2.0-2.49'
        ELSE 'Below 2.0'
    END as gpa_range,
    COUNT(*) as student_count
FROM Grade
GROUP BY 
    CASE 
        WHEN gpa >= 4.5 THEN '4.5-5.0'
        WHEN gpa >= 4.0 THEN '4.0-4.49'
        WHEN gpa >= 3.5 THEN '3.5-3.99'
        WHEN gpa >= 3.0 THEN '3.0-3.49'
        WHEN gpa >= 2.5 THEN '2.5-2.99'
        WHEN gpa >= 2.0 THEN '2.0-2.49'
        ELSE 'Below 2.0'
    END
ORDER BY gpa_range DESC;

-- Additional useful queries for 5.0 GPA scale

-- 1. Find top performers (GPA 4.0 and above)
SELECT u.first_name, u.last_name, g.gpa
FROM Users u
JOIN Grade g ON u.id = g.student_id
WHERE g.gpa >= 4.0 AND role = 'Student'
ORDER BY g.gpa DESC;

-- 2. Calculate average GPA by department
SELECT d.name as department_name, AVG(g.gpa) as avg_gpa
FROM Department d
JOIN Users u ON d.id = u.major
JOIN Grade g ON u.id = g.student_id
GROUP BY d.id, d.name
ORDER BY avg_gpa DESC;

-- 3. GPA percentile calculation
WITH RankedGPAs AS (
  SELECT 
    student_id,
    gpa,
    CUME_DIST() OVER (ORDER BY gpa DESC) * 100 as top_percent
  FROM Grade
)
SELECT 
    u.first_name,
    u.last_name,
    r.gpa,
    ROUND(r.top_percent, 2) as top_percent
FROM RankedGPAs r
JOIN Users u ON r.student_id = u.id AND u.role = 'Student'
ORDER BY r.gpa DESC;

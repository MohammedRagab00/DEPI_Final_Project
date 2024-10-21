use StudentManagementSystem

--Fact Table: GradeFact
CREATE TABLE GradeFact (
  GradeID INT PRIMARY KEY,
  StudentID INT,
  CourseID VARCHAR(10),
  Semester DATE,
  Grade INT,
  GPA_Points DECIMAL(3, 2),
  InstructorID INT
);

--Dimension Tables:

--StudentDim
CREATE TABLE StudentDim (
  StudentID INT PRIMARY KEY,
  FirstName VARCHAR(20),
  LastName VARCHAR(20),
  EmailAddress VARCHAR(50),
  Major INT,
  Role VARCHAR(10)
);

--CourseDim
CREATE TABLE CourseDim (
  CourseID VARCHAR(10) PRIMARY KEY,
  CourseName VARCHAR(20),
  CreditHours INT,
  Department INT
);

--InstructorDim
CREATE TABLE InstructorDim (
  InstructorID INT PRIMARY KEY,
  FirstName VARCHAR(20),
  LastName VARCHAR(20),
  EmailAddress VARCHAR(50),
  Department INT
);


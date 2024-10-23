use StudentManagementSystem


select * from GradeFact

select * from InstructorDim

select * from StudentDim

select * from CourseDim

select * from StudentDim inner join InstructorDim on StudentID = InstructorID


-- Check for invalid StudentID
SELECT gf.GradeID, gf.StudentID, gf.CourseID, gf.Semester, gf.Grade, gf.GPA_Points, gf.InstructorID
FROM GradeFact gf
LEFT JOIN StudentDim sd ON gf.StudentID = sd.StudentID
WHERE sd.StudentID IS NULL;

-- Check for invalid CourseID
SELECT gf.GradeID, gf.StudentID, gf.CourseID, gf.Semester, gf.Grade, gf.GPA_Points, gf.InstructorID
FROM GradeFact gf
LEFT JOIN CourseDim cd ON gf.CourseID = cd.CourseID
WHERE cd.CourseID IS NULL;

-- Check for invalid InstructorID
SELECT gf.GradeID, gf.StudentID, gf.CourseID, gf.Semester, gf.Grade, gf.GPA_Points, gf.InstructorID
FROM GradeFact gf
LEFT JOIN InstructorDim id ON gf.InstructorID = id.InstructorID
WHERE id.InstructorID IS NULL;

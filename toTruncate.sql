use StudentManagementSystem

EXEC sp_msforeachtable "ALTER TABLE ? NOCHECK CONSTRAINT all"


DELETE FROM [dbo].[GradeFact];
DELETE FROM [dbo].[StudentDim];
DELETE FROM [dbo].[CourseDim];
DELETE FROM [dbo].[InstructorDim];
DELETE FROM [dbo].[Department];
DELETE FROM [dbo].[Users];
DELETE FROM [dbo].[Grade];
DELETE FROM [dbo].[Courses];
DELETE FROM [dbo].[Course_prerequisite];
DELETE FROM [dbo].[Place];
DELETE FROM [dbo].[ValidDays];
DELETE FROM [dbo].[Section];
DELETE FROM [dbo].[Course_registered];
DELETE FROM [dbo].[Course_grade];


EXEC sp_msforeachtable "ALTER TABLE ? WITH CHECK CHECK CONSTRAINT all"

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Setup database connection
connection_string = os.getenv("DB_CONNECTION_STRING")
engine = create_engine(connection_string)

# Load CSV files in the specified order
departments = pd.read_csv(
    "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\departments.csv"
)
users = pd.read_csv(
    "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\users.csv"
)
grade = pd.read_csv(
    "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\Grade.csv"
)
courses = pd.read_csv(
    "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\courses.csv"
)
course_prerequisite = pd.read_csv(
    "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\Course_prerequisite.csv"
)
place = pd.read_csv(
    "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\Place.csv"
)
sections = pd.read_csv(
    "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\sections.csv"
)
course_registered = pd.read_csv(
    "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\Course_registered.csv"
)
course_grade = pd.read_csv(
    "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\Course_grade.csv"
)

# Transform Data
# Check if the GradeFact table has the GPA_Points column
with engine.connect() as conn:
    has_gpa_points_column = (
        conn.execute(
            "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'GradeFact' AND COLUMN_NAME = 'GPA_Points'"
        ).scalar()
        > 0
    )

if has_gpa_points_column:
    # Drop the existing GPA_Points column from the GradeFact table
    conn.execute("ALTER TABLE GradeFact DROP COLUMN GPA_Points")

# Example transformation for GradeFact
course_grade["GPA_Points"] = course_grade["grade"] * 0.1  # Example calculation
grade_fact = course_grade.rename(
    columns={
        "semester": "Semester",
        "course_id": "CourseID",
        "student_id": "StudentID",
        "grade": "Grade",
    }
)

# Load data into data warehouse tables
grade_fact.to_sql("GradeFact", con=engine, if_exists="append", index=False)

# Transform and load data for dimension tables
users_dim = users.rename(
    columns={
        "id": "StudentID",
        "first_name": "FirstName",
        "last_name": "LastName",
        "email": "EmailAddress",
        "major": "Major",
        "role": "Role",
    }
)
courses_dim = courses.rename(
    columns={
        "id": "CourseID",
        "name": "CourseName",
        "credit_hours": "CreditHours",
        "department": "Department",
    }
)
instructor_dim = (
    sections[["instructor_id"]]
    .drop_duplicates()
    .rename(columns={"instructor_id": "InstructorID"})
)
instructor_dim = instructor_dim.merge(users, left_on="InstructorID", right_on="id")[
    ["InstructorID", "first_name", "last_name", "email", "major"]
].rename(
    columns={
        "first_name": "FirstName",
        "last_name": "LastName",
        "email": "EmailAddress",
        "major": "Department",
    }
)

# Load dimension tables into the database
users_dim.to_sql("StudentDim", con=engine, if_exists="append", index=False)
courses_dim.to_sql("CourseDim", con=engine, if_exists="append", index=False)
instructor_dim.to_sql("InstructorDim", con=engine, if_exists="append", index=False)

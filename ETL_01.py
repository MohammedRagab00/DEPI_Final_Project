import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Setup database connection
connection_string = os.getenv("DB_CONNECTION_STRING")
engine = create_engine(connection_string)

# Base directory for the CSV files using a relative path
base_directory = "Ignore\\Week2\\Data\\"

# List of CSV file paths
file_names = [
    "departments.csv",
    "users.csv",
    "Grade.csv",
    "courses.csv",
    "Course_prerequisite.csv",
    "Place.csv",
    "sections.csv",
    "Course_registered.csv",
    "Course_grade.csv",
]

# Load CSV files into a dictionary
dataframes = {
    name.split(".")[0]: pd.read_csv(base_directory + name) for name in file_names
}

# Accessing dataframes
departments = dataframes["departments"]
users = dataframes["users"]
grade = dataframes["Grade"]
courses = dataframes["courses"]
course_prerequisite = dataframes["Course_prerequisite"]
place = dataframes["Place"]
sections = dataframes["sections"]
course_registered = dataframes["Course_registered"]
course_grade = dataframes["Course_grade"]

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

# Load data into the GradeFact table
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

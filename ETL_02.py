import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import logging

# Load environment variables from .env file
load_dotenv()

# Setup database connection
connection_string = os.getenv("DB_CONNECTION_STRING")
engine = create_engine(connection_string)

# Hardcode the CSV file paths
CSV_FILE_PATHS = {
    "departments": "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\departments.csv",
    "users": "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\users.csv",
    "grade": "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\Grade.csv",
    "courses": "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\courses.csv",
    "course_prerequisite": "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\Course_prerequisite.csv",
    "place": "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\Place.csv",
    "sections": "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\sections.csv",
    "course_registered": "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\Course_registered.csv",
    "course_grade": "C:\\Study_02\\Material\\DataEngineer\\Final_Project\\Ignore\\Week2\\Data\\Course_grade.csv",
}

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


class ETLPipeline:
    def __init__(self, engine):
        self.engine = engine

    def extract_data(self):
        self.departments = pd.read_csv(CSV_FILE_PATHS["departments"])
        self.users = pd.read_csv(CSV_FILE_PATHS["users"])
        self.grade = pd.read_csv(CSV_FILE_PATHS["grade"])
        self.courses = pd.read_csv(CSV_FILE_PATHS["courses"])
        self.course_prerequisite = pd.read_csv(CSV_FILE_PATHS["course_prerequisite"])
        self.place = pd.read_csv(CSV_FILE_PATHS["place"])
        self.sections = pd.read_csv(CSV_FILE_PATHS["sections"])
        self.course_registered = pd.read_csv(CSV_FILE_PATHS["course_registered"])
        self.course_grade = pd.read_csv(CSV_FILE_PATHS["course_grade"])

    def transform_data(self):
        # Check if the GradeFact table has the GPA_Points column
        with self.engine.connect() as conn:
            has_gpa_points_column = (
                conn.execute(
                    "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'GradeFact' AND COLUMN_NAME = 'GPA_Points'"
                ).scalar()
                > 0
            )

        if has_gpa_points_column:
            # Drop the existing GPA_Points column from the GradeFact table
            with self.engine.begin() as conn:
                conn.execute("ALTER TABLE GradeFact DROP COLUMN GPA_Points")

        # Transform GradeFact
        self.grade_fact = self.course_grade.rename(
            columns={
                "semester": "Semester",
                "course_id": "CourseID",
                "student_id": "StudentID",
                "grade": "Grade",
            }
        )
        self.grade_fact["GPA_Points"] = self.grade_fact["Grade"] * 0.1

        # Transform dimension tables
        self.users_dim = self.users.rename(
            columns={
                "id": "StudentID",
                "first_name": "FirstName",
                "last_name": "LastName",
                "email": "EmailAddress",
                "major": "Major",
                "role": "Role",
            }
        )
        self.courses_dim = self.courses.rename(
            columns={
                "id": "CourseID",
                "name": "CourseName",
                "credit_hours": "CreditHours",
                "department": "Department",
            }
        )
        self.instructor_dim = (
            self.sections[["instructor_id"]]
            .drop_duplicates()
            .rename(columns={"instructor_id": "InstructorID"})
        )
        self.instructor_dim = self.instructor_dim.merge(
            self.users, left_on="InstructorID", right_on="id"
        )[["InstructorID", "first_name", "last_name", "email", "major"]].rename(
            columns={
                "first_name": "FirstName",
                "last_name": "LastName",
                "email": "EmailAddress",
                "major": "Department",
            }
        )

    def load_data(self):
        try:
            # Load dimension tables into the database
            self.users_dim.to_sql(
                "StudentDim", con=self.engine, if_exists="append", index=False
            )
            self.courses_dim.to_sql(
                "CourseDim", con=self.engine, if_exists="append", index=False
            )
            self.instructor_dim.to_sql(
                "InstructorDim", con=self.engine, if_exists="append", index=False
            )

            # Load fact table into the database
            self.grade_fact.to_sql(
                "GradeFact", con=self.engine, if_exists="append", index=False
            )
            logging.info("Data loaded into the data warehouse successfully.")
        except Exception as e:
            logging.error(f"Error occurred while loading data: {e}")
            raise

    def run(self):
        try:
            self.extract_data()
            self.transform_data()
            self.load_data()
            logging.info("ETL process completed successfully.")
        except Exception as e:
            logging.error(f"Error occurred during ETL process: {e}")
            raise


if __name__ == "__main__":
    etl_pipeline = ETLPipeline(engine)
    etl_pipeline.run()

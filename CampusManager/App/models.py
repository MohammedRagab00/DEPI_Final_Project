from App import db, bcrypt, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import validates
from sqlalchemy import func
from flask import flash
from enum import Enum
# from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# class ChatHistory(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     original_text = db.Column(db.Text, nullable=False)
#     summarized_text = db.Column(db.Text, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)

#     # Add relationship to User model
#     user = db.relationship("User", backref=db.backref("chat_history", lazy=True))

#     def __repr__(self):
#         return f"<ChatHistory {self.id}>"


# # Add this to your User model class if you want to track chat history
# chat_histories = db.relationship("ChatHistory", backref="user", lazy=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(length=20), nullable=False, unique=False)
    last_name = db.Column(db.String(length=20), nullable=False, unique=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    ssn = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    major = db.Column(db.Integer(), db.ForeignKey("department.id"))
    role = db.Column("role", db.Integer(), nullable=False, default=3)
    registered_courses = db.relationship(
        "Course_registered", backref="student", lazy=True
    )
    taught_sections = db.relationship(
        "Section", backref="instructor", lazy=True, foreign_keys="Section.instructor_id"
    )
    grade = db.relationship(
        "Grade", uselist=False, back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode(
            "utf-8"
        )

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_enroll(self, sec_obj):
        if Course_registered.query.filter_by(
            student_id=self.id, section_id=sec_obj.id
        ).first():
            return False
        return True

    def can_drop(self, sec_obj):
        if Course_registered.query.filter_by(
            student_id=self.id, section_id=sec_obj.section_id
        ).first():
            return True
        return False

    def __repr__(self):
        return f"User {self.first_name} {self.last_name}"

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter(
            func.lower(cls.email_address) == func.lower(email)
        ).first()

    @validates("email_address")
    def convert_lower(self, key, value):
        return value.lower()


class Grade(db.Model):
    student_id = db.Column(db.Integer(), db.ForeignKey("user.id"), primary_key=True)
    passed_credit_hours = db.Column(db.Integer(), nullable=False, default=0)
    gpa = db.Column(db.Float(), nullable=False, default=0.0)
    user = db.relationship("User", back_populates="grade")
    failed_credit_hours = db.Column(db.Integer(), default=0)

    @validates("student_id")
    def validate_student_role(self, key, student_id):
        user = User.query.get(student_id)
        if user and user.role != 0:
            raise ValueError("Only users with role 0 can have a Grade record.")
        return student_id


class Courses(db.Model):
    id = db.Column(db.String(length=10), primary_key=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    credit_hours = db.Column(db.Integer(), nullable=False, default=3)
    department = db.Column(db.Integer(), db.ForeignKey("department.id"))

    # Relationship to Course_prerequisite
    courses = db.relationship(
        "Course_prerequisite",
        backref="course",
        lazy=True,
        foreign_keys="[Course_prerequisite.prerequisite_id]",
    )

    # Relationship to Section
    sections = db.relationship("Section", back_populates="course", lazy=True)


class Course_prerequisite(db.Model):
    course_id = db.Column(
        db.String(length=10), db.ForeignKey("courses.id"), primary_key=True
    )
    prerequisite_id = db.Column(
        db.String(length=10), db.ForeignKey("courses.id"), primary_key=True
    )


class WeekDay(Enum):
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"


class SectionType(Enum):
    THEORETICAL = "THEORETICAL"
    TUTORIAL = "TUTORIAL"
    LAB = "LAB"


class Section(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    course_id = db.Column(db.String(length=10), db.ForeignKey("courses.id"))
    place = db.Column(db.Integer(), db.ForeignKey("place.place_num"), nullable=False)
    semester = db.Column(db.String(length=20), nullable=False)
    type = db.Column(
        db.Enum(SectionType), nullable=False, default=SectionType.THEORETICAL
    )
    day = db.Column(db.Enum(WeekDay), nullable=False)  # Use Enum for better clarity
    start_time = db.Column(db.Time(), nullable=False)  # Separate start time
    end_time = db.Column(db.Time(), nullable=False)  # Separate end time
    group = db.Column(db.Integer(), nullable=False)
    capacity = db.Column(db.Integer(), nullable=False, default=26)

    # Relationship to Courses with back_populates
    course = db.relationship(
        "Courses", back_populates="sections", foreign_keys=[course_id]
    )

    registered_courses = db.relationship(
        "Course_registered", backref="section", lazy=True
    )
    instructor_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def is_full(self):
        """Check if the section has reached or exceeded its capacity."""
        enrolled_count = Course_registered.query.filter_by(section_id=self.id).count()
        return enrolled_count >= self.capacity

    @staticmethod
    def check_time_conflict(existing_sections, new_section):
        for enrolled_sec in existing_sections:
            if (
                enrolled_sec.start_time < new_section.end_time
                and new_section.start_time < enrolled_sec.end_time
                and enrolled_sec.day == new_section.day
            ):
                return True  # Conflict detected
        return False  # No conflict


class Course_registered(db.Model):
    student_id = db.Column(db.Integer(), db.ForeignKey("user.id"), primary_key=True)
    section_id = db.Column(db.Integer(), db.ForeignKey("section.id"), primary_key=True)

    def unregister_and_grade(self, grade):
        # Create or update a Course_grade entry
        course_grade = Course_grade.query.filter_by(
            semester=self.section.semester,
            course_id=self.section.course_id,
            student_id=self.student_id,
        ).first()

        if course_grade:
            course_grade.grade = grade
        else:
            course_grade = Course_grade(
                semester=self.section.semester,
                course_id=self.section.course_id,
                student_id=self.student_id,
                grade=grade,
            )
            db.session.add(course_grade)

        # Get the course credit hours from Section
        course = self.section.course
        if not course:
            flash("Course not found for the section.", "danger")
            return

        course_credit_hours = course.credit_hours

        user = User.query.get(self.student_id)
        if user:
            grade_record = user.grade
            if not grade_record:
                # Create a Grade record if it does not exist
                grade_record = Grade(student_id=user.id)
                db.session.add(grade_record)

            # Update the GPA (weighted by course credit hours)
            self.update_gpa(grade_record, grade, course_credit_hours)

        # Delete all registrations matching course_id and group
        registrations_to_delete = (
            Course_registered.query.join(Section)
            .filter(
                Course_registered.student_id == self.student_id,
                Section.course_id == self.section.course_id,
                Section.group == self.section.group,
            )
            .all()
        )

        for registration in registrations_to_delete:
            db.session.delete(registration)

        db.session.commit()

    def update_gpa(self, grade_record, grade, course_credit_hours):
        gpa_value = self.grade_to_gpa(grade)

        # Calculate new total credits and GPA points
        new_total_credits = (
            grade_record.passed_credit_hours
            + grade_record.failed_credit_hours
            + course_credit_hours
        )
        total_gpa_points = grade_record.gpa * (
            grade_record.passed_credit_hours + grade_record.failed_credit_hours
        )
        new_total_points = total_gpa_points + (gpa_value * course_credit_hours)

        if grade >= 60:
            grade_record.passed_credit_hours += course_credit_hours
        else:
            grade_record.failed_credit_hours += course_credit_hours

        # Calculate new GPA
        if new_total_credits > 0:
            grade_record.gpa = min(new_total_points / new_total_credits, 5)
        else:
            grade_record.gpa = 0

        db.session.commit()

    @staticmethod
    def grade_to_gpa(grade):
        """Convert a numeric grade to the corresponding GPA."""
        if 60 <= grade <= 64:
            return 1.0 + (grade - 60) * 0.1
        elif 65 <= grade <= 74:
            return 1.5 + (grade - 65) * 0.1
        elif 75 <= grade <= 84:
            return 2.5 + (grade - 75) * 0.1
        elif 85 <= grade <= 100:
            return 3.5 + (grade - 85) * 0.1
        return 0  # GPA is 0 for grades below 60


class Course_grade(db.Model):
    semester = db.Column(db.String(length=20), primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey("courses.id"), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey("user.id"), primary_key=True)
    grade = db.Column(db.Integer(), nullable=False)


class Place(db.Model):
    place_num = db.Column(db.Integer(), primary_key=True)
    department = db.Column(db.Integer(), db.ForeignKey("department.id"))
    capacity = db.Column(db.Integer(), nullable=False, default=30)
    sections = db.relationship("Section", backref="place_ref", lazy=True)


class Department(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=20), nullable=False)
    head_id = db.Column(
        db.Integer(), db.ForeignKey("user.id"), nullable=False, default=0
    )

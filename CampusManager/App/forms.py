from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    IntegerField,
    HiddenField,
    TimeField,
    SelectField,
)
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from App.models import (
    User,
    Courses,
    Department,
    Place,
    Section,
    Course_prerequisite,
    SectionType,
    WeekDay,
)
from flask import flash


class RegisterForm(FlaskForm):
    def validate_ssn(self, ssn_to_check):
        user = User.query.filter_by(ssn=ssn_to_check.data).first()
        if user:
            raise ValidationError("Ssn already exists!")
        if len(ssn_to_check.data) != 14:
            raise ValidationError("Ssn must be exactly 14 characters long.")
        if (
            int(ssn_to_check.data[5:7]) < 1
            or int(ssn_to_check.data[5:7]) > 31
            or int(ssn_to_check.data[3:5]) < 1
            or int(ssn_to_check.data[3:5]) > 12
            or int(ssn_to_check.data[1:3]) < 0
        ):
            raise ValidationError("Invalid Ssn.")

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(
            email_address=email_address_to_check.data
        ).first()
        if email_address:
            raise ValidationError(
                "Email Address already exists! Please try a different email"
            )

    first_name = StringField(
        label="First name: ", validators=[Length(min=2, max=14), DataRequired()]
    )
    last_name = StringField(
        label="Last name: ", validators=[Length(min=2, max=14), DataRequired()]
    )
    ssn = StringField(label="Ssn: ", validators=[DataRequired()])
    email_address = StringField(
        label="Email Address: ", validators=[Email(), DataRequired()]
    )
    password1 = PasswordField(
        label="Password: ", validators=[Length(min=6, max=60), DataRequired()]
    )
    password2 = PasswordField(
        label="Confirm Password: ", validators=[EqualTo("password1"), DataRequired()]
    )
    submit = SubmitField(
        label="Create Account",
    )


class LoginForm(FlaskForm):
    email_address = StringField(label="Email: ", validators=[DataRequired()])
    password = PasswordField(label="Password: ", validators=[DataRequired()])
    submit = SubmitField(
        label="Sign In",
    )


class AddDepartmentForm(FlaskForm):
    def validate_name(self, name_to_check):
        user = Courses.query.filter_by(name=name_to_check.data).first()
        if user:
            raise ValidationError("Department already exists!")

    name = StringField(label="Name: ", validators=[DataRequired()])
    head_id = IntegerField(label="Department Head ID: ", default=0)

    submit = SubmitField(label="Add Department")


class AddSectionForm(FlaskForm):
    def validate_course_id(self, course_id_to_check):
        course_id = Courses.query.filter_by(id=course_id_to_check.data).first()
        if not course_id:
            raise ValidationError("Course Id doesn't exist!")

    def validate_capacity(self, field):
        place_num = self.place.data
        section_capacity = field.data

        place = Place.query.filter_by(place_num=place_num).first()
        if not place:
            raise ValidationError("Place not found.")

        if section_capacity > place.capacity:
            raise ValidationError(
                "Section capacity cannot be greater than the place capacity."
            )

    def validate_combination(self):
        course_id = self.course_id.data
        section_type = self.type.data
        group = self.group.data

        section = Section.query.filter_by(
            course_id=course_id, type=section_type, group=group
        ).first()
        if section:
            flash(
                "This combination of Course ID, Type, and Group already exists.",
                category="danger",
            )
            return False
        return True

    def validate_end_time(self, end_time):
        if self.start_time.data and end_time.data <= self.start_time.data:
            raise ValidationError("End time must be after start time.")

    def validate(self, extra_validators=None):
        if not super(AddSectionForm, self).validate(extra_validators):
            return False

        if not self.validate_combination():
            return False

        return True

    course_id = StringField(label="Course Id: ", validators=[DataRequired()])
    place = IntegerField(label="Place Num: ", validators=[DataRequired()])
    semester = StringField(
        label="Semester: ", validators=[DataRequired(), Length(max=20)]
    )
    type = SelectField(
        "Type",
        choices=[
            (SectionType.THEORETICAL.name, "Theoretical"),
            (SectionType.TUTORIAL.name, "Tutorial"),
            (SectionType.LAB.name, "Lab"),
        ],
        validators=[DataRequired()],
    )
    day = SelectField(
        "Day",
        choices=[
            (WeekDay.SATURDAY.name, "Saturday"),
            (WeekDay.SUNDAY.name, "Sunday"),
            (WeekDay.MONDAY.name, "Monday"),
            (WeekDay.TUESDAY.name, "Tuesday"),
            (WeekDay.WEDNESDAY.name, "Wednesday"),
            (WeekDay.THURSDAY.name, "Thursday"),
        ],
        validators=[DataRequired()],
    )
    start_time = TimeField(label="Start Time: ", validators=[DataRequired()])
    end_time = TimeField(label="End Time: ", validators=[DataRequired()])
    group = IntegerField(label="Group: ", validators=[DataRequired()])
    capacity = IntegerField(label="Max capacity: ", validators=[DataRequired()])

    submit = SubmitField(label="Add Section")


class AddCourseForm(FlaskForm):
    def validate_id(self, id_to_check):
        user = Courses.query.filter_by(id=id_to_check.data).first()
        if user:
            raise ValidationError("Course already exists!")

    def validate_credit_hours(self, credit_hours_to_check):
        if credit_hours_to_check.data < 0 or credit_hours_to_check.data > 5:
            raise ValidationError("Credit hours should be between 0-5")

    def validate_department(self, department_to_check):
        department = Department.query.filter_by(id=department_to_check.data).first()
        if department:
            pass
        else:
            raise ValidationError("Department number doesn't exist!")

    id = StringField(label="Course ID: ", validators=[DataRequired()])
    name = StringField(label="Name: ", validators=[DataRequired()])
    credit_hours = IntegerField(label="Credit hours: ", validators=[DataRequired()])
    department = IntegerField(label="Department number", validators=[DataRequired()])

    submit = SubmitField(label="Add Course")


class AddPlaceForm(FlaskForm):
    def validate_place_num(self, place_num_to_check):
        place_num = Place.query.filter_by(place_num=place_num_to_check.data).first()
        if place_num:
            raise ValidationError("Place already exists!")

    def validate_capacity(self, capacity_to_check):
        if capacity_to_check.data < 10 or capacity_to_check.data > 120:
            raise ValidationError("Capacity should be between 10-120")

    def validate_department(self, department_to_check):
        department = Department.query.filter_by(id=department_to_check.data).first()
        if department:
            pass
        else:
            raise ValidationError("Department number doesn't exist!")

    place_num = IntegerField(label="Place Num: ", validators=[DataRequired()])
    department = IntegerField(label="Department Num: ", validators=[DataRequired()])
    capacity = IntegerField(label="Capacity", validators=[DataRequired()])

    submit = SubmitField(label="Add Place")


class EnrollSectionForm(FlaskForm):
    submit = SubmitField(
        label="Enroll Section!",
    )


class DropSectionForm(FlaskForm):
    submit = SubmitField(
        label="Drop Section!",
    )


class EditRoleForm(FlaskForm):
    submit = SubmitField(
        label="Save!",
    )


class DeleteUserForm(FlaskForm):
    submit = SubmitField(
        label="Delete!",
    )


class AddCoursePrerequisiteForm(FlaskForm):
    def validate_course_id(self, course_id_to_check):
        course = Courses.query.filter_by(id=course_id_to_check.data).first()
        if course:
            pass
        else:
            raise ValidationError("Course doesn't exist!")

    def validate_prerequisite_id(self, prerequisite_id_to_check):
        course = Courses.query.filter_by(id=prerequisite_id_to_check.data).first()
        if course:
            pass
        else:
            raise ValidationError("Course Prerequisite doesn't exist!")

    def validate_combination(self):
        course_id = self.course_id.data
        prerequisite_id = self.prerequisite_id.data

        # Query the database to check if the combination already exists
        coursePrerequisite = Course_prerequisite.query.filter_by(
            course_id=course_id, prerequisite_id=prerequisite_id
        ).first()
        if coursePrerequisite:
            flash(
                "This combination of Course ID, and Course Prerequisite already exists.",
                category="danger",
            )
            return False
        if course_id == prerequisite_id:
            flash(
                "Course ID and Prerequisite ID cannot be the same.", category="danger"
            )
            return False
        return True

    def validate(self, extra_validators=None):
        """Override the validate method to include custom validation."""
        if not super(AddCoursePrerequisiteForm, self).validate(extra_validators):
            return False

        # Call the custom combination validator
        if not self.validate_combination():
            return False

        return True

    course_id = StringField(label="Course ID: ", validators=[DataRequired()])
    prerequisite_id = StringField(
        label="Course Prerequisite: ", validators=[DataRequired()]
    )

    submit = SubmitField(label="Add Course Prerequisite")


class RegisterTeachingForm(FlaskForm):
    section_id = IntegerField(label="Section ID", validators=[DataRequired()])
    action = HiddenField(default="register")  # Add this hidden field
    submit = SubmitField(label="Register for Teaching")


class UnRegisterTeachingForm(FlaskForm):
    section_id = IntegerField(label="Section ID", validators=[DataRequired()])
    action = HiddenField(default="unregister")  # Add this hidden field
    submit = SubmitField(label="UnRegister from Teaching")


class GradeStudentForm(FlaskForm):
    student_id = IntegerField(label="Student ID", validators=[DataRequired()])
    grade = IntegerField(label="Grade", validators=[DataRequired()])
    submit = SubmitField(label="Submit Grade")

    def validate_grade(self, field):
        if field.data < 0 or field.data > 100:
            raise ValidationError("Grade must be between 0 and 100.")

    def validate_student_id(self, field):
        user = User.query.get(field.data)
        if not user or user.role != 0:
            raise ValidationError(
                "Invalid student ID or student does not have the correct role."
            )


class ForgotPasswordForm(FlaskForm):
    email_address = StringField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Send Reset Link")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("New Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")

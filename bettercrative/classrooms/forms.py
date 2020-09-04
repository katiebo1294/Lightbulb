from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, Optional
from bettercrative.models import Classroom


# Teacher can create an empty classroom with a unique name
class ClassroomForm(FlaskForm):
    name = TextAreaField('Title', validators=[InputRequired(), Length(max=20, message='Must be shorter than 20 characters')])

    def validate_name(self, name):
        name = Classroom.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That name has already been taken. Please choose another.')

    submitClass = SubmitField('Create Classroom')


# Student enters a classroom by inputting the unique classroom name
class EnterClassroomForm(FlaskForm):
    room_id = StringField('Room ID', validators=[InputRequired()])
    submit = SubmitField('Enter Classroom')


# Teacher can add an existing quiz or create a new one to be added to the current classroom
class AddQuizForm(FlaskForm):
    quiz = SelectField('Choose a Quiz', coerce=int, validators=[InputRequired('Please select a quiz.')])
    submit = SubmitField('Add Quiz')


class StudentForm(FlaskForm):
    name = StringField('Fill in Name here',validators=[InputRequired(), Length(min=3, max=20)])
    submit = SubmitField('Submit')


class SetActiveForm(FlaskForm):
    require_usernames = BooleanField('Require student usernames?', validators=[Optional()])
    generate_qr = BooleanField('Generate QR code for student sign-in?', validators=[Optional()])
    submit = SubmitField('Set Active')
    # TODO other options we want to have for active quizzes

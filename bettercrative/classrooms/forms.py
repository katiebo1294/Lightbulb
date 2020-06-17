from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError

from bettercrative.models import Classroom


# Teacher can create an empty classroom with a unique name
class ClassroomForm(FlaskForm):
    name = StringField('Title', validators=[InputRequired(), Length(min=4, max=15, message='Must be at least 4 chars')])

    def validate_name(self, name):
        name = Classroom.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That name has already been taken. Please choose another.')

    submit = SubmitField('Create Classroom')


# Student enters a classroom by inputting the unique classroom name
class EnterClassroomForm(FlaskForm):
    room_id = StringField('Room ID', validators=[InputRequired()])
    submit = SubmitField('Enter Classroom')


# Teacher can add an existing quiz or create a new one to be added to the current classroom
class AddQuizForm(FlaskForm):
    quiz = SelectField('Choose a Quiz', coerce=int, validators=[InputRequired('Please select a quiz.')])
    submit = SubmitField('Add Quiz')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList, FormField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError


class QuizForm(FlaskForm):
    #questions and answers and stuff
    submit = SubmitField('Create Quiz')


class ClassroomForm(FlaskForm):
    classroom_Name = StringField('Title', validators=[InputRequired()])
    key = PasswordField('Key', validators=[InputRequired(), Length(min=4, max=15)])

    def validate_key(self, key):
        if key:
            raise ValidationError('That key has already been taken. Please choose another.')

    submit = SubmitField('Create Classroom')

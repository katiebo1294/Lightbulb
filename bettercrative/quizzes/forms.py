from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList, FormField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError

class QuizForm(FlaskForm):
    #questions and answers and stuff
    submit = SubmitField('Create Quiz')
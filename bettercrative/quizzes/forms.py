from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, Form, BooleanField, IntegerField
from wtforms.validators import InputRequired

# Each answer has some content and whether or not it is correct
class AnswerForm(FlaskForm):
    content = StringField('Answer', validators=[InputRequired('Please fill out this field.')])
    correct = BooleanField('Correct?')

# Currently, a quiz has one question with a list of answers attached to it
class QuestionForm(FlaskForm):
    content = StringField('Question', validators=[InputRequired('Please fill out this field.')])
    category = SelectField('Type', choices=[('Multiple Choice', 'Multiple Choice'), ('True/False', 'True/False'), ('Short Answer', 'Short Answer'), ('IDE', 'IDE')])
    submit = SubmitField('Add Question')

class QuizForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired('Please fill out this field.')])
    submit = SubmitField('Create Quiz')

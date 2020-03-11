from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, Form, BooleanField, IntegerField
from wtforms.validators import InputRequired

# Each answer has some content and whether or not it is correct
class AnswerForm(Form):
    content = StringField('Answer', validators=[InputRequired('Please fill out this field.')])
    correct = BooleanField('Correct?')

# Currently, a quiz has one question with a list of answers attached to it
class QuizForm(FlaskForm):
    name = StringField('Title', validators=[InputRequired('Please fill out this field.')])
    question_content = StringField('Question', validators=[InputRequired('Please fill out this field.')])
    question_answers = FieldList(FormField(AnswerForm), min_entries=4)
    submit = SubmitField('Create Quiz')

# TODO change these forms when we rearrange the database
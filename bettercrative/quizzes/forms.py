from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, Form, BooleanField, IntegerField
from wtforms.validators import InputRequired


class AnswerForm(Form):
    content = StringField('Answer', validators=[InputRequired('Please fill out this field.')])
    # TODO user must select at least one correct answer
    correct = BooleanField('Correct?')


class QuizForm(FlaskForm):
    name = StringField('Title', validators=[InputRequired('Please fill out this field.')])
    question_content = StringField('Question', validators=[InputRequired('Please fill out this field.')])
    question_answers = FieldList(FormField(AnswerForm), min_entries=4)
    submit = SubmitField('Create Quiz')

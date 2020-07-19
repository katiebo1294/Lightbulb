from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import InputRequired



class AnswerForm(FlaskForm):
    content = StringField('Answer', validators=[InputRequired('Please fill out this field.')])
    correct = BooleanField('Correct')
    submit = SubmitField('Save')


class QuestionForm(FlaskForm):
    content = StringField('Question', validators=[InputRequired('Please fill out this field.')])
    submit = SubmitField('Save')


class QuizForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired('Please fill out this field.')])
    submit = SubmitField('Create Quiz')

class QuestionFormOverall(FlaskForm):
    answer_form = wtforms.FormField(AnswerForm)
    question_form = wtforms.FormField(QuestionForm)

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FormField, FieldList, TextAreaField, RadioField
from wtforms.validators import InputRequired, Optional, Length
from wtforms.widgets import TextArea

from bettercrative.models import Quiz


class AnswerForm(FlaskForm):
    content = TextAreaField('Answer', validators=[Optional()])
    correct = BooleanField('Correct')
    submit = SubmitField('Save')


class QuestionForm(FlaskForm):
    content = TextAreaField('Question', validators=[Optional()])
    submit = SubmitField('Save')


class QuizForm(FlaskForm):
    name = TextAreaField('Name', validators=[InputRequired(), Length(max=60, message='Must be shorter than 60 characters')])
    submitQuiz = SubmitField('Create Quiz')


class TFform(FlaskForm):
    content = StringField('Answer', validators=[Optional()])
    correct = BooleanField('Correct')
    submit = SubmitField('Save')


class QuestionFormOverall(FlaskForm):
    answer_form = FieldList(FormField(AnswerForm))
    question_form = FormField(QuestionForm)
    submit = SubmitField('Save Changes')


class QuestionFormOverallTF(FlaskForm):
    answer_form = FieldList(FormField(TFform))
    question_form = FormField(QuestionForm)
    submit = SubmitField('Save Changes')

class QuestionFormOverallSA(FlaskForm):
    answer_form = TextAreaField(u'short answer here')
    question_form = FormField(QuestionForm)
    submit = SubmitField('Save Changes')


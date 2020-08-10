from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FormField, FieldList, TextAreaField, RadioField
from wtforms.validators import InputRequired, Optional
from wtforms.widgets import TextArea

class BetterStringField(StringField):
    widget = TextArea()

class AnswerForm(FlaskForm):
    content = BetterStringField('Answer', validators=[Optional()])
    correct = BooleanField('Correct')
    submit = SubmitField('Save')


class QuestionForm(FlaskForm):
    content = BetterStringField('Question', validators=[Optional()])
    submit = SubmitField('Save')


class QuizForm(FlaskForm):
    name = BetterStringField('Name', validators=[Optional()])
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


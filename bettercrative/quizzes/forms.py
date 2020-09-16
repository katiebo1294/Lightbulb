from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FormField, FieldList, TextAreaField, RadioField, Form
from wtforms.validators import InputRequired, Optional
from wtforms.widgets import TextArea

class AnswerForm(Form):
    content = TextAreaField('Answer', validators=[Optional()])
    correct = BooleanField('Correct')
    submit = SubmitField('Save')


class QuestionForm(Form):
    content = TextAreaField('Question', validators=[Optional()])
    submit = SubmitField('Save')


class QuizForm(FlaskForm):
    name = TextAreaField('Name', validators=[InputRequired()])
    submitQuiz = SubmitField('Create Quiz')


class TFform(Form):
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


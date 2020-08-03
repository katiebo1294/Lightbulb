from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FormField, FieldList, TextAreaField, RadioField
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea

class BetterStringField(StringField):
    widget = TextArea()

class AnswerForm(FlaskForm):
    content = BetterStringField('Answer', validators=[InputRequired('Please fill out this field.')])
    correct = BooleanField('Correct')
    submit = SubmitField('Save')


class QuestionForm(FlaskForm):
    content = BetterStringField('Question', validators=[InputRequired('Please fill out this field.')])
    submit = SubmitField('Save')


class QuizForm(FlaskForm):
    name = BetterStringField('Name', validators=[InputRequired('Please fill out this field.')])
    submitQuiz = SubmitField('Create Quiz')

class TFform(FlaskForm):
    content = StringField('Answer', validators=[InputRequired('Please fill out this field.')])
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


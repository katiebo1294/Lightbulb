from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, TextField
from wtforms.validators import InputRequired, Length, ValidationError


class AnswerForm(FlaskForm):
    # TODO will this work for all question types?
    content = StringField(validators=[InputRequired()])


class QuestionForm(FlaskForm):
    content = StringField('Content', validators=[InputRequired()])
    type = SelectField(u'Question Type', choices=[(('T/F', 'True or False'), ('MC', 'Multiple Choice'),
                                                   ('SA', 'Short Answer'), ('IDE', 'Code'))])
    answers = FieldList(FormField(AnswerForm))


class QuizForm(FlaskForm):
    name = StringField('Title', validators=[InputRequired()])
    questions = FieldList(FormField(QuestionForm))
    submit = SubmitField('Create Quiz')

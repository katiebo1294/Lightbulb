from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, Form
from wtforms.validators import InputRequired, Length, ValidationError


class AnswerForm(Form):
    # TODO will this work for all question types?
    content = StringField('Answer Content', validators=[InputRequired()])


class QuestionForm(Form):
    content = StringField('Question Content', validators=[InputRequired()])
    qtype = SelectField('Question Type', choices=[(('T/F', 'True or False'), ('MC', 'Multiple Choice'),
                                                  ('SA', 'Short Answer'), ('IDE', 'Code'))])
    answers = FieldList(FormField(AnswerForm), min_entries=2, max_entries=4)  # TODO increase limit on answers


class QuizForm(FlaskForm):
    name = StringField('Title', validators=[InputRequired()])
    questions = FieldList(FormField(QuestionForm), min_entries=1, max_entries=20)  # TODO increase limit on questions
    submit = SubmitField('Create Quiz')

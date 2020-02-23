from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, RadioField
from wtforms.validators import InputRequired


class AnswerForm(FlaskForm):
    # TODO will this work for all question types?
    content = StringField('Answer', validators=[InputRequired()])


class QuestionForm(FlaskForm):
    content = StringField('Question', validators=[InputRequired()])
    qtype = RadioField('Question Type', choices=[('T/F', 'True/False'), ('MC', 'Multiple Choice'),
                                                  ('SA', 'Short Answer'), ('IDE', 'Code')])
    answers = FieldList(FormField(AnswerForm), min_entries=4)  # TODO increase limit on answers


class QuizForm(FlaskForm):
    name = StringField('Title', validators=[InputRequired()])
    questions = FieldList(FormField(QuestionForm), min_entries=1)  # TODO increase limit on questions
    submit = SubmitField('Create Quiz')

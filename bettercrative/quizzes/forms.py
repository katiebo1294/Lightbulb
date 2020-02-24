from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField
from wtforms.validators import InputRequired


class AnswerForm(FlaskForm):
    # TODO will this work for all question types?
    content = StringField('Answer', validators=[InputRequired('Please fill out this field.')])


class QuestionForm(FlaskForm):
    content = StringField('Question', validators=[InputRequired('Please fill out this field.')])
    qtype = SelectField('Question Type', choices=[('T/F', 'True/False'), ('MC', 'Multiple Choice'),
                                                  ('SA', 'Short Answer'), ('IDE', 'Code')],
                        validators=[InputRequired('Please fill out this field.')])
    answers = FieldList(FormField(AnswerForm), min_entries=4)


class QuizForm(FlaskForm):
    name = StringField('Title', validators=[InputRequired('Please fill out this field.')])
    questions = FieldList(FormField(QuestionForm), min_entries=1)
    submit = SubmitField('Create Quiz')

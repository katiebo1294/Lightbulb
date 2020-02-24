from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, Form
from wtforms.validators import InputRequired


class AnswerForm(Form):
    # TODO will this work for all question types?
    content = StringField('Answer', validators=[InputRequired('Please fill out this field.')])


class QuizForm(FlaskForm):
    name = StringField('Title', validators=[InputRequired('Please fill out this field.')])
    question_content = StringField('Question', validators=[InputRequired('Please fill out this field.')])
    question_answers = FieldList(FormField(AnswerForm), min_entries=4)
    classroom = StringField('Classroom', validators=[InputRequired('Please fill out this field.')])
    submit = SubmitField('Create Quiz')

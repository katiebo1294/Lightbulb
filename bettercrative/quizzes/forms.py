from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList, FormField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError


class AnswerForm(FlaskForm):
    answer_type = StringField(validators=[InputRequired()])


class QuestionForm(FlaskForm):
    answers = FieldList(FormField(AnswerForm))


class QuizForm(FlaskForm):
    quiz_Name = StringField('Title', validators=[InputRequired()])
    questions = FieldList(FormField(QuestionForm))
    submit = SubmitField('Create Quiz')

# TODO: how to allow user to add however many questions and answers they want
# TODO: how to have different question types (i.e., true/false, multiple choice, short answer, IDE, etc.)

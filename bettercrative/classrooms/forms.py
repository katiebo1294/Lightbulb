from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList, FormField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
from bettercrative.models import Classroom


class ClassroomForm(FlaskForm):
    name = PasswordField('Title', validators=[InputRequired(), Length(min=4, max=15)])

    def validate_name(self, name):
        name = Classroom.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That name has already been taken. Please choose another.')

    submit = SubmitField('Create Classroom')

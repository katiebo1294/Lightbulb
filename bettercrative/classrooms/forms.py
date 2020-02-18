from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList, FormField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
from bettercrative.models import Classroom



class ClassroomForm(FlaskForm):
    classroom_Name = StringField('Title', validators=[InputRequired()])
    key = PasswordField('Key', validators=[InputRequired(), Length(min=4, max=15)])

    def validate_key(self, key):
        key = Classroom.query.filter_by(key=key.data).first()
        if key:
            raise ValidationError('That key has already been taken. Please choose another.')

    submit = SubmitField('Create Classroom')





class enterClassroom(FlaskForm):
    input_key = StringField('What is the key', validators=[InputRequired()])
    
    def validate_entrance(self, input_key, key):
        key = Classroom.query.filter_by(key=key.data).first()
        if not (input_key==key):
            raise ValidationError('There is not key that is that')

    submit = SubmitField('Enter Classroom')
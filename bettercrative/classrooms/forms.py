from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList, FormField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
from bettercrative.models import Classroom


class ClassroomForm(FlaskForm):
    classroom_Name = StringField('Classroom Name', validators=[InputRequired()])
    key = PasswordField('Key', validators=[InputRequired(), Length(min=4, max=15)])

    def validate_key(self, key):
        key = Classroom.query.filter_by(key=key.data).first()
        if key:
            raise ValidationError('That key has already been taken. Please choose another.')

    submit = SubmitField('Create Classroom')



class enterClassroom(FlaskForm):
    classroomName = StringField("What is the classrooms name", validators=[InputRequired()])
    input_key = StringField('What is the key', validators=[InputRequired()])
    submit = SubmitField('Enter Classroom')


    def validate_entrance(self, input_key, classroomName):
        key = Classroom.query.filter_by(key=input_key.data).first()
        getName = Classroom.query.filter_by(classroom_Name=classroomName.data).first()
        
        if getName and not(key): #If that classroom name exists and the key is wrong 
            raise ValidationError('There is not key that is that')
        elif getName and (key):
            return True
        


#FROM CLASSROOM WHERE classroom_Name = inputed classroomNamedata

#if that classroom_name does not exists - just continue b/c no issue
# if that classrom_name does exist, check the users key to the key for that 
# classroom id. If t
# if that classroom


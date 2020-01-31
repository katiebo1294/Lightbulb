from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList, FormField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError



class ClassroomForm(FlaskForm):
    classroom_Name = StringField('Title', validators=[InputRequired()])
    classroom_Content = StringField('Content', validators=[InputRequired()])
    key = PasswordField('Key', validators=[InputRequired(), Length(min=4, max=15)])


    #Questions about this method below
    #I think that since key is a string, we could change the if statement to search the database for the key 
    #and check if the values of the key and whats in the database is equal instead ? - Hansel

    def validate_key(self, key): 
        if key:
            raise ValidationError('That key has already been taken. Please choose another.')

    submit = SubmitField('Create Classroom')

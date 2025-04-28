# Add any form classes for Flask-WTF here

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , IntegerField, BooleanField, FloatField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    photo = FileField('Profile Photo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])



class ProfileForm(FlaskForm):
    user_id_fk = IntegerField('User ID', validators=[DataRequired()])
    description = StringField('Description')
    parish = StringField('Parish')
    biography = StringField('Biography')
    sex = StringField('Sex')
    race = StringField('Race')
    birth_year = IntegerField('Birth Year')
    height = FloatField('Height')
    fav_cuisine = StringField('Favourite Cuisine')
    fav_colour = StringField('Favourite Colour')
    fav_school_subject = StringField('Favourite School Subject')
    political = BooleanField('Political')
    religious = BooleanField('Religious')
    family_oriented = BooleanField('Family Oriented')


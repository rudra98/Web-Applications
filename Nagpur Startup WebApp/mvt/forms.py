from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DecimalField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from mvt.models import User
from datetime import datetime


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    terms = BooleanField('I have read the ',validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class EventForm(FlaskForm):
    eventname = StringField('Event Name',
                        validators=[DataRequired()])
    eventlocation = StringField('Event Location',
                        validators=[DataRequired()])
    eventdate = DateField('Event Date', validators=[DataRequired()], format="%Y-%m-%d %H %m %s")
    description = TextAreaField('Description',
                        validators=[DataRequired()])
    submit = SubmitField('Submit')
    #attend = SubmitField('Attend')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    firstname = StringField('First Name',
                           validators=[Length(min=2, max=20)])
    lastname = StringField('Last Name',
                           validators=[Length(min=2, max=20)])
    designation = SelectField('Designation',choices=[('explorer', 'Explorer'), ('startup', 'Self Employed'),
                    ('facilitator', 'Facilitator'),('enabler', 'Enabler')],validators=[DataRequired()])
    address = TextAreaField('Address')
    pincode = DecimalField('Pincode',places=6)
    contactno = DecimalField('Contact Number',places=9)
    aboutme = TextAreaField('About Me')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
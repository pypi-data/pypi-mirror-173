from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError


class StaffLoginForm(FlaskForm):
    pin = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=4, max=15,
               message="Password needs to be between 4 - 15 digits.")])
    submit = SubmitField('Login')


class AddUserForm(FlaskForm):
    """
    Form to add a user.
    """
    username = StringField('User Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Submit')

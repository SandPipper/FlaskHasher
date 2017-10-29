from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
                    ValidationError, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from ..models import User


class SignUpForm(FlaskForm):
    email = StringField("Email", validators=[Required(),
        Email("Please enter a valid email address.")])

    username = StringField('Username', validators=[Required(), Length(3, 64,
        message="Your username must be at least 3 characters."),
        Regexp("^[A-Za-zА-Яа-я][A-Za-z0-9_.А-Яа-я0-9_.]*$", 0,
        "Usernames must have only letters, numbers, dots or underscores")])

    password = PasswordField('Password', validators=[Required(), Length(8, 64,
        message="Your password must be at least 8 characters."),
        EqualTo('password2', message="Passwords must match.")])

    password2 = PasswordField('Confirm password', validators=[Required()])

    submitSignUp = SubmitField('Sign Up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class SignInForm(FlaskForm):
    email = StringField("Email", validators=[Required(),
        Email("Please enter a valid email address.")])

    password = PasswordField("Password", validators=[Required(), Length(8, 64,
        message="Your password must be at least 8 characters.")])

    remember_me = BooleanField("Remember me")
    submitSignIn = SubmitField('Sign In')

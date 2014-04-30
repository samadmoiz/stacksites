# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from flaskcities.users.models import User


class RegisterForm(Form):
    username = TextField('Username', validators=[DataRequired("You must enter a username."), 
                         Length(min=2, max=25)])
    email = TextField('Email',
                       validators=[DataRequired("You must enter an email address."), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[DataRequired("You must enter a password."), Length(min=6, max=40)])
    confirm = PasswordField('Verify password',
                            validators=[DataRequired("Please re-type the password entered above."), EqualTo('password', message='Passwords must match.')])
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("That email address has already been registered.")
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("That username has already been taken.")
            return False
        
        self.user = user
        return True 


class LoginForm(Form):
    creds = TextField('Email or Username', 
                       validators=[
                       DataRequired("You forgot to enter your username or email.")
                       ])
    password = PasswordField('Password',
                              validators=[
                              DataRequired("You forgot to enter your password.")
                              ])
    activated = BooleanField("Account Status")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(email=self.creds.data).first()
        if not self.user:
            self.user = User.query.filter_by(username=self.creds.data).first()
            if not self.user:
                self.creds.errors.append("We didn't recognize that email address or username.")
                return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append("Wrong password.")
            return False

        if not self.user.active:
            self.activated.errors.append("Your account has not been activated yet. \
             Please check your inbox for the activation email or resend one.")
            return False

        return True


class ResendConfirmationForm(Form):
    creds = TextField("Email or Username",
                      validators=[DataRequired("You must enter your email address or username.")])

    def __init__(self, *args, **kwargs):
        super(ResendConfirmationForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(ResendConfirmationForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(email=self.creds.data).first()
        if not self.user:
            self.user = User.query.filter_by(username=self.creds.data).first()
            if not self.user:
                self.creds.errors.append("We didn't recognize that email address or username. Please try again.")
                return False

        if self.user.active:
            self.creds.errors.append("This account has already been activated.")
            return False

        return True


class ForgotPasswordForm(Form):
    email = TextField("Email",
                      validators=[DataRequired("You must enter your email address.")])

    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(ForgotPasswordForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(email=self.email.data).first()
        if not self.user:
            self.email.errors.append("We didn't recognize that email address. Please try again.")
            return False
        return True


class ResetPasswordForm(Form):
    password = PasswordField('Password',
                             validators=[DataRequired("You must enter a password."),
                             Length(min=6, max=40)])
    confirm = PasswordField('Verify password',
                            validators=[DataRequired("Please re-type the password entered above."),
                            EqualTo('password', message='Passwords must match.')])

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(ResetPasswordForm, self).validate()
        if not initial_validation:
            return False
        return True
from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Length, Email
from ..models import User
from flask import flash


class ForgotPasswordForm(Form):
    email = StringField("Enter your Email", validators=[
                        DataRequired(), Email()])
    submit = SubmitField("Submit")


class ResetPassword(Form):
    password = PasswordField("New Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_confirm_password(self, field):
        if field.data != self.password.data:
            raise ValidationError("Passwords do not match")


class LoginForm(Form):
    email = StringField("Email", validators=[
                           DataRequired(), Length(1, 100), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
    
    def validate_email(self, field):
        user = User.query.filter_by(email=self.field.data).first()
        if user:
            flash("Email already in use")

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.verify_password(field.data):
            flash("Incorrect username or password", category='error')
            raise ValidationError("Password is incorrect")
        

class AdminLoginForm(LoginForm):

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.verify_password(field.data):
            raise ValidationError("Password is incorrect")
        if user and not user.has_role('admin'):
            raise ValidationError("User doesn't exist")


class SignUpForm(Form):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired()])
    is_provider = BooleanField("Register As A Service Provider")
    submit = SubmitField("Create Account")   

    def validate_confirm_password(self, field):
        if field.data != self.password.data:
            raise ValidationError("Passwords do not match")
        
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already exists")
        

    
        

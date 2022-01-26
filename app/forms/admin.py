from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField, SelectField, FloatField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, Email, InputRequired
from ..models import User




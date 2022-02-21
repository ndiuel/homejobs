from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Regexp, Length
from flask_wtf.file import FileRequired, FileField
from ..models import Service


class PersonalInfoForm(Form):
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    phone_no = StringField("Phone No", validators=[DataRequired()], render_kw={'inputmode': 'tel'})
    image = FileField("Upload Profile Image", validators=[FileRequired()])
    submit = SubmitField("Submit")


class ChangeImageForm(Form):
    image = FileField("Change Profile Image", validators=[FileRequired()])
    submit = SubmitField("Submit")
    

class ChangePersonalInfoForm(Form):
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    phone_no = StringField("Phone No", validators=[DataRequired()], render_kw={'inputmode': 'tel'})
    submit = SubmitField("Submit")
    
    
class AddressForm(Form):
    state = StringField("State Of Residence", validators=[DataRequired()])
    lga = StringField("L.G.A Of Residence", validators=[DataRequired()])
    address = StringField("Current Address") 
    submit = SubmitField("Submit")
    

class VerificationForm(Form):
    identification = FileField("Upload Valid Means Of Identification", validators=[DataRequired()])
    submit = SubmitField("Submit")
    

def AboutForm():
    class _About(Form):
        about = TextAreaField("Write About Yourself", validators=[DataRequired()])
        skills = SelectMultipleField("Select Skills", choices=[(s.id, s.name) for s in Service.query], 
                                     validators=[DataRequired()], render_kw={'size': '1'}, coerce=int)
        submit = SubmitField("Submit")
    return _About
        
    
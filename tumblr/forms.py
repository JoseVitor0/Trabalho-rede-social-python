# Aqui vão estar os formulários do nosso site

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, ValidationError
from wtforms.widgets import TextArea

from tumblr.models import User


class Login(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    btn = SubmitField('Logar')

class Register(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    confirmpassword = PasswordField("confpass", validators=[DataRequired()])
    btn = SubmitField('Logar')


def validate_email(self, email):
    email_user = User.query.filter_by(email=email.data).first()
    if email_user:
        return ValidationError("Email Valido")


class FormCreateNewPost(FlaskForm):
    text = StringField('PostText', widget=TextArea(), validators=[DataRequired()])
    photo = FileField('Photo', validators=[DataRequired()])
    btn = SubmitField('Publish')

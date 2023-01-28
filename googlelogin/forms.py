from flask_wtf import FlaskForm, RecaptchaField
from wtforms import SubmitField


class LoginForm(FlaskForm):
    login = SubmitField('Login with Google')

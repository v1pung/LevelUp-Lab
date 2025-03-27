from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from .model import Users


class RegForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(min=4, max=16)])
    psw = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=16)])
    conf_psw = PasswordField('Confirm password', validators=[DataRequired(), Length(min=4, max=16)])
    submit = SubmitField('Register')

    def validate_login(self, login):
        user = Users.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError('Имя пользователя уже занято')


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(min=4, max=16)])
    psw = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=16)])
    remember = BooleanField('Remember me')
    submit = SubmitField("Login")

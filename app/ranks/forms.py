from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange


class ActivityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=30)])
    reward = FloatField('Reward', validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_reward(self, field):
        if field.data < 1 or field.data > 15:
            raise ValidationError('Награда должна быть от 1 до 15')
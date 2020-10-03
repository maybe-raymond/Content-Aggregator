from flask_wtf import FlaskForm
from blitz.models import User, Followers
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from email_validator import validate_email,  EmailNotValidError


class registration_Form(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    submit=SubmitField("sign up")

    def validate_email(self, email):
        try:
            valid = validate_email(email.data)
            user = User.query.filter_by(Email=email.data).first()
            if user:
                raise ValidationError("You are already registered for the newsletter ")
        except EmailNotValidError as e:
            raise e


class Choice_Form(FlaskForm):
    hearld = BooleanField("Hearld")
    Hmetro = BooleanField("H_metro")
    Dailynews = BooleanField("Dailynews")
    The_Zimbabwean = BooleanField("The_Zimbabwean")
    NewsDay = BooleanField("NewsDay")
    submit = SubmitField("send")

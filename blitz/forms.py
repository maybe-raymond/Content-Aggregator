from flask_wtf import FlaskForm
from blitz.models import User
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError



class registration_Form(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    confirm_password = PasswordField("confirm password", validators=[DataRequired(), EqualTo("password")])
    check = BooleanField("check")
    submit=SubmitField("sign up")

    def email_Validate(self, email):
        user = User.query.filter_by(email =email.data).first()
        if user:
            raise ValidationError("This email aready exists")


    def user_Validate(self, password):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("This Username is aready taken")


class Login_Form(FlaskForm):
    username =   StringField("Username")
    password =  PasswordField("password")
    remember = BooleanField("Remember me")
    submit = SubmitField("Log in ")


class Comment_Form(FlaskForm):
    content = TextAreaField("Comment")
    submit = SubmitField("Post")


class Choice_Form(FlaskForm):
    hearld = BooleanField("Hearld")
    Hmetro = BooleanField("H_metro")
    Dailynews = BooleanField("Dailynews")
    The_Zimbabwean = BooleanField("The_Zimbabwean")
    NewsDay = BooleanField("NewsDay")
    submit = SubmitField("send")

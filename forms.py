from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisterForm(FlaskForm):
    username= StringField(
        "username",
        validators=[DataRequired(message="username requried"), Length(min=3, max=30)]
    )
    email= StringField(
        "email",
        validators=[DataRequired(message="Email requried"), Email(message="Enter vaild email")]
    )
    password= PasswordField(
        "passowrd",
        validators=[DataRequired(message="password requried"), Length(min=6, message="atleast 6 chars")]
    )
    confirm_password= PasswordField(
        "confirm_passowrd",
        validators=[DataRequired(message="please confirm password"),
                    EqualTo("password", message="password must match") ]
    )
    submit= SubmitField(
        "submit"
    )

class LoginForm(FlaskForm):
    email=StringField(
        "email",
        validators=[DataRequired(message="Email requried"),Email()]
    )
    password=PasswordField(
        "password",
        validators=[DataRequired(message="password requried")]
    )
    submit= SubmitField(
        "submit"
    )
class FeedbackForm(FlaskForm):
    title= StringField(
        "title",
        validators=[DataRequired(), Length(max=100)]
    )
    content= StringField(
        "content",
        validators=[DataRequired()]
    )
    submit= SubmitField(
        "submit"
    )
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField, SubmitField
from wtforms.validators import Length, Email, EqualTo, DataRequired


class RegisterForm(FlaskForm):
    username= StringField(
        "username",
        validators=[DataRequired(message="Username Required"), Length(min=3,max=50)]
    )
    email= EmailField(
        "email",
        validators=[DataRequired(message="Email Required"), Email("Enter vaild email")]
    )
    password= PasswordField(
        "password",
        validators=[DataRequired(message="passeord Required"), Length(min=6,message="Atleast 6 chars")]
    )
    confirm_password=PasswordField(
        "confirm_password",
        validators=[DataRequired("please confrim password"),
                    EqualTo("password", message="password must match")]
    )
    submit= SubmitField(
        "submit",
    )
class LoginrForm(FlaskForm):
    
    email= EmailField(
        "email",
        validators=[DataRequired(message="Email Required"), Email("Enter vaild email")]
    )
    password= PasswordField(
        "password",
        validators=[DataRequired(message="passeord Required"), Length(min=6,message="Atleast 6 chars")]
    )
    submit= SubmitField(
        "submit",
    )


class FeedbackForm(FlaskForm):

    title= StringField(
        "title",
        validators=[DataRequired(), Length(max=50)]
    )
    content= TextAreaField(
        "content",
        validators=()
    )
    submit= SubmitField(
        "submit"
    )

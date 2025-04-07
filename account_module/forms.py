from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    username = StringField(
        '',
        validators=[
            DataRequired(),
            Length(max=100)
        ],
        render_kw={
            'class': 'form input',
            'placeholder': 'Username',
        }
    )

    email = StringField(
        '',
        validators=[
            DataRequired(message='Please enter your email'),
            Email(),
            Length(max=200, message='Email cannot be longer than 200 characters')
        ],
        render_kw={
            'class': 'form input',
            "placeholder": "Email"
        })
    password = PasswordField(
        '',
        validators=[
            DataRequired(),
            Length(max=100)
        ],
        render_kw={
            'class': 'form input',
            "placeholder": "Password"
        }
    )
    confirm_password = PasswordField(
        '',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords do not match')
        ],
        render_kw={
            'class': 'form input',
            "placeholder": "Confirm Password"
        }
    )
    submit = SubmitField(
        'sign up',
        render_kw={
            'class': 'form-btn'
        }
    )


class LoginForm(FlaskForm):
    email = StringField(
        '',
        validators=[
            DataRequired(message='Please enter your email'),
            Email(),
            Length(max=200, message='Email cannot be longer than 200 characters')
        ],
        render_kw={
            'class': 'form input',
            "placeholder": "Email"
        })
    password = PasswordField(
        '',
        validators=[
            DataRequired(),
            Length(max=100)
        ],
        render_kw={
            'class': 'form input',
            "placeholder": "Password"
        }
    )

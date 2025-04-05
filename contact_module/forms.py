from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactUsForm(FlaskForm):
    full_name = StringField('Full Name',
                            validators=[
                                DataRequired(message='Please enter your full name'),
                                Length(max=100, message='Full Name cannot be longer than 100 characters')
                            ],
                            render_kw={
                                "class": "form-control",
                                "placeholder": "Full Name"
                            })
    email = StringField('Email',
                        validators=[
                            DataRequired(message='Please enter your email'),
                            Email(),
                            Length(max=200, message='Email cannot be longer than 200 characters')
                        ],
                        render_kw={
                            "class": "form-control",
                            "placeholder": "Email"
                        })
    title = StringField('Subject',
                        validators=[
                            DataRequired(message='Please enter your subject'),
                            Length(max=200, message='Subject cannot be longer than 200 characters')
                        ],
                        render_kw={
                            "class": "form-control",
                            "placeholder": "Subject"
                        })
    message = TextAreaField('Message',
                            validators=[
                                DataRequired(message='Please enter your message'),
                                Length(max=400, message='Message cannot be longer than 400 characters')
                            ],
                            render_kw={
                                "class": "form-control",
                                "placeholder": "Message",
                                "row": "9",
                                "col": "16",
                                'id': 'message',

                            })

    submit = SubmitField('Send Message',
                         render_kw={
                             "class": "btn btn-primary",
                         })

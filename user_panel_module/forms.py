from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class EditProfileForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[
                                 DataRequired(message='Please enter your First Name'),
                                 Length(max=100, message='First Name cannot be longer than 100 characters')
                             ],
                             render_kw={
                                 "id": "first_name",
                                 "placeholder": "First Name"
                             })
    last_name = StringField('Last Name',
                            validators=[
                                DataRequired(message='Please enter your Last Name'),
                                Length(max=200, message='Last Name cannot be longer than 200 characters')
                            ],
                            render_kw={
                                "id": "last_name",
                                "placeholder": "Last Name"
                            })
    avatar = FileField('Change Photo',
                       validators=[
                           FileAllowed(['jpg', 'png', 'jpeg'], 'Image Only'),
                       ],
                       render_kw={
                           "id": "imageUpload",
                           "style": "display: none"
                       })
    address = TextAreaField('Address',
                            validators=[
                                DataRequired(message='Please enter your address'),
                                Length(max=400, message='Message cannot be longer than 400 characters')
                            ],
                            render_kw={
                                "class": "form-control",
                                "placeholder": "Address",
                                "row": 3,
                                'id': 'address',

                            })

    about_user = TextAreaField('About User',
                               validators=[
                                   DataRequired(message='Please enter your address'),
                                   Length(max=400, message='Message cannot be longer than 400 characters')
                               ],
                               render_kw={
                                   "id": "about_user",
                                   "placeholder": "About User",
                                   "row": 5,

                               })


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[
        DataRequired(), Length(max=100)
    ])
    password = PasswordField('New Password', validators=[
        DataRequired()
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords do not match')
    ])
    submit = SubmitField('Change Password',
                         render_kw={
                             'class': 'btn save-btn',
                         })

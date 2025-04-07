import random
import string

from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash

from extensions import db
from .forms import RegisterForm
from .models import User

account_views = Blueprint('account_views', __name__, template_folder='templates')


def get_random_string(length=72):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@account_views.route('register/', methods=['GET', 'POST'])
def register_view():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        if User.query.filter_by(username=username).first():
            form.username.errors.append("Username already exists")
        elif User.query.filter_by(email=email).first():
            form.email.errors.append("Email already exists")
        else:
            new_user = User(
                username=username,
                email=email,
                email_active_code=get_random_string(),
                is_active=False
            )
            new_user.password = generate_password_hash(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please check your email to activate.', 'success')
            return redirect(url_for('account_views.login'))  # یا نام ویو صفحه لاگین
    return render_template('account_module/register_page.html', register_form=form)


@account_views.route('login/', methods=['GET', 'POST'])
def login():
    return render_template('account_module/login_page.html')

import random
import string
from flask import Blueprint, redirect, url_for, render_template, flash, abort, request, session
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from extensions import db
from utils.email_service import send_email
from .forms import RegisterForm, LoginForm, ForgetPasswordForm
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
            send_email(' Activate Your Account ', new_user.email, {'user': new_user}, 'emails/activate_account.html')
            flash('Account created! Please check your email to activate.', 'success')
            # todo: send email active code
            return redirect(url_for('account_views.login_view'))  # یا نام ویو صفحه لاگین
    return render_template('account_module/register_page.html', register_form=form)


@account_views.route('login/', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user_email = form.email.data
        user_password = form.password.data

        user = User.query.filter(User.email.ilike(user_email)).first()
        if user:
            if not user.is_active:
                flash('User is not active', 'warning')
            else:
                correct_password = check_password_hash(user.password, user_password)
                if correct_password:
                    login_user(user)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect email or password', 'danger')
    else:
        flash('Email does not exist', 'danger')
    return render_template('account_module/login_page.html', login_form=form)


@account_views.route('/activate-account/<string:email_active_code>')
def activate_account(email_active_code):
    user = User.query.filter_by(email_active_code=email_active_code).first()
    if user:
        if not user.is_active:
            user.is_active = True
            user.email_active_code = get_random_string()
            db.session.commit()
            flash('Account activated successfully.', 'success')
            return redirect(url_for('account_views.login_view'))
        else:
            flash('Account already activated.', 'info')
            return redirect(url_for('account_views.login'))
    abort(404)


@account_views.route('/forget-pass/', methods=['GET', 'POST'])
def forgot_password_view():
    form = ForgetPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user_email = form.email.data
        user = User.query.filter_by(email=user_email).first()
        if user:
            send_email(
                ' Reset Password',
                user.email,
                {'user': user},
                'emails/forgot_password.html'
            )
            return redirect(url_for('views.home'))
    return render_template('account_module/Forgot_password.html', forget_password_form=form)


@account_views.route('/logout', methods=['GET'])
def logout_view():
    logout_user()
    session.clear()
    return redirect(url_for('account_views.login_view'))

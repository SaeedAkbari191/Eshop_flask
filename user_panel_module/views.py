import os
import uuid
from flask import render_template, Blueprint, redirect, request, url_for, flash
from flask_login import login_required, current_user, logout_user
from werkzeug.utils import secure_filename

from extensions import db
from order_module.models import Order
from .forms import EditProfileForm, ChangePasswordForm

user_views = Blueprint('user_views', __name__, template_folder='templates')


@user_views.route('/user-basket')
@login_required
def user_basket():
    user = current_user
    # فرض می‌کنیم تابع زیر سفارش باز فعلی را می‌دهد:
    order = Order.query.filter_by(user_id=user.id, is_paid=False).first()

    if not order or not order.orderdetail_set:
        return render_template('user_panel_module/user_basket.html', order=None)

    # مجموع قیمت‌ها
    sum_total = order.calculate_total_price()

    # ساخت داده‌های PayPal
    paypal_data = {
        'cmd': '_xclick',
        'business': 'your-paypal-sandbox-email@example.com',
        'amount': sum_total,
        'item_name': f'Order #{order.id}',
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        # 'return': url_for('payment_success_page', _external=True),
        # 'cancel_return': url_for('payment_failure_page', _external=True),
        # 'notify_url': url_for('paypal_ipn', _external=True)
    }

    return render_template('user_panel_module/user_basket.html',
                           order=order,
                           sum=sum_total,
                           paypal_data=paypal_data)


@user_views.route('/')
def user():
    return render_template('user_panel_module/user_panel_dashboard_page.html')


@user_views.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(current_user)

        # پردازش فایل آواتار
        avatar_file = request.files.get('avatar')
        if avatar_file and avatar_file.filename:
            filename = secure_filename(avatar_file.filename)
            avatar_folder = os.path.join('static', 'uploads', 'user')
            os.makedirs(avatar_folder, exist_ok=True)

            avatar_path = os.path.join(avatar_folder, f"user_{current_user.id}_{filename}")
            avatar_file.save(avatar_path)

            # مسیر مناسب برای ذخیره در دیتابیس (استفاده از '/' نه '\')
            current_user.avatar = f"user/user_{current_user.id}_{filename}"

        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('user_views.user'))

    return render_template('user_panel_module/edit_profile_page.html',
                           edit_profile_form=form,
                           current_user=current_user)


@user_views.route('/settings/', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.password.data

        if current_user.check_password(current_password):
            current_user.set_password(new_password)
            db.session.commit()
            logout_user()
            flash('Password changed successfully. Please log in again.', 'success')
            return redirect(url_for('account_views.login_view'))  # آدرس لاگین رو تنظیم کن

        else:
            form.current_password.errors.append('Current password is incorrect.')

    return render_template('user_panel_module/settings.html', change_password_form=form)

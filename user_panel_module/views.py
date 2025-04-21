from flask import render_template, Blueprint, redirect, request, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from .forms import EditProfileForm
from extensions import db

user_views = Blueprint('user_views', __name__, template_folder='templates')


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

    # form = EditProfileForm(obj=current_user)
    # if request.method == 'POST' and form.validate_on_submit():
    #     # به‌روزرسانی اطلاعات متنی
    #     current_user.first_name = form.first_name.data
    #     current_user.last_name = form.last_name.data
    #     current_user.address = form.address.data
    #     current_user.about_user = form.about_user.data
    #
    #     # اگر فایل آپلود شده موجود بود
    #     avatar_file = form.avatar.data
    #     if avatar_file and hasattr(avatar_file, 'filename') and avatar_file.filename != '':
    #         # ساخت نام امن فایل و مسیر ذخیره‌سازی
    #         filename = secure_filename(avatar_file.filename)
    #         avatar_folder = os.path.join('static', 'uploads', 'user')
    #         os.makedirs(avatar_folder, exist_ok=True)
    #
    #         avatar_path = os.path.join(avatar_folder, f"user_{current_user.id}_{filename}")
    #         avatar_file.save(avatar_path)
    #
    #         # ذخیره مسیر نسبی در دیتابیس (مثلاً: user/user_3_john.jpg)
    #         current_user.avatar = os.path.join('user', f"user_{current_user.id}_{filename}")
    #
    #     # ذخیره تغییرات در دیتابیس
    #     db.session.commit()
    #     flash("Profile updated successfully.", "success")
    #     return redirect(url_for('user_views.user'))
    # return render_template('user_panel_module/edit_profile_page.html', edit_profile_form=form, current_user=current_user)

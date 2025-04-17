import os
from flask import current_app, request, abort, render_template
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from wtforms import FileField


class SuperUserOnlyAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_superuser

    def inaccessible_callback(self, name, **kwargs):
        return render_template('account_module/forbidden.html'), 404


class UserAdmin(ModelView):
    form_extra_fields = {
        'avatar': FileField('avatar',
                            validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'],
                                                    'Images only!')])
    }

    # form_excluded_columns = ['email_active_code']

    def on_model_change(self, form, model, is_created):
        file = request.files.get('avatar')
        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            # ذخیره فایل در مسیر static/uploads/
            file.save(upload_path)
            model.avatar = filename

        return super().on_model_change(form, model, is_created)

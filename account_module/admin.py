import os
from flask import current_app, request
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectField, QuerySelectMultipleField
from flask_wtf.file import FileAllowed
from slugify import slugify
from werkzeug.utils import secure_filename
from wtforms import FileField


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

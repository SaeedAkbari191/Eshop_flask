import os
from flask import current_app, request
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from wtforms import FileField
from .models import FooterLink, FooterLinkBox


class SiteSettingAdmin(ModelView):
    form_extra_fields = {
        'site_logo': FileField('',
                               validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'],
                                                       'Images only!')]),
    }

    def on_model_change(self, form, model, is_created):
        file = request.files.get('site_logo')
        if file and file.filename:
            filename = secure_filename(file.filename)
            folder_name = 'Site_settings'
            folder_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_name)
            os.makedirs(folder_path, exist_ok=True)
            upload_path = os.path.join(folder_path, filename)
            # ذخیره فایل در مسیر static/uploads/
            file.save(upload_path)
            # ذخیره مسیر نسبی فایل در دیتابیس
            model.site_logo = f'{folder_name}/{filename}'
        return super().on_model_change(form, model, is_created)


class SliderAdmin(ModelView):
    form_extra_fields = {
        'image': FileField('',
                           validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'],
                                                   'Images only!')]),
    }

    def on_model_change(self, form, model, is_created):
        file = request.files.get('image')
        if file and file.filename:
            filename = secure_filename(file.filename)
            folder_name = 'Slider'
            folder_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_name)
            os.makedirs(folder_path, exist_ok=True)
            upload_path = os.path.join(folder_path, filename)
            # ذخیره فایل در مسیر static/uploads/
            file.save(upload_path)
            # ذخیره مسیر نسبی فایل در دیتابیس
            model.image = f'{folder_name}/{filename}'
        return super().on_model_change(form, model, is_created)


class FooterLinkAdmin(ModelView):
    form_extra_fields = {
        'footer_link_box': QuerySelectField('Footer Link Box', query_factory=lambda: FooterLinkBox.query.all(),
                                            get_label='title'),
    }

class SiteBannerAdmin(ModelView):
    form_extra_fields = {
        'image': FileField('',
                           validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'],
                                                   'Images only!')]),
    }

    def on_model_change(self, form, model, is_created):
        file = request.files.get('image')
        if file and file.filename:
            filename = secure_filename(file.filename)
            folder_name = 'Banner'
            folder_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_name)
            os.makedirs(folder_path, exist_ok=True)
            upload_path = os.path.join(folder_path, filename)
            # ذخیره فایل در مسیر static/uploads/
            file.save(upload_path)
            # ذخیره مسیر نسبی فایل در دیتابیس
            model.image = f'{folder_name}/{filename}'
        return super().on_model_change(form, model, is_created)
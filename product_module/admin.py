import os
from flask import current_app, request
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectField, QuerySelectMultipleField
from flask_wtf.file import FileAllowed
from slugify import slugify
from sqlalchemy.sql.functions import count
from werkzeug.utils import secure_filename
from wtforms import FileField
from .models import ProductCategory, ProductBrand, Product
from extensions import db


class ProductAdmin(ModelView):
    form_extra_fields = {
        'image1': FileField('image1',
                            validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'],
                                                    'Images only!')]),
        'image2': FileField('image2',
                            validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'],
                                                    'Images only!')]),
        'category': QuerySelectMultipleField('Category', query_factory=lambda: ProductCategory.query.all(),
                                             get_label='title'),
        'brand': QuerySelectField('Brand', query_factory=lambda: ProductBrand.query.all(), get_label='title'),
    }

    form_excluded_columns = ['slug']

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.slug = slugify(model.title)
        else:
            old_product = Product.query.get(model.id)
            if old_product:
                print('ss')
                model.slug = slugify(model.title)

        file1 = request.files.get('image1')
        if file1 and file1.filename:
            filename1 = secure_filename(file1.filename)
            upload_path1 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename1)
            # ذخیره فایل در مسیر static/uploads/
            file1.save(upload_path1)
            # ذخیره مسیر نسبی فایل در دیتابیس
            model.image1 = filename1

        file2 = request.files.get('image2')
        if file2 and file2.filename:
            filename2 = secure_filename(file2.filename)
            upload_path2 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename2)
            # ذخیره فایل در مسیر static/uploads/
            file2.save(upload_path2)
            # ذخیره مسیر نسبی فایل در دیتابیس
            model.image2 = filename2
        return super().on_model_change(form, model, is_created)

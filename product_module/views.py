import os
from io import BytesIO

from PIL import Image, ImageOps
from flask import Blueprint, request, render_template, session, current_app, send_file, abort
from sqlalchemy.orm import subqueryload
from unicodedata import category

from .models import Product, ProductCategory

p_views = Blueprint('p_views', __name__, template_folder='templates')


@p_views.route('/uploads/<path:filename>')
def get_image(filename):
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    full_path = os.path.join(upload_folder, filename)

    if not os.path.exists(full_path):
        abort(404)

    try:
        img = Image.open(full_path)
        img = ImageOps.fit(img, (360, 360), Image.Resampling.LANCZOS)

        # ذخیره در حافظه موقتی (نه روی دیسک)
        img_io = BytesIO()
        img_format = img.format if img.format else 'JPEG'
        img.save(img_io, img_format)
        img_io.seek(0)

        return send_file(img_io, mimetype=f'image/{img_format.lower()}')

    except Exception as e:
        print(f"Error processing image: {e}")
        abort(500)


@p_views.route('/')
@p_views.route('/cat/<string:category>')
def product_list(category=None):
    page = request.args.get('page', 1, type=int)
    per_page = 1

    query = Product.query.order_by(Product.price.desc())

    if category:
        query = query.join(Product.category).filter(ProductCategory.url_title.ilike(category))

    products = query.paginate(page=page, per_page=per_page, error_out=False)

    # فقط وقتی این ویو رندر میشه، دسته‌بندی‌ها هم پاس داده میشن
    main_categories = ProductCategory.query.options(subqueryload(ProductCategory.parent)).filter_by(is_active=True,
                                                                                                    parent_id=None).all()

    return render_template('product_module/product_list.html',
                           products=products,
                           main_categories=main_categories,
                           selected_category=category)


#


@p_views.route("<string:slug>")
def product_detail(slug):
    products = Product.query.filter_by(slug=slug).first_or_404()

    favorite_product_id = session.get('ProductFavorite')
    is_favorite = favorite_product_id == str(products.id)

    return render_template('product_module/product_details.html', products=products,
                           )

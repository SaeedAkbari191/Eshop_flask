import os
from flask import Blueprint, request, render_template, session, send_from_directory, current_app
from .models import Product
from site_module.models import SiteSetting
from flask_sqlalchemy import pagination

p_views = Blueprint('p_views', __name__, template_folder='templates')


@p_views.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(os.path.join(current_app.root_path, 'static', 'uploads'), filename)


@p_views.route('/')
def products():
    page = request.args.get('page', 1, type=int)  # دریافت شماره صفحه
    per_page = 1  # تعداد محصولات در هر صفحه

    # صفحه‌بندی داده‌ها
    products = Product.query.order_by(Product.price.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('product_module/product_list.html', products=products)


# @view.route('product-details/')
# def product_details():
#     return render_template('product_module/product_details.html')

@p_views.route("<string:slug>")
def product_detail(slug):
    products = Product.query.filter_by(slug=slug).first_or_404()
    site_setting = SiteSetting.query.filter_by(is_main_setting=True).first_or_404()

    favorite_product_id = session.get('ProductFavorite')
    is_favorite = favorite_product_id == str(products.id)

    return render_template('product_module/product_details.html', products=products, site_setting=site_setting,
                           )

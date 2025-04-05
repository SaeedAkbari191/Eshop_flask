import os

from flask import Blueprint, render_template, session, send_from_directory, current_app
from .models import Product

p_views = Blueprint('p_views', __name__, template_folder='templates')


@p_views.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(os.path.join(current_app.root_path,'static','uploads'), filename)


@p_views.route('/')
def products():
    products = Product.query.filter(Product.is_active == True).all()
    return render_template('product_module/product_list.html', products=products)


# @view.route('product-details/')
# def product_details():
#     return render_template('product_module/product_details.html')

@p_views.route("<string:slug>")
def product_detail(slug):
    products = Product.query.filter_by(slug=slug).first_or_404()

    favorite_product_id = session.get('ProductFavorite')
    is_favorite = favorite_product_id == str(products.id)

    return render_template('product_module/product_details.html', products=products, )

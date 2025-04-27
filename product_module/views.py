import os
from io import BytesIO
from flask_login import current_user
from PIL import Image, ImageOps
from flask import Blueprint, request, render_template, session, current_app, send_file, abort
from sqlalchemy import func
from sqlalchemy.orm import subqueryload
from extensions import db
from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery
from utils.http_service import get_client_ip

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
@p_views.route('/brand/<string:brand>')
def product_list(category=None, brand=None):
    page = request.args.get('page', 1, type=int)
    per_page = 1

    query = Product.query.order_by(Product.price.desc())

    if category:
        query = query.join(Product.category).filter(ProductCategory.url_title.ilike(category))

    if brand:
        query = query.join(Product.brand).filter(ProductBrand.url_title.ilike(brand))

    products = query.paginate(page=page, per_page=per_page, error_out=False)

    # فقط وقتی این ویو رندر میشه، دسته‌بندی‌ها هم پاس داده میشن
    main_categories = ProductCategory.query.options(subqueryload(ProductCategory.parent)).filter_by(is_active=True,
                                                                                                    parent_id=None).all()

    brands = db.session.query(ProductBrand, func.count(Product.id).label('products_count')).join(Product,
                                                                                                 isouter=True).filter(
        ProductBrand.is_active == True
    ).group_by(ProductBrand.id).all()

    return render_template('product_module/product_list.html',
                           products=products,
                           main_categories=main_categories,
                           brands=brands)


#


@p_views.route("<string:slug>")
def product_detail(slug):
    product = Product.query.filter_by(slug=slug).first_or_404()

    # بررسی اینکه آیا این محصول در علاقه‌مندی‌ها هست یا نه
    favorite_product_id = session.get('ProductFavorite')
    is_favorite = str(product.id) == str(favorite_product_id)

    product_galleries = ProductGallery.query.filter_by(product_id=product.id).limit(3).all()
    related_product = Product.query.filter_by(brand_id=product.brand_id).filter(Product.id != product.id).limit(
        12).all()

    # گرفتن آی‌پی کاربر
    user_ip = get_client_ip(request)
    print(user_ip)
    user_id = current_user.id if current_user.is_authenticated else None

    # بررسی اینکه آیا قبلاً این آی‌پی این محصول را دیده یا نه
    visited = ProductVisit.query.filter(
        func.lower(ProductVisit.ip) == func.lower(user_ip),
        ProductVisit.product_id == product.id
    ).first()

    if not visited:
        new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=product.id)
        db.session.add(new_visit)
        db.session.commit()

    return render_template(
        'product_module/product_details.html',
        products=product,
        is_favorite=is_favorite,
        products_galleries=product_galleries,
        related_products=related_product,
    )

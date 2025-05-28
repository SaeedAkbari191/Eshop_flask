from flask import Blueprint, render_template
from flask import Blueprint, render_template
from sqlalchemy.orm import subqueryload
from extensions import db
from sqlalchemy import func
from product_module.models import ProductCategory, Product, ProductVisit
from site_module.models import Slider, SiteSetting, SiteBanner, SiteBannerPosition
from order_module.models import Order, OrderDetail

views = Blueprint('views', __name__, template_folder='templates')


@views.route('/', methods=['GET', 'POST'])
def home():
    sliders = Slider.query.filter_by(is_active=True).all()
    banners = SiteBanner.query.filter_by(is_active=True, position=SiteBannerPosition.home).all()
    products = Product.query.filter_by(is_active=True, is_deleted=False).order_by(Product.id.desc()).limit(5).all()
    main_categories = ProductCategory.query.options(subqueryload(ProductCategory.parent)).filter_by(is_active=True,
                                                                                                    parent_id=None).all()
    most_visit_product = (
        db.session.query(Product, func.count(ProductVisit.id).label('visit_count'))
        .join(ProductVisit)
        .filter(Product.is_active == True, Product.is_deleted == False)
        .group_by(Product)
        .order_by(func.count(ProductVisit.id).desc())
        .limit(12)
        .all()
    )
    most_visit_product = [item[0] for item in most_visit_product]

    most_bought_products = (
        Product.query
        .join(OrderDetail, Product.id == OrderDetail.product_id)
        .join(Order, OrderDetail.order_id == Order.id)
        .filter(Order.is_paid == True)
        .with_entities(Product, func.sum(OrderDetail.count).label('order_count'))
        .group_by(Product.id)
        .order_by(func.sum(OrderDetail.count).desc())
        .limit(12)
        .all()
    )

    context = {
        'sliders': sliders,
        'main_categories': main_categories,
        'top_banners': banners[:3],
        'middle_banners': banners[3:5],
        'bottom_banners': banners[5:8],
        'products': products,
        'most_visit_product': most_visit_product,
        'most_bought_product': most_bought_products,
    }
    return render_template('home_module/index_page.html', **context)


@views.route('/about-us')
def about_us_page():
    site_setting = SiteSetting.query.filter_by(is_main_setting=True).first()
    return render_template('home_module/about_us.html', site_setting=site_setting)

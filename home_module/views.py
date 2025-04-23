from flask import Blueprint, render_template
from flask import Blueprint, render_template
from sqlalchemy.orm import subqueryload

from product_module.models import ProductCategory, Product
from site_module.models import Slider, SiteSetting, SiteBanner, SiteBannerPosition

views = Blueprint('views', __name__, template_folder='templates')


@views.route('/', methods=['GET', 'POST'])
def home():
    sliders = Slider.query.filter_by(is_active=True).all()
    banners = SiteBanner.query.filter_by(is_active=True, position=SiteBannerPosition.home).all()
    products = Product.query.filter_by(is_active=True).limit(7).all()
    main_categories = ProductCategory.query.options(subqueryload(ProductCategory.parent)).filter_by(is_active=True,
                                                                                                    parent_id=None).all()

    context = {
        'sliders': sliders,
        'main_categories': main_categories,
        'top_banners': banners[:3],
        'middle_banners': banners[3:5],
        'bottom_banners': banners[5:8],
        'products': products,
    }
    return render_template('home_module/index_page.html', **context)


@views.route('/about-us')
def about_us_page():
    site_setting = SiteSetting.query.filter_by(is_main_setting=True).first()
    return render_template('home_module/about_us.html', site_setting=site_setting)

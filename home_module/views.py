from flask import Blueprint, render_template
from flask import Blueprint, render_template
from sqlalchemy.orm import subqueryload

from product_module.models import ProductCategory
from site_module.models import Slider, SiteSetting

views = Blueprint('views', __name__, template_folder='templates')


@views.route('/', methods=['GET', 'POST'])
def home():
    slider = Slider.query.filter_by(is_active=True)
    main_categories = ProductCategory.query.options(subqueryload(ProductCategory.parent)).filter_by(is_active=True,
                                                                                                    parent_id=None).all()
    return render_template('home_module/index_page.html', sliders=slider, main_categories=main_categories)


@views.route('/about-us')
def about_us_page():
    site_setting = SiteSetting.query.filter_by(is_main_setting=True).first()
    return render_template('home_module/about_us.html', site_setting=site_setting)

import jinja2
from flask import Blueprint, render_template
from site_module.models import Slider, SiteSetting

views = Blueprint('views', __name__, template_folder='templates')


@views.route('/', methods=['GET', 'POST'])
def home():
    slider = Slider.query.filter_by(is_active=True)
    return render_template('home_module/index_page.html', sliders=slider, )


@views.route('/about-us')
def about_us_page():
    site_setting = SiteSetting.query.filter_by(is_main_setting=True).first()
    return render_template('home_module/about_us.html', site_setting=site_setting)

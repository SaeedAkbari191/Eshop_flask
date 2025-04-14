import jinja2
from flask import Blueprint, render_template
from site_module.models import Slider, SiteSetting

views = Blueprint('views', __name__, template_folder='templates/home_module')


@views.route('/', methods=['GET', 'POST'])
def home():
    slider = Slider.query.filter_by(is_active=True)
    return render_template('index_page.html', sliders=slider, )

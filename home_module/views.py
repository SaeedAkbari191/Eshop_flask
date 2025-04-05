import jinja2
from flask import Blueprint, render_template

views = Blueprint('views', __name__, template_folder='templates/home_module')


@views.route('/', methods=['GET', 'POST'])
def home():
    header_context = {'title': 'header'}
    footer_context = {'title': 'footer'}
    return render_template('index_page.html', header_context=header_context, footer_context=footer_context)

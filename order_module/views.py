from flask import Blueprint

order_views = Blueprint('order_views', __name__, template_folder='templates')


@order_views.route('/')
def index():
    return 'dd'

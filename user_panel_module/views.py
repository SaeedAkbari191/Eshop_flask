from flask import render_template, Blueprint

user_views = Blueprint('user_views', __name__, template_folder='templates')


@user_views.route('/')
def user():
    return render_template('user_panel_module/user_panel_dashboard_page.html')

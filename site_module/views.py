import os

from flask import Blueprint, send_from_directory, current_app

setting_views = Blueprint('setting_views', __name__, template_folder='templates')


@setting_views.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(os.path.join(current_app.root_path, 'static', 'uploads'), filename)
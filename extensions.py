from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_thumbnails import Thumbnail
from account_module.admin import SuperUserOnlyAdminView

thumb = Thumbnail()

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

login_manager = LoginManager()

from account_module.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


admin = Admin(index_view=SuperUserOnlyAdminView(), template_mode='bootstrap4')

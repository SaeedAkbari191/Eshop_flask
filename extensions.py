from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

from account_module.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


admin = Admin(template_mode='bootstrap4')

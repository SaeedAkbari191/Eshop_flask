import os

from flask import Flask
from flask_admin.contrib.sqla import ModelView

from extensions import db, migrate, admin

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hbnwdvbn ajnbsjn ahe'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/flaskecommerceproject'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)

    from product_module.models import Product, ProductCategory, ProductBrand, ProductTag
    from product_module.admin import ProductAdmin
    from contact_module.models import ContactUS

    from account_module.models import User
    from account_module.admin import UserAdmin


    admin.add_view(ProductAdmin(Product, db.session))
    admin.add_view(ModelView(ProductCategory, db.session))
    admin.add_view(ModelView(ProductBrand, db.session))
    admin.add_view(ModelView(ProductTag, db.session))
    admin.add_view(ModelView(ContactUS, db.session))
    admin.add_view(UserAdmin(User, db.session))
    # admin.add_view(ModelView(product_category_association, db.session))

    from home_module.views import views
    from product_module.views import p_views
    from contact_module.views import contact_views

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(p_views, url_prefix='/products')
    app.register_blueprint(contact_views, url_prefix='/contact-us')

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    return app

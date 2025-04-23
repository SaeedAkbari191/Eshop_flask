import os

from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from extensions import db, migrate, admin, login_manager, mail, thumb

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hbnwdvbn ajnbsjn ahe'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/flaskecommerceproject'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # EMAIL CONFIG
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_DEFAULT_SENDER'] = 'm.saeedakbari559728@gmail.com'
    app.config['MAIL_USERNAME'] = 'm.saeedakbari559728@gmail.com'
    app.config['MAIL_PASSWORD'] = 'cpnw wexj hicw flqy'

    app.config['THUMBNAIL_MEDIA_ROOT'] = 'static/uploads'
    app.config['THUMBNAIL_MEDIA_THUMBNAIL_ROOT'] = 'static/uploads/thumbnails'

    @app.context_processor
    def inject_site_settings():
        site_setting = SiteSetting.query.filter_by(is_main_setting=True).first()
        footer_link_boxes = FooterLinkBox.query.all()

        return dict(site_setting=site_setting, footer_link_boxes=footer_link_boxes, current_user=current_user)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    thumb.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'account_views.login_view'
    login_manager.login_message_category = 'info'
    admin.init_app(app)

    from product_module.models import Product, ProductCategory, ProductBrand, ProductTag
    from product_module.admin import ProductAdmin, ProductCategoryAdmin
    from contact_module.models import ContactUS

    from account_module.models import User
    from account_module.admin import UserAdmin

    from site_module.models import SiteSetting, Slider, FooterLink, FooterLinkBox,SiteBanner
    from site_module.admin import SiteSettingAdmin, SliderAdmin, FooterLinkAdmin

    admin.add_view(ProductAdmin(Product, db.session))
    admin.add_view(ProductCategoryAdmin(ProductCategory, db.session))
    admin.add_view(ModelView(ProductBrand, db.session))
    admin.add_view(ModelView(ProductTag, db.session))
    admin.add_view(ModelView(ContactUS, db.session))
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(SiteSettingAdmin(SiteSetting, db.session))
    admin.add_view(SliderAdmin(Slider, db.session))
    admin.add_view(FooterLinkAdmin(FooterLink, db.session))
    admin.add_view(ModelView(FooterLinkBox, db.session))
    admin.add_view(ModelView(SiteBanner, db.session))
    # admin.add_view(ModelView(product_category_association, db.session))

    from home_module.views import views
    from product_module.views import p_views
    from contact_module.views import contact_views
    from account_module.views import account_views
    from site_module.views import setting_views
    from user_panel_module.views import user_views

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(p_views, url_prefix='/products')
    app.register_blueprint(contact_views, url_prefix='/contact-us')
    app.register_blueprint(account_views, url_prefix='/')
    app.register_blueprint(setting_views, url_prefix='/')
    app.register_blueprint(user_views, url_prefix='/user')

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    return app

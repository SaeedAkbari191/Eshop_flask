from extensions import db
from sqlalchemy import Enum
import enum


class SiteSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), nullable=False)
    url_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=True)
    fax = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    copy_right = db.Column(db.String(100), nullable=False)
    about_us_text = db.Column(db.Text, nullable=False)
    site_logo = db.Column(db.String(200), nullable=False)
    is_main_setting = db.Column(db.Boolean, default=False)

    def __str__(self):
        return self.site_name


class FooterLinkBox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.title


class FooterLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(400), nullable=False)
    footer_link_box_id = db.Column(db.Integer, db.ForeignKey('footer_link_box.id'), nullable=False)
    footer_link_box = db.relationship('FooterLinkBox', backref=db.backref('footer_links', lazy=True))

    def __str__(self):
        return self.title


class Slider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(400), nullable=False)
    url_title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    image = db.Column(db.String(200), nullable=False)

    def __str__(self):
        return self.title


class SiteBannerPosition(enum.Enum):
    home = 'home'
    product_list = 'product_list'
    product_details = 'product_details'


class SiteBanner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url_title = db.Column(db.String(400), nullable=False)
    image = db.Column(db.String(255), nullable=False)  # برای مسیر عکس
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    position = db.Column(db.Enum(SiteBannerPosition), nullable=False)

    def __repr__(self):
        return f'<SiteBanner {self.title}>'

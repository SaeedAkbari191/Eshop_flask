from flask import url_for
from slugify import slugify
from extensions import db

# جدول واسط برای رابطه Many-to-Many بین Product و ProductCategory
product_category_association = db.Table(
    'product_category_association',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('product_category.id'), primary_key=True)
)


class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False, index=True)
    url_title = db.Column(db.String(300), nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True)
    is_deleted = db.Column(db.Boolean, default=False)

    def __str__(self):
        return f'({self.title} , {self.url_title})'


class ProductBrand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False, index=True)
    url_title = db.Column(db.String(300), nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True)

    def __str__(self):
        return self.title


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    category = db.relationship('ProductCategory', secondary=product_category_association, backref='products')
    image1 = db.Column(db.String(300), nullable=True)
    image2 = db.Column(db.String(300), nullable=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('product_brand.id'), nullable=True)
    brand = db.relationship('ProductBrand', backref='products')
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    old_price = db.Column(db.Integer, nullable=False)
    short_description = db.Column(db.String(300), nullable=True, )
    description = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    is_deleted = db.Column(db.Boolean, default=False)

    def __str__(self):
        return f"{self.title} ({self.price})"

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        db.session.add(self)
        db.session.commit()

    def get_absolute_url(self):
        return f"/products/{self.slug}"


class ProductTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(50), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref='product_tags')

    def str(self):
        return self.caption

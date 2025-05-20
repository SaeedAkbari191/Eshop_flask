from flask_sqlalchemy import SQLAlchemy
from datetime import date
from extensions import db
from account_module.models import User
from product_module.models import Product


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_paid = db.Column(db.Boolean, default=False)
    payment_date = db.Column(db.Date, nullable=True)

    user = db.relationship('User', backref=db.backref('order', lazy=True))

    orderdetail_set = db.relationship('OrderDetail', backref='order', lazy='dynamic')

    def __repr__(self):
        return f'<Order by {self.user.username}>'

    def calculate_total_price(self):
        total_amount = 0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_amount += (order_detail.final_price or 0) * order_detail.count
        else:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.product.price * order_detail.count
        return total_amount


class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    final_price = db.Column(db.Integer, nullable=True)
    count = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product')

    def __repr__(self):
        return f'<OrderDetail for Order {self.order_id}>'

    def total_price(self):
        if self.final_price is not None:
            return self.count * self.final_price
        return self.count * self.product.price

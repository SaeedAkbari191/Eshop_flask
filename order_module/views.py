from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from extensions import db
from product_module.models import Product
from .models import Order, OrderDetail

order_views = Blueprint('order_views', __name__, template_folder='templates')


@order_views.route('/add-to-order', methods=['GET', 'POST'])
def add_to_order():
    try:
        product_id = int(request.args.get('product_id', 0))
        count = int(request.args.get('count', 0))
    except (TypeError, ValueError):
        return jsonify({
            'status': 'Invalid Data',
            'text': 'Product ID and count must be integers.',
            'icon': 'warning',
            'confirmButtonText': 'Ok!'
        })

    if count < 1:
        return jsonify({
            'status': 'Invalid Count.',
            'text': 'Invalid Count.',
            'icon': 'warning',
            'confirmButtonText': 'Ok!'
        })

    if current_user.is_authenticated:
        product = Product.query.filter_by(id=product_id, is_active=True, is_deleted=False).first()
        if product is not None:
            current_order = Order.query.filter_by(user_id=current_user.id, is_paid=False).first()
            if not current_order:
                current_order = Order(user_id=current_user.id)
                db.session.add(current_order)
                db.session.commit()

            current_order_details = OrderDetail.query.filter_by(order_id=current_order.id,
                                                                product_id=product_id).first()
            if current_order_details is not None:
                current_order_details.count += count
                db.session.commit()
            else:
                new_details = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                db.session.add(new_details)
                db.session.commit()

            return jsonify({
                'status': 'SUCCESS',
                'text': 'The Product has been successfully added to your shopping cart',
                'icon': 'success',
                'confirmButtonText': 'Ok!'
            })
        else:
            return jsonify({
                'status': 'Not Found',
                'text': 'Product Not Found',
                'icon': 'error',
                'confirmButtonText': 'Ok!'
            })
    else:
        return jsonify({
            'status': 'Not_Authorized',
            'text': 'Please Log in to add the product to your shopping cart',
            'confirmButtonText': 'ok',
            'icon': 'error'
        })

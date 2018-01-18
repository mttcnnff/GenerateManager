from flask_restful import Resource, abort
from . import api
from flask import request
from ..models import OrderModel
from .. import db

@api.route('/order')
class Order(Resource):
    def order_does_not_exist(self, todo_id):
        abort(404, message="Order {} does not exist".format(todo_id))

    def post(self):
        print(">>> Order placed")
        order = OrderModel();
        order.company = request.form['hostname']
        order.product = request.form['product']
        order.price = request.form['price'][1:]
        order.qty = request.form['qty']
        order.team = request.form['team']
        order.member = request.form['member']
        # print(" >>> HOSTNAME: " + request.form['hostname'])
        # print(" >>> PRODUCT: " + request.form['product'])
        # print(" >>> PRICE: " + request.form['price'])
        # print(" >>> QTY: " + request.form['qty'])
        # print("\n\n")
        db.session.add(order)
        return 'Successfully placed order.'

    def get(self):
        return 'Successfully placed order.'
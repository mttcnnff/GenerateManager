from flask_restful import Resource, abort
from . import api
from flask import request
from ..models import MemberModel
from .. import db

@api.route('/order', methods = ['POST'])
class Order(Resource):
    def order_does_not_exist(self, todo_id):
        abort(404, message="Order {} does not exist".format(todo_id))

    def post(self, id):
        print(">>> hello")
        print(">>> " + request.method)
        if request.method == "POST":
            url = request.form['hostname']
            print(" >>> HOSTNAME: " + request.form['hostname'])
            print(" >>> PRODUCT: " + request.form['product'])
            print(" >>> PRICE: " + request.form['price'])
            print(" >>> QTY: " + request.form['qty'])
            print("\n\n")

        return 'Successfully placed order.'
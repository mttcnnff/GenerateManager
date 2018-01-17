from flask_restful import Resource
from . import api

@api.route('/todos/<int:id>')
class TodoItem(Resource):
    def get(self, id):
        return {'task': 'Say "Hello, World!"'}
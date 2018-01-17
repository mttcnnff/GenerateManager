from flask import Blueprint
from flask_restful import Resource, Api
from .. import api
import types
from ..decorators import api_route

api_bp = Blueprint('api', __name__)

api = Api(api_bp)                               # Create API object
api.route = types.MethodType(api_route, api)    # Add decorator

from . import routes, Members, orders

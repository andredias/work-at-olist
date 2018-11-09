from flask import Blueprint
from flask_restful import Api

api = Blueprint('api', __name__)
api_rest = Api(api)

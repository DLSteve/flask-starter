from flask import Blueprint
from flask_restplus import Api


api_v1_blueprint = Blueprint('api_v1', __name__, template_folder='templates')
api_v1 = Api(api_v1_blueprint, version='1.0', title='flask-starter API', doc='/doc')

from . import auth, doc_view, resets

from flask_restplus import Resource
from flask import jsonify, current_app
from flask_login import login_required, current_user
from . import api_v1
from .models.token import token, Token

auth = api_v1.namespace('auth', description='Auth API')


@api_v1.app.before_request
@login_required
def before_request():
    if not current_app.config.get('AUTH_DISABLED'):
        if current_user.is_anonymous:
            return jsonify({401: 'Unauthorized'})


@auth.route('/token')
@auth.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'User not found',
    500: 'Internal Server Error'
})
class APIToken(Resource):

    @auth.doc('get_token')
    @auth.marshal_with(token)
    def get(self):
        """Gets an API Token"""
        if current_user and not current_user.is_anonymous:
            user = current_user
            tok = Token(user, 3600)
            return tok
        return jsonify({404: 'User not found'})

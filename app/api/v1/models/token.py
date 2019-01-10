from flask_restplus import fields
from .. import api_v1


token = api_v1.model('Token', {
    'token': fields.String(description='API Token'),
    'expiration': fields.Integer(description='Token expiration time'),
})


class Token(object):

    def __init__(self, auth_user, exp):
        self.token = auth_user.generate_auth_token(exp)
        self.expiration = exp

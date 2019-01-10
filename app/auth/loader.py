import base64

from app import login_manager
from app.models import User, Settings


@login_manager.request_loader
def load_user_from_request(req):
    if req.path.startswith('/api/v1/auth/token'):
        api_key = req.headers.get('Authorization')
        if api_key:
            api_key = api_key.replace('Basic ', '', 1)
            try:
                api_key = base64.b64decode(api_key)
            except TypeError:
                pass
            api_key = api_key.decode("utf-8")
            api_key = api_key.replace(':', ' ', 1).split(' ')
            username = api_key[0]
            password = api_key[1]

            # TODO: Implement token authorization

    if req.path.startswith('/api'):
        api_key = None
        api_key_arg = req.args.get('api-key')
        api_key_header = req.headers.get('Authorization')

        if api_key_arg:
            api_key = api_key_arg

        if api_key_header:
            api_key = api_key_header.replace('IAM api-key=', '', 1)

        if api_key:
            api_secret1 = Settings.query.get('api_secret1')
            api_secret2 = Settings.query.get('api_secret2')
            if api_secret1 or api_secret2:
                user = User.verify_api_key(api_secret1.value, api_key)
                if not user:
                    user = User.verify_api_key(api_secret2.value, api_key)
                return user

        api_token = req.args.get('api-token')
        if api_token:
            user = User.verify_auth_token(api_token)
            return user
    return None

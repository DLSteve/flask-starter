import json
import uuid
import requests

from datetime import datetime
from urllib.parse import quote_plus
from app import login_manager, oauth, db
from app.models import User
from flask import render_template, request, session, abort, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required
from jose import jws
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired

from . import auth

TENANT_ID = ''
CORE_URL = ''

# Dummy object that get initialized at runtime.
AAD = None


@auth.before_app_first_request
def init_oauth():
    # General
    global TENANT_ID
    TENANT_ID = current_app.config.get('AZURE_TENANT_ID')

    global CORE_URL
    CORE_URL = 'https://login.microsoftonline.com/' + TENANT_ID

    # OpenID Connect
    scopes = 'openid profile'
    token_url = CORE_URL + '/oauth2/token'
    authorize_url = CORE_URL + '/oauth2/authorize'

    global AAD
    AAD = oauth.remote_app(
        'microsoft',
        consumer_key=current_app.config.get('AZURE_CLIENT_ID'),
        consumer_secret=current_app.config.get('AZURE_CLIENT_SECRET'),
        request_token_params={'scope': scopes},  # Use "{'scope': SCOPES}, 'prompt': 'login'}" for restricted apps.
        base_url='http://ignore',  # We won't need this.
        request_token_url=None,
        access_token_method='POST',
        access_token_url=token_url,
        authorize_url=authorize_url
    )


@auth.route('/login')
def login():
    if current_app.config.get('AUTH_TYPE') == 'OpenID':
        return redirect(url_for('auth.sso_openid', next=request.args.get('next')))
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    if current_app.config.get('AUTH_TYPE') == 'OpenID':
        return redirect(url_for('auth.logout_openid'))

    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    return redirect(url_for('auth.logged_out'))


@auth.route('/sso/openid', methods=['POST', 'GET'])
def sso_openid():
    guid = uuid.uuid4()
    session['state'] = guid
    s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'],
                                        expires_in=300)
    token = s.dumps({'guid': str(guid), 'next': request.args.get('next')}).decode('ascii')
    return AAD.authorize(callback=url_for('auth.sso_openid_authorized', _external=True,
                         _scheme=current_app.config.get('PREFERRED_URL_SCHEME')), state=token)


@auth.route('/sso/openid/authorized')
def sso_openid_authorized():
    response = AAD.authorized_response()
    state = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
    try:
        data = state.loads(request.args['state'])
    except SignatureExpired:
        return None
    except BadSignature:
        return None

    if not response:
        abort(403)
    if str(session['state']) != str(data['guid']):
        abort(403)
    access_token = response['id_token']

    keys_url = CORE_URL + '/discovery/keys'
    keys_raw = requests.get(keys_url).text
    keys = json.loads(keys_raw)

    user_data = json.loads(jws.verify(access_token, keys, algorithms=['RS256']))

    usr = User.query.filter_by(username=user_data.get('unique_name')).first()

    if usr:
        usr.last_login = datetime.utcnow()
        usr.set_user_id()
        db.session.add(usr)
        db.session.commit()
    else:
        usr = User(
            username=user_data.get('unique_name'),
            first_name=user_data.get('given_name'),
            last_name=user_data.get('family_name'),
            last_login=datetime.utcnow()
        )
        usr.set_user_id()
        db.session.add(usr)
        db.session.commit()

    login_user(usr)

    return redirect(data.get('next') or url_for('main.index'))


@auth.route('/logout/openid')
@login_required
def logout_openid():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    return redirect('https://login.microsoftonline.com/' + TENANT_ID +
                    '/oauth2/logout?post_logout_redirect_uri=' +
                    quote_plus(url_for('auth.logged_out', _external=True,
                                       _scheme=current_app.config.get('PREFERRED_URL_SCHEME'))))


@auth.route('/slo/openid')
def slo_openid():
    """This function receives a GET request from the IdP for logging the user out.
    """
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    return 'success', 200


@auth.route('/logged/in')
def logged_in():
    return render_template('auth/logged_in.html')


@auth.route('/logged/out')
def logged_out():
    return render_template('auth/logged_out.html')


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if user:
        return user
    return None

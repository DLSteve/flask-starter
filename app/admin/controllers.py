from flask import render_template, current_app, abort
from flask_login import login_required, current_user
from app import db
from app.auth_utilities import admin_required, generate_password
from app.models import Settings, User
from sqlalchemy.exc import IntegrityError
from . import admin


@admin.before_request
@login_required
@admin_required
def before_request():
    if not current_app.config.get('AUTH_DISABLED'):
        if current_user.is_anonymous:
            abort(401)


@admin.route('/settings')
def app_settings():
    api_secret1 = Settings.query.get('api_secret1')
    api_secret2 = Settings.query.get('api_secret2')
    if not api_secret1:
        api_secret1 = Settings(
            id='api_secret1',
            value=generate_password(30)
        )
        db.session.add(api_secret1)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise
    if not api_secret2:
        api_secret2 = Settings(
            id='api_secret2',
            value=generate_password(30)
        )
        db.session.add(api_secret2)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise

    key1 = User.generate_api_key(api_secret1.value)
    key2 = User.generate_api_key(api_secret2.value)

    return render_template('admin/pages/admin_app_settings.html', title='App Settings', key1=key1, key2=key2)


@admin.route('/settings/key/reset/<string:key_num>')
def settings_key_reset(key_num):
    key = ''
    key_id = ''
    if key_num == '1':
        key = reset_api_key('api_secret1')
        key_id = 'key1'
    elif key_num == '2':
        key = reset_api_key('api_secret2')
        key_id = 'key2'
    else:
        abort(404)

    return render_template('admin/partials/admin_settings_key_reset.html', key=key, key_id=key_id)


def reset_api_key(key_name):
    api_secret = Settings.query.get(key_name)
    if not api_secret:
        api_secret = Settings(
            id=key_name,
            value=generate_password(30)
        )
        db.session.add(api_secret)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise
    else:
        api_secret.value = generate_password(30)
        db.session.add(api_secret)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise
    return User.generate_api_key(api_secret.value)

import os

from app.config import config, SecretsConfig
from app.util import current_year
from app.auth_utilities import check_access
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
from flask_azure_storage import FlaskAzureStorage
from flask_wtf.csrf import CSRFProtect
from celery import Celery

login_manager = LoginManager()
login_manager.session_protection = None
login_manager.login_view = 'auth.login'
db = SQLAlchemy()
migrate = Migrate()
oauth = OAuth()
azs = FlaskAzureStorage()
csrf = CSRFProtect()
celery = Celery(__name__)


def create_app(cli=False):
    # Checks if APPLICATION_SETTINGS is set. If the environment variable is
    # not set it will set it with a default value. The script will check in a
    # few default locations for a config file.
    if not os.environ.get('APPLICATION_SETTINGS'):
        cluster_config = 'flask-starter.cfg'
        default_config = 'flask-starter-default.cfg'
        dev_config = 'settings.dev.cfg'
        cluster = os.path.abspath(os.path.join(os.sep, 'configs', cluster_config))
        default = os.path.abspath(os.path.join(os.sep, 'default', default_config))
        dev = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'configs', dev_config))

        if os.path.isfile(cluster):
            os.environ['APPLICATION_SETTINGS'] = cluster
        elif os.path.isfile(default):
            os.environ['APPLICATION_SETTINGS'] = default
        elif os.path.isfile(dev):
            os.environ['APPLICATION_SETTINGS'] = dev

    app = Flask(__name__, static_folder='static')
    app.config.from_object(config)
    app.config.from_envvar('APPLICATION_SETTINGS')
    sec = SecretsConfig()
    app.config.from_object(sec)

    login_manager.init_app(app)
    db.init_app(app)
    oauth.init_app(app)
    azs.init_app(app)
    csrf.init_app(app)
    celery.conf.update(app.config)

    # Force SSL redirects
    SSLify(app, permanent=True)

    # Only configures flask_migrate if being run from the command line.
    if cli:
        migrate.init_app(app, db)

    # Registers custom filters in the template engine.
    app.jinja_env.globals.update(permission_required=check_access)
    app.jinja_env.globals.update(current_year=current_year)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .error import error as error_blueprint
    from .profile import profile as profile_blueprint
    from .data import data as data_blueprint
    from .admin import admin as admin_blueprint
    from .api.v1 import api_v1_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(error_blueprint, url_prefix='/error')
    app.register_blueprint(profile_blueprint, url_prefix='/profile')
    app.register_blueprint(data_blueprint, url_prefix='/data')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    # Exempt API Routes from CSRF protection
    csrf.exempt(api_v1_blueprint)

    return app

import os
import ssl

from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class SecretsConfig:
    """Loads all environmental variables and sets them as attributes"""
    def __init__(self):
        for k, v in os.environ.items():
            self.__dict__[k] = v


class Config:

    # General Settings
    APP_VERSION = 'N/A'
    APP_COMMIT = 'N/A'
    APP_COMMIT_FULL = 'null'
    SITE_NAME = 'flask-starter'

    # Upload Settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'temp')
    ALLOWED_EXTENSIONS = {'csv', 'tsv'}

    # Security Settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_REFRESH_EACH_REQUEST = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = False
    PREFERRED_URL_SCHEME = 'https'
    AUTH_TYPE = 'OpenID'
    SWAGGER_UI_DOC_EXPANSION = 'list'

    # Default Database Settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 120

    # Celery Settings
    CELERY_REDIRECT_STDOUTS = False
    CELERY_TIMEZONE = 'America/Los_Angeles'
    BROKER_TRANSPORT_OPTIONS = {
        'visibility_timeout': 3600,
        'fanout_prefix': True,
        'fanout_patterns': True
    }


config = Config

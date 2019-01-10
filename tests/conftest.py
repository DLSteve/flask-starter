import os
import json
import pytest

from app import create_app
from app import db
from app.models import Role, Permission


@pytest.fixture(scope='session', autouse=True)
def app():
    new_app = create_app()
    new_app.app_context().push()
    return new_app


@pytest.fixture(scope='class')
def database():
    basedir = os.path.abspath(os.path.dirname(__file__))
    db.create_all()
    with open(os.path.join(basedir, '..', 'app', 'seedfiles', 'permissions.json')) as perm_file:
        perm = json.load(perm_file)
    with open(os.path.join(basedir, '..', 'app', 'seedfiles', 'roles.json')) as role_file:
        roles = json.load(role_file)
    Permission.insert_permissions(perm)
    Role.insert_roles(roles)
    yield db
    db.session.remove()
    db.drop_all()

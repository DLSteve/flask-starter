import pytest
from app.models import User, AnonymousUser, Role


@pytest.mark.usefixtures('app')
class TestAnonUser:
    def test_user_can(self):
        u = AnonymousUser()
        assert not u.can('default')

    def test_is_administrator(self):
        u = AnonymousUser()
        assert not u.is_administrator()


@pytest.mark.usefixtures('app')
class TestUserRoles:
    def test_ops(self, database):
        role1 = Role.query.filter_by(name='IAM Operations').first()
        u = User(username='opstestor')
        u.roles.append(role1)
        assert u.can('pwr_upload')
        assert not u.can('api_pwr_read')
        assert not u.is_administrator()

    def test_api_user(self, database):
        role1 = Role.query.filter_by(name='DataStudio API User').first()
        u = User(username='apitestor')
        u.roles.append(role1)
        assert u.can('api_pwr_read')
        assert not u.can('pwr_upload')
        assert not u.is_administrator()

    def test_multi_user(self, database):
        role1 = Role.query.filter_by(name='IAM Operations').first()
        role2 = Role.query.filter_by(name='DataStudio API User').first()
        u = User(username='multitestor')
        u.roles.append(role1)
        u.roles.append(role2)
        assert u.can('api_pwr_read')
        assert u.can('pwr_upload')
        assert not u.is_administrator()

    def test_admin(self, database):
        role1 = Role.query.filter_by(name='Administrator').first()
        u = User(username='admintestor')
        u.roles.append(role1)
        assert u.can('api_pwr_read')
        assert u.can('pwr_upload')
        assert u.is_administrator()

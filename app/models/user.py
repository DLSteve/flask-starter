from datetime import datetime
from flask import current_app
from app import db, login_manager
from app.auth_utilities import generate_random_id
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired, URLSafeSerializer
from .settings import Settings
from sqlalchemy.exc import IntegrityError


roles = db.Table('user_role_mapper',
                 db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                 db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
                 )

permissions = db.Table('role_permission_mapper',
                       db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                       )


class Permission(db.Model):
    """Individual Permissions for Users."""
    __tablename__ = 'permission'
    id = db.Column(db.Integer, db.Sequence('permission_id_seq'), primary_key=True)
    name = db.Column(db.Unicode(64), unique=True, index=True)

    def __repr__(self):
        return '<Permission %r>' % self.name

    @staticmethod
    def insert_permissions(perms):
        if perms:
            for p in perms:
                permission = Permission.query.filter_by(name=p).first()
                if permission is None:
                    permission = Permission(name=p)
                    db.session.add(permission)
            db.session.commit()

    @staticmethod
    def clean_permissions(perms):
        if perms:
            all_permissions = Permission.query.all()
            for p in all_permissions:
                if p.name not in perms:
                    db.session.delete(p)
            db.session.commit()


class Role(db.Model):
    """User's Role."""
    __tablename__ = 'role'
    id = db.Column(db.Integer, db.Sequence('role_id_seq'), primary_key=True)
    name = db.Column(db.Unicode(64), unique=True, index=True)
    permissions = db.relationship('Permission', secondary=permissions,
                                  backref=db.backref('roles', lazy='dynamic', cascade='all'))

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles(rls):
        if rls:
            for r in rls:
                role = Role.query.filter_by(name=r).first()
                if role is None:
                    role = Role(name=r)
                    db.session.add(role)
                for p in role.permissions:
                    if p.name not in rls[r]:
                        role.permissions.remove(p)
                perm_names = [pr.name for pr in role.permissions]
                for p in rls[r]:
                    if p not in perm_names:
                        permission = Permission.query.filter_by(name=p).first()
                        role.permissions.append(permission)
            db.session.commit()


class User(UserMixin, db.Model):
    """Site User"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, db.Sequence('users_id_seq'), primary_key=True)
    username = db.Column(db.Unicode(64), unique=True, index=True)
    first_name = db.Column(db.Unicode(64), index=True)
    last_name = db.Column(db.Unicode(64), index=True)
    user_id = db.Column(db.Unicode(64))
    updated = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles, backref=db.backref('users', lazy='dynamic', cascade='all'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def can(self, perm):
        role_perm = []
        for role in self.roles:
            for p in role.permissions:
                role_perm.append(p.name)
                if p.name == 'terminated':
                    return None
                if p.name == 'admin':
                    return perm
        return perm in role_perm

    def is_administrator(self):
        return self.can('admin')

    def set_user_id(self):
        if not self.user_id:
            id_set = False
            while not id_set:
                user_id = generate_random_id(10)
                id_exists = User.query.filter_by(user_id=user_id).first()
                if not id_exists:
                    self.user_id = user_id
                    id_set = True

    @staticmethod
    def generate_api_key(secret):
        s = URLSafeSerializer(secret)
        full_key = s.dumps({'user_id': 'ZZZZZ99999'}).split('.')
        if full_key[0] and full_key[1]:
            key_base = Settings.query.get('api_key_base')
            if not key_base:
                key_base = Settings(
                    id='api_key_base',
                    value=full_key[0]
                )
                db.session.add(key_base)
                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    raise
            return full_key[1]
        return None

    @staticmethod
    def verify_api_key(secret, key):
        s = URLSafeSerializer(secret)
        key_base = Settings.query.get('api_key_base')
        if key_base:
            full_key = '{}.{}'.format(key_base.value, key)
            try:
                data = s.loads(full_key)
            except BadSignature:
                return None
            user = User.query.filter_by(user_id=data['user_id']).first()
            return user
        return None

    def generate_auth_token(self, expiration):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'],
                                            expires_in=expiration)
        return s.dumps({'user_id': self.user_id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.filter_by(user_id=data['user_id']).first()
        return user

    def __repr__(self):
        return '<User id: {}, username: {}>'.format(self.id, self.username)


class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser

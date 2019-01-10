import random
import string
from functools import wraps
from flask import abort, current_app
from flask_login import current_user
from app import util


def check_access(permission=None, user=current_user):
    """Checks if a user has the correct attributes needed for access.

    Args:
        permission: A specific permission or permissions the user requires for access. Can be a single string or
            multiple permissions passed as a python list. If a list of permissions is passed, the user must have all
            the required permissions on order to pass the check. Default is None.
        user: User object to test against. Default is current_user from flask_login.

    Returns:
        True if successful, False otherwise. If no parameters are passed, False is returned by default.

    """
    # Makes sure there is at least one parameter.
    if permission:

        # Allow access to route if AUTH_DISABLED config is set to true.
        if current_app.config.get('AUTH_DISABLED'):
            return True

        # Anonymous users rejected by default.
        if user.is_anonymous:
            return False

        if permission:
            if util.is_iterable(permission):
                for p in permission:
                    if not user.can(p):
                        return False
            elif not user.can(permission):
                return False

        return True

    # 403 Aborts by default for security.
    else:
        return False


def permission_required(permission=None):
    """Decorator wrapper for check_access to use in view functions.

       The wrapper() function will run abort(403) if the check is not passed.

    Args:
        permission: A specific permission or permissions the user requires for access. Can be a single string or
            multiple permissions passed as a python list. If a list of permissions is passed, the user must have all
            the required permissions on order to pass the check. Default is None.

    Returns:
        None.

    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            authorized = check_access(permission=permission)
            if authorized:
                return f(*args, **kwargs)

            # 403 Aborts by default for security.
            else:
                abort(403)
        return wrapper
    return decorator


def admin_required(f):
    return permission_required('admin')(f)


def generate_password(length):
    """Function for generating passwords or secrets. It uses the
     cryptographically more secure random.SystemRandom() for selecting
     characters for the passwords.

    Args:
        length: An Int value for password length.

    Returns:
        A password as a String value.

    """
    return ''.join(random.SystemRandom().choice(
        string.ascii_letters + string.punctuation + string.digits) for _ in range(length))


def generate_random_id(length):
    """Function for generating random IDs. It uses the
     cryptographically more secure random.SystemRandom() for selecting
     characters for the ID.

    Args:
        length: An Int value for ID length.

    Returns:
        A ID as a String value.

    """
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

import time

from flask import url_for
from urllib.parse import urlparse, urlunparse
from werkzeug.urls import url_decode, url_encode


def make_next_param(base_url, next_url):
    l = urlparse(base_url)
    c = urlparse(next_url)
    if (not l.scheme or l.scheme == c.scheme) and (not l.netloc or l.netloc == c.netloc):
        return urlunparse(('', '', c.path, c.params, c.query, ''))
    return next_url


def login_url(login_view, next_url=None, next_field='next'):
    if login_view.startswith(('https://', 'http://', '/')):
        base = login_view
    else:
        base = url_for(login_view)
    if next_url is None:
        return base
    parts = list(urlparse(base))
    md = url_decode(parts[4])
    md[next_field] = make_next_param(base, next_url)
    parts[4] = url_encode(md, sort=True)
    return urlunparse(parts)


def is_iterable(value):
    """Checks if an object is a list or tuple.

    Args:
        value: Object to check.

    Returns:
        True if the object is a list or tuple, False otherwise.

    """
    return isinstance(value, (tuple, list))


def current_year():
    """Gets the current year.

    Returns:
        The current year as a string.

    """
    return time.strftime('%Y')


def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

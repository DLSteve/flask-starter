from app import login_manager
from app.util import login_url
from flask import render_template, request, redirect, jsonify, abort
from . import error


@error.app_errorhandler(400)
def bad_request(e):
    if request.path.startswith('/api/'):
        response = jsonify({'error': 'bad request'})
        response.status_code = 400
        return response
    return render_template('error/400.html'), 400


@error.app_errorhandler(401)
def unauthorized(e):
    if request.path.startswith('/api/'):
        response = jsonify({'error': 'unauthorized'})
        response.status_code = 401
        return response
    return render_template('error/401.html'), 401


@error.app_errorhandler(403)
def forbidden(e):
    if request.path.startswith('/api/'):
        response = jsonify({'error': 'forbidden'})
        response.status_code = 403
        return response
    return render_template('error/403.html'), 403


@error.app_errorhandler(404)
def page_not_found(e):
    if request.path.startswith('/api/'):
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('error/404.html'), 404


@error.app_errorhandler(500)
def internal_server_error(e):
    if request.path.startswith('/api/'):
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template('error/500.html'), 500


@login_manager.unauthorized_handler
def unauthorized():
    login_view = login_manager.login_view
    if not login_view or request.path.startswith('/api/'):
        abort(401)
    return redirect(login_url(login_view, request.url))

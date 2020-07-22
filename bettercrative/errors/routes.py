from flask import render_template, Blueprint

errors = Blueprint('errors', __name__)


@errors.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400


@errors.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401


@errors.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@errors.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

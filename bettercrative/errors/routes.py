from flask import render_template, Blueprint

errors = Blueprint('errors', __name__)


@errors.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

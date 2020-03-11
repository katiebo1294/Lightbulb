from flask import render_template, request, Blueprint, make_response, url_for, flash, redirect
from flask_login import current_user, login_user

from bettercrative import bcrypt
from bettercrative.classrooms.forms import EnterClassroomForm
from bettercrative.users.forms import LoginForm

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    # A logged-in user's homepage is their account page; otherwise it's the sign-in page
    if current_user.is_authenticated:
        redirect(url_for('users.account'))
        return render_template('account.html')
    else:
        return render_template('home.html')


@main.route('/about')
def about():
    return render_template('about.html')

# For testing CodeMirror
@main.route('/test')
def test():
    return render_template('test.html')

# Routing for 404 errors
@main.route("/<page_name>")
def other_page(page_name):
    response = make_response(render_template('404.html'), 404)
    return render_template('404.html')


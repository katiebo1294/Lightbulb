from flask import render_template, request, Blueprint, make_response
from flask_login import current_user
from bettercrative.users.forms import LoginForm, StudentLoginForm

from bettercrative.models import Classroom, Quiz

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('login_home.html')
    else:
        return render_template('home.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route("/<page_name>")
def other_page(page_name):
    response = make_response(render_template('404.html'), 404)
    return render_template('404.html')

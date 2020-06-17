from flask import render_template, Blueprint, make_response, url_for, redirect
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    """ Displays the "home" page. If the user is signed in, this becomes their "account" page. """
    if current_user.is_authenticated:
        redirect(url_for('users.account'))
        return render_template('account.html')
    else:
        return render_template('home.html')


@main.route('/about')
def about():
    """ Displays the "about" page. """
    return render_template('about.html')


@main.route("/<page_name>")
def other_page(page_name):
    """ 404 error routes """
    response = make_response(render_template('404.html'), 404)
    return render_template('404.html')

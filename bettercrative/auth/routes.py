from flask import render_template
from flask_login import login_required
from . import auth


@auth.route('/login')
def login():
    return render_template('auth/login.html')

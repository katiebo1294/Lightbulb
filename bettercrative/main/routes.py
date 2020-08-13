from flask import render_template, Blueprint, make_response, url_for, redirect, request, flash
from flask_login import current_user

from bettercrative import db, bcrypt
from bettercrative.models import User, Quiz, Classroom, Question
from bettercrative.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                       RequestResetForm, ResetPasswordForm)
from bettercrative.classrooms.forms import ClassroomForm, EnterClassroomForm
from bettercrative.quizzes.forms import QuizForm

main = Blueprint('main', __name__)


@main.route('/',  methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    """ Displays the "home" page. """
    if current_user.is_authenticated:
        return render_template('user_home.html', classForm=ClassroomForm(), quizForm=QuizForm())
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

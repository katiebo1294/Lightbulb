from flask import render_template, request, Blueprint, make_response, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from bettercrative.users.forms import LoginForm, StudentLoginForm

from bettercrative.models import Classroom, Quiz, User

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        redirect(url_for('users.account'))
        return render_template('account.html')
    else:
        return render_template('home.html')



@main.route('/about')
def about():
    return render_template('about.html')


#to do - work out how to take user id and retrieve classroom id from it
#then afterwards do that with the key

#this works a bit individually. You can type out the url and it will render the classroom html page
#query works but doesn't serve any function yet 

@main.route("/classroom") #to do - make dynamic
@login_required
def user_classrooms():
    classroom = Classroom.query.filter_by(user_id=id)
    redirect(url_for('main.user_classrooms'))
    return render_template('classroom.html')




# displays the current user's created quizzes
@main.route("/user/quizzes")
@login_required
def user_quizzes():
    user = User.query.filter_by(current_user)
    quizzes = Quiz.query.filter_by(quiz_owner=user) \
        .order_by(Quiz.date_created.desc())
    return render_template('user_quizzes.html')


@main.route("/<page_name>")
def other_page(page_name):
    response = make_response(render_template('404.html'), 404)
    return render_template('404.html')


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
    """ Displays the "home" page. If the user is signed in, this becomes their "account" page. """
    if current_user.is_authenticated:
        form = UpdateAccountForm()
        classForm =  ClassroomForm()
        quizForm = QuizForm()

        if quizForm.submitQuiz.data and quizForm.validate_on_submit():
            quiz = Quiz(
                name=quizForm.name.data,
                owner=current_user
            )
            first_question = Question(quiz_id=quiz.id, name="Question 1")
            db.session.add(first_question)
            quiz.questions.append(first_question)
            db.session.add(quiz)

            db.session.commit()
            flash(u'New quiz \"' + quiz.name + '\" created!', 'success')
            quiz.active = first_question.id
            print(quiz.active)
            return redirect(url_for('users.account'))

        # classroom form
        if classForm.submitClass.data and classForm.validate_on_submit():
            classroom = Classroom(name=classForm.name.data, owner=current_user)
            db.session.add(classroom)
            db.session.commit()
            flash(u'New classroom \"' + classroom.name + '\" created!', 'success')
            return redirect(url_for('users.account'))

        # profile form
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash(u'Your account has been updated!', 'success')
            return redirect(url_for('users.account'))

        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        return render_template('account.html', title='Account',
                            image_file=image_file, form=form, classForm=classForm, quizForm=quizForm)
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

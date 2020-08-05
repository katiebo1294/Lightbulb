from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from bettercrative import db, bcrypt
from bettercrative.models import User, Quiz, Classroom, Question
from bettercrative.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                       RequestResetForm, ResetPasswordForm)
from bettercrative.classrooms.forms import ClassroomForm, EnterClassroomForm
from bettercrative.quizzes.forms import QuizForm
from bettercrative.users.util import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    """ Register a new (teacher) account. """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(u'Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """ Log in to an existing (teacher) account. """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash(u'You have been successfully logged in!', 'success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(u'Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    """ Log out of the current (teacher) account. """
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/quizzes", methods=['GET', 'POST'])
@login_required
def quizzes():
    """ Display the current user's created quizzes. """
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
        return redirect(url_for('users.quizzes'))
    return render_template('quizzes.html', title="Quizzes", quizForm=quizForm)


@users.route("/classrooms", methods=['GET', 'POST'])
@login_required
def classrooms():
    """ Display the current user's created classrooms. """
    classForm = ClassroomForm()

    if classForm.submitClass.data and classForm.validate_on_submit():
        classroom = Classroom(name=classForm.name.data, owner=current_user)
        db.session.add(classroom)
        db.session.commit()
        flash(u'New classroom \"' + classroom.name + '\" created!', 'success')
        return redirect(url_for('users.classrooms'))
    return render_template('classrooms.html', title="Classrooms", classForm=classForm)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """ Display the current user's account page. """
    form = UpdateAccountForm()

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
                           image_file=image_file, form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """ Request a password reset for the current user. """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(u'An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """ Resets the password based on the given token.
    
        Parameters:
                token (int): the token created during the reset request.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash(u'That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash(u'Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

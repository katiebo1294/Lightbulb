from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from bettercrative import db
from bettercrative.models import Classroom, Quiz
from bettercrative.quizzes.forms import QuizForm

quizzes = Blueprint('quizzes', __name__)


@quizzes.route("/quiz/new", methods=['GET', 'POST'])
@login_required
def new_quiz():
    form = QuizForm()
    if form.validate_on_submit():
        quiz = Quiz(quiz_Name=form.quiz_Name.data)
        db.session.add(quiz)
        db.session.commit()
        flash('New Quiz Created!', 'success')
    return render_template('create_quiz.html', title='New Quiz', form=form)


# TODO: make quiz home route page
@quizzes.route("/quiz/<int:id>")
@login_required
def quiz(id):
    quiz = Quiz.query_or_404(id)
    return render_template('quiz.html', title=quiz.quiz_Name, quiz=quiz)
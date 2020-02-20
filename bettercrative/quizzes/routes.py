from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from bettercrative import db
from bettercrative.models import Quiz, Question, Answer
from bettercrative.quizzes.forms import QuizForm

quizzes = Blueprint('quizzes', __name__)


@quizzes.route("/quiz/new", methods=['GET', 'POST'])
@login_required
def new_quiz():
    form = QuizForm()
    if form.validate_on_submit():
<<<<<<< HEAD
        quiz = Quiz(quiz_Name=form.quiz_Name.data)
=======
        quiz = Quiz(name=form.name.data, owner=current_user)
>>>>>>> katie
        db.session.add(quiz)
        # add each question to the quiz
        for question in form.questions.data:
            question = Question(**question)
            # add each answer to the question
            for answer in question.answers.data:
                answer = Answer(**answer)
                question.answers.append(answer)
            quiz.questions.append(question)
        db.session.commit()
        flash(u'New Quiz "{{ name }}" Created!', 'success')
    return render_template('create_quiz.html', title='New Quiz', form=form)


# TODO: make quiz home route page
@quizzes.route("/quiz/<int:id>")
@login_required
def quiz(id):
    quiz = Quiz.query_or_404(id)
    return render_template('quiz.html', title=quiz.name, quiz=quiz)
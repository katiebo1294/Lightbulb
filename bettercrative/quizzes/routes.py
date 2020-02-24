from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from bettercrative import db
from bettercrative.models import Quiz, Question, Answer
from bettercrative.quizzes.forms import QuizForm, QuestionForm

quizzes = Blueprint('quizzes', __name__)


@quizzes.route("/quiz/new", methods=['GET', 'POST'])
@login_required
def new_quiz():
    form = QuizForm()
    if form.validate_on_submit():
        new_quiz = Quiz(name=form.name.data, owner=current_user)
        db.session.add(new_quiz)
        # add each question to the quiz
        for question in form.questions.data:
            new_question = Question(**question)
            # add each answer to the question
            qform = QuestionForm()
            for answer in qform.answers.data:
                new_answer = Answer(**answer)
                new_question.answers.append(new_answer)
            new_quiz.questions.append(new_question)
        db.session.commit()
        flash(u'New Quiz \"' + quiz.name + '\" Created!', 'success')
        return redirect(url_for('quizzes.quiz', id=quiz.id))
    return render_template('create_quiz.html', title='New Quiz', form=form)


# TODO: make quiz home route page
@quizzes.route("/quiz/<int:id>")
@login_required
def quiz(id):
    quiz = Quiz.query.get_or_404(id)
    return render_template('quiz.html', title=quiz.name, quiz=quiz)

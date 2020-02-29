from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from bettercrative import db
from bettercrative.classrooms.routes import classroom
from bettercrative.models import Quiz, Answer, Classroom, User
from bettercrative.quizzes.forms import QuizForm

quizzes = Blueprint('quizzes', __name__)


@quizzes.route("/quiz/new", methods=['GET', 'POST'])
@login_required
def new_quiz():
    form = QuizForm()
    if form.validate_on_submit():
        quiz = Quiz(name=form.name.data, question_content=form.question_content.data, owner=current_user)
        db.session.add(quiz)
        # add each question to the quiz
        for answer in form.question_answers.data:
            new_answer = Answer(**answer)
            # add each answer to the question
            quiz.question_answers.append(new_answer)
        db.session.commit()
        flash(u'New quiz \"' + quiz.name + '\" created!', 'success')
        # if a classroom id was passed in, redirect to add this new quiz to that classroom
        if form.classroomid:
            #gets the quiz by id through form and assigns said quiz to the active_quiz
            classroom = Classroom.query.filter_by(name=form.classroomid.data).first()
            addedQuiz = Quiz.query.filter_by(id=quiz.id).first()
            classroom.added_quizzes.append(addedQuiz)
            db.session.commit()
            flash(u'Quiz \"' + addedQuiz.name + '\" added to \"' + classroom.name + '\"!', 'success')
            return redirect(url_for('classrooms.classroom', id=classroom.id))
        else:
            return redirect(url_for('quizzes.quiz', id=quiz.id))
    return render_template('create_quiz.html', title='New Quiz', form=form)


@quizzes.route("/quiz/<int:id>")
@login_required
def quiz(id):
    quiz = Quiz.query.get_or_404(id)
    return render_template('account.html', title=quiz.name, quiz=quiz)

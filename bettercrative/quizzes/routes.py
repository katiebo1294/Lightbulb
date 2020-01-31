from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from bettercrative import db
from bettercrative.models import Quizzes
from bettercrative.quizzes.forms import QuizForm

classrooms = Blueprint('quizzes', __name__)


@classrooms.route("/quiz/new", methods=['GET', 'POST'])
@login_required
def new_quiz():
    form = QuizForm()
    if form.validate_on_submit():
        quiz = Quizzes(quizzes_Name=form.quizzes_Name.data)
        db.session.add(quiz)
        db.session.commit()
        flash('New Quiz Created!', 'success')
    return render_template('create_quiz.html', title='New Quiz', form=form)




#make quiz home route page
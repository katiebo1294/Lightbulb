from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from bettercrative import db
from bettercrative.models import Classroom, Quiz
from bettercrative.classrooms.forms import ClassroomForm

classrooms = Blueprint('classrooms', __name__)


# TODO: when user attempts to create new classroom, check if there is already a classroom attached to their id(?)
@classrooms.route("/classroom/new", methods=['GET', 'POST'])
@login_required
def new_classroom():
    form = ClassroomForm()
    if form.validate_on_submit():
        classroom = Classroom(name=form.name.data, owner=current_user)
        db.session.add(classroom)
        db.session.commit()
        flash(u'Classroom created!', 'success')
        return redirect(url_for('users.account'))
        # TODO: have flash message say the specific classroom name
    return render_template('create_classroom.html', title='New Classroom', form=form)


# TODO: add ability to add quiz to classroom
@classrooms.route("/classroom/<int:id>")
@login_required
def classroom(id):
    classroom = Classroom.query_or_404(id)
    return render_template('classroom.html', title=classroom.name, classroom=classroom)


def add_quiz(id):
    classroom = Classroom.query_or_404(id)
    quizzes = Quiz.query.filter_by(owner=current_user)
    flash(u'Quiz added to classroom!', 'success')
    # TODO: have flash message say the specific classroom name
    return render_template('classroom.html', title=classroom.name, classroom=classroom)
    # TODO allow user to select a quiz they have already made, or create a new one, to be put into this classroom

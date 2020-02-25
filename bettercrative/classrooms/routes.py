from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from bettercrative import db
from bettercrative.models import Classroom, Quiz
from bettercrative.classrooms.forms import ClassroomForm, EnterClassroomForm, AddQuizForm

classrooms = Blueprint('classrooms', __name__)


@classrooms.route("/classroom/new", methods=['GET', 'POST'])
@login_required
def new_classroom():
    form = ClassroomForm()
    if form.validate_on_submit():
        classroom = Classroom(name=form.name.data, owner=current_user)
        db.session.add(classroom)
        db.session.commit()
        flash(u'Classroom\"' + classroom.name + '\" created!', 'success')
        # TODO: have flash message say the specific classroom name
        return redirect(url_for('classrooms.classroom', id=classroom.id))
    return render_template('create_classroom.html', title='New Classroom', form=form)


@classrooms.route("/classroom/enter", methods=['GET', 'POST'])
def enter_classroom():
    form = EnterClassroomForm()
    if form.validate_on_submit():
        classroom = Classroom.query.filter_by(name=form.room_id.data).first()
        if classroom:
            return redirect(url_for('classrooms.classroom', id=classroom.id, classroom=classroom))
        else:
            flash(u'A classroom does not exist with that name. Please try again.', 'danger')
    return render_template('enter_classroom.html', title='get in chief', form=form)


# displays a specific classroom (student view)
@classrooms.route("/classroom/<int:id>")
def classroom(id):
    classroom = Classroom.query.get_or_404(id)
    return render_template('classroom.html', classroom=classroom)


def add_quiz(id):
    classroom = Classroom.query_or_404(id)
    quizzes = Quiz.query.filter_by(owner=current_user)
    form = AddQuizForm(classroom_host=classroom)
    flash(u'Quiz added to\"' + classroom.name + '\"!', 'success')
    # TODO: have flash message say the specific classroom name
    return render_template('classroom.html', title=classroom.name, classroom=classroom)
    # TODO allow user to select a quiz they have already made, or create a new one, to be put into this classroom

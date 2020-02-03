from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from bettercrative import db
from bettercrative.models import Classroom, Quiz
from bettercrative.classrooms.forms import ClassroomForm

classrooms = Blueprint('classrooms', __name__)


# TODO: when user attempts to create new classroom, check if there is already a classroom attached to their user_id(?)
@classrooms.route("/classroom/new", methods=['GET', 'POST'])
@login_required
def new_classroom():
    form = ClassroomForm()
    if form.validate_on_submit():
        classroom = Classroom(classroom_Name=form.classroom_Name.data, classroom_Content=form.classroom_Content,
                             key=form.key.data, author=current_user)
        db.session.add(classroom)
        db.session.commit()
        flash('New Classroom Created!', 'success')
    return render_template('create_classroom.html', title='New Classroom', form=form)


# TODO: add ability to add quiz to classroom
@classrooms.route("/classroom/<int:classroom_id>")
@login_required
def classroom(classroom_id):
    classroom = Classroom.query_or_404(classroom_id)
    return render_template('classroom.html', title=classroom.classroom_Name, classroom=classroom)

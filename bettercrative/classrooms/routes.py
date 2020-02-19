from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from bettercrative import db
from bettercrative.models import Classroom, Quiz
from bettercrative.classrooms.forms import ClassroomForm, enterClassroom

classrooms = Blueprint('classrooms', __name__)


@classrooms.route("/classroom/new", methods=['GET', 'POST'])
@login_required
def new_classroom():
    form = ClassroomForm()
    if form.validate_on_submit():
        classroom = Classroom(classroom_Name=form.classroom_Name.data, key=form.key.data, user_id=current_user.username)
        db.session.add(classroom)
        db.session.commit()
        flash('Clasroom created! ', 'success')
        # TODO: have flash message say the specific classroom name
        return redirect(url_for('main.home')) #should redirect to the classroom
    return render_template('create_classroom.html', title='New Classroom', form=form)

@classrooms.route("/enter_classroom", methods=['GET', 'POST'])
def enter_classroom():
    form = enterClassroom()
    if form.validate_on_submit and  form.validate_entrance(input_key=form.input_key, classroomName=form.classroomName):
        return redirect(url_for('main.home')) #should redirect to classroom later
    return render_template('enter_classroom.html', title='get in chief', form=form)


# TODO: add ability to add quiz to classroom
@classrooms.route("/classroom/<int:id>")
@login_required
def classroom(id):
    classroom = Classroom.query_or_404(id)
    return render_template('classroom.html', title=classroom.classroom_Name, classroom=classroom)


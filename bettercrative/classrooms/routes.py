from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint,
                   request)
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
        flash(u'New classroom \"' + classroom.name + '\" created!', 'success')
        return redirect(url_for('classrooms.classroom', id=classroom.id))
    return render_template('create_classroom.html', title='New Classroom', form=form)


@classrooms.route("/classroom/enter", methods=['GET', 'POST'])
def enter_classroom():
    form = EnterClassroomForm()
    if form.validate_on_submit():
        classroom = Classroom.query.filter_by(name=form.room_id.data).first()
        if classroom:
            return redirect(url_for('classrooms.classroom', id=classroom.id))
        else:
            flash(u'A classroom does not exist with that name. Please try again.', 'danger')
    return render_template('enter_classroom.html', title='get in chief', form=form)


# displays a specific classroom TODO if logged in and classroom owner, add option to edit/add a quiz
@classrooms.route("/classroom/<int:id>", methods=['GET', 'POST'])
def classroom(id):
    classroom = Classroom.query.get_or_404(id)
    quizzes = classroom.added_quizzes
    # if there is an active quiz, pass it to the template; else pass None
    # TIM -> "REMOVED DUE TO ACTIVE_QUIZ BEING MOVED TO CLASSROOM FOCUS, MAYBE ADD IN LATER?"
    #active_quiz = None
    #for quiz in quizzes:
    #    if quiz.active:
    #        active_quiz = quiz
    return render_template('classroom.html', title=classroom.name, classroom=classroom) #, active_quiz=active_quiz <- THIS WAS REMOVED FROM END OF THIS LINE


@classrooms.route("/classroom/<int:id>/add-quiz", methods=['GET', 'POST'])
@login_required
def add_quiz(id):
    classroom = Classroom.query.get_or_404(id)
    # retrieve the current user's quizzes, create tuples with (id, name) as choices for the form
    quizzes = Quiz.query.filter_by(user_id=current_user.id).all()
    quiz_list = [(q.id, q.name) for q in quizzes]
    form = AddQuizForm()
    form.quiz.choices = quiz_list
    if form.validate_on_submit():
        #gets the quiz by id through form and assigns said quiz to the active_quiz
        quizID = form.quiz.data
        addedQuiz = Quiz.query.filter_by(id=quizID).first()
        classroom.added_quizzes.append(addedQuiz)
        db.session.commit()
        flash(u'Quiz \"' + addedQuiz.name + '\" added to \"' + classroom.name + '\"!', 'success')
        return redirect(url_for('classrooms.classroom', id=classroom.id))
    return render_template('add_quiz.html', title=classroom.name, classroom=classroom, form=form)
    # TODO allow user to select a quiz they have already made, or create a new one, to be put into this classroom

@classrooms.route("/classroom/set_active", methods=['GET', 'POST'])
@login_required
def set_active():
    # gets the name and class_id from the URL params
    name = request.args.get('name', None)
    class_id = request.args.get('classroom_id', None)

    #TODO: make custom exceptions and catch them somewhere along the line to give the user a useful error page. 
    if name is None:
        raise Exception('No \'name\' supplied!')
    if class_id is None:
        raise Exception('No \'classroom_id\' supplied!')

    classroom = Classroom.query.get(class_id)
    classroom.active_quiz = name

    return render_template('account.html')
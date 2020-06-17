from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint,
                   request)
from flask_login import current_user, login_required
from bettercrative import db
from bettercrative.models import Classroom, Quiz, Response
from bettercrative.classrooms.forms import ClassroomForm, EnterClassroomForm, AddQuizForm
from typing import List
classrooms = Blueprint('classrooms', __name__)


@classrooms.route("/classroom/new", methods=['GET', 'POST'])
@login_required
def new_classroom():
    """ Create a new classroom. """
    form = ClassroomForm()
    if form.validate_on_submit():
        classroom = Classroom(name=form.name.data, owner=current_user)
        db.session.add(classroom)
        db.session.commit()
        flash(u'New classroom \"' + classroom.name + '\" created!', 'success')
        return redirect(url_for('classrooms.classroom', classroom_id=classroom.id))
    return render_template('create_classroom.html', title='New Classroom', form=form)

# TODO exception handling for student enter classroom w/o active quiz
@classrooms.route("/classroom/enter", methods=['GET', 'POST'])
def enter_classroom():
    """ Student sign-in to classroom. Classroom must have an active quiz. """
    form = EnterClassroomForm()
    if form.validate_on_submit():
        classroom = Classroom.query.filter_by(name=form.room_id.data).first()
        if classroom and classroom.active_quiz:
            return redirect(url_for('classrooms.take_quiz', classroom_id=classroom.id))
        else:
            flash(u'A classroom does not exist with that name. Please try again.', 'danger')
    return render_template('enter_classroom.html', title='get in chief', form=form)



@classrooms.route("/classroom/<int:classroom_id>", methods=['GET', 'POST'])
def classroom(classroom_id):
    """ 
    Display the given classroom's dashboard.

    Parameters:
            classroom_id (int): the ID of the classroom to display
    """
    classroom = Classroom.query.get_or_404(classroom_id)
    quizzes = classroom.added_quizzes
    for quiz in quizzes:
        print(quiz.classroom_hosts)
    if current_user.is_authenticated:
        return render_template('classroom.html', title=classroom.name, classroom=classroom)
    else:
        quiz = Quiz.query.filter_by(quiz.classroom_hosts.contains(classroom_id)).first()
        return render_template('take_quiz.html', title='TakeQuiz', classroom=classroom, quiz=quiz)

        print(classroom_id)
        return render_template('take_quiz.html', classroom_id=classroom_id)  


@classrooms.route("/classroom/<int:classroom_id>/add_quiz", methods=['GET', 'POST'])
@login_required
def add_quiz(classroom_id):
    """
    Add a quiz to a classroom. Can choose an existing quiz that belongs to the user or create a new one.

    Parameters:
            classroom_id (int): the ID of the classroom to add a quiz to
    """
    classroom = Classroom.query.get_or_404(classroom_id)

    # Seting up the form
    form = AddQuizForm()

    # add default option to "create a quiz" in the dropdown
    default_choice = (0, "Create a Quiz")
    quizzes = Quiz.query.filter_by(user_id = current_user.id).all()

    # putting all quizzes of that user in the list
    quiz_list = [ (quiz.id, quiz.name) for quiz in quizzes]
    quiz_list.append(default_choice)
    form.quiz.choices = quiz_list

    # Handle POST request
    if form.validate_on_submit():
        # get chosen quiz's ID from the form, grab that quiz and attach it to the current classroom
        quiz_id = form.quiz.data
        if quiz_id == 0:
            return redirect(url_for('quizzes.new_quiz'))
        else:
            quiz = Quiz.query.filter_by(id=quiz_id).first()
            classroom.added_quizzes.append(quiz)
            db.session.commit()
            flash(u'Quiz \"' + quiz.name + '\" added to \"' + classroom.name + '\"!', 'success')
            return redirect(url_for('classrooms.classroom', classroom_id=classroom.id))
    
    # Handle GET request
    return render_template('add_quiz.html', title=classroom.name, classroom=classroom, form=form, quiz_list = quiz_list)


# !currently there is a bug where if you click on the nav bar the change gets 
# !reset, however, routing to the page separately or refreshing the page does
# !not break the active-ness
@classrooms.route("/classroom/set_active", methods=['GET', 'POST'])
@login_required
def set_active():
    """
    Sets the given quiz as active in the classroom it's in.
    
    Parameters: 
            quiz_id (int): the ID of the quiz to set active
            classroom_id (int): the ID of the classroom to make it active in
    """
    quiz_id = request.args.get('quiz_id', None)
    quiz = Quiz.query.get_or_404(quiz_id)
    classroom_id= request.args.get('classroom_id', None)
    classroom = Classroom.query.get_or_404(classroom_id)
    
    classroom.active_quiz = quiz_id
    db.session.commit()
    print(classroom.active_quiz)

    return render_template('classroom.html', classroom=classroom)


@classrooms.route("/classroom/remove_active", methods=['GET', 'POST'])
@login_required
def remove_active():
    """ Sets the given quiz to inactive in the current classroom.
    
        Parameters: 
                classroom_id (int): the ID of the classroom to inactive the quiz in
    """
    class_id = request.args.get('classroom_id', None)
    print(class_id)

    #TODO: custom error handling
    if class_id is None:
        raise Exception('No \'classroom_id\' supplied!')

    classroom = Classroom.query.get(class_id)
    if classroom is None:
        return "No Classroom Found", 404
    classroom.active_quiz = None
    db.session.commit()
    print(classroom.active_quiz)

    return "set Empty", 200
  

@classrooms.route("/classroom/<int:classroom_id>/take", methods=['GET', 'POST'])
def take_quiz(classroom_id):
    """ Student takes the given quiz.

        Parameters:
                classroom_id (int): the ID of the classroom the student is signed in to
    """
    classroom = Classroom.query.get_or_404(classroom_id)
    quiz_id = classroom.active_quiz
    quiz = Quiz.query.get_or_404(quiz_id)
    
    #dictionary of true and false for each input
    dicts = {}
    keys = len(quiz.question_answers)
    print(keys)
    i = 0
    for option in quiz.question_answers:
        print(option.content)
        dicts[option.content] = option.correct
    
    #gets a list of what the student responded with
    print(dicts)
    answered = request.form.getlist('studentResponse') 
    print(answered) 


    result = True
    for studentResponse in answered:
        if dicts[studentResponse]==False:
            result = False
        else:
            result = True


    print(result)
    response = Response(classroom_host_id=classroom.id, quiz_reference=quiz.id, isCorrect=str(result))
    db.session.add(response)
    db.session.commit()
    return render_template('take_quiz.html', title='TakeQuiz', classroom=classroom, quiz=quiz)
  


# query database for all responses from this specific classroom, send lists of right and wrong answers to front

@login_required
@classrooms.route("/classroom/<int:classroom_id>/results", methods=['GET', 'POST'])
def view_results(classroom_id):
    """ View the student responses from the given classroom.

        Parameters: 
                classroom_id (int): the ID of the classroom to retrieve answers from
    """
    classroom = Classroom.query.get_or_404(classroom_id)
    
    print("WRONG ANSWERS-------------")
    sumWrong = 0
    wrong_answers = Response.query.filter_by(classroom_host_id=classroom_id, isCorrect='False')
    for y in wrong_answers:
        sumWrong +=1
        print(y)


    print("RIGHT ANSWERS ----------------")
    sumRight = 0
    correct_responses = Response.query.filter_by(classroom_host_id=classroom_id, isCorrect='True')
    for z in correct_responses:
        sumRight +=1
        print(z)

    print(sumRight)
    print(sumWrong)

    return render_template('classroom_results.html', title='results of quiz', rightAnswers=correct_responses, wrongAnswers=wrong_answers, classroomid=classroom_id, sumWrong=sumWrong, sumRight=sumRight)



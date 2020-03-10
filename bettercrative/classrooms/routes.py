from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint,
                   request)
from flask_login import current_user, login_required
from bettercrative import db
from bettercrative.models import Classroom, Quiz, Answer, Response
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
        return redirect(url_for('classrooms.classroom', classroom_id=classroom.id))
    return render_template('create_classroom.html', title='New Classroom', form=form)


@classrooms.route("/classroom/enter", methods=['GET', 'POST'])
def enter_classroom():
    form = EnterClassroomForm()
    if form.validate_on_submit():
        classroom = Classroom.query.filter_by(name=form.room_id.data).first()
        if classroom and classroom.active_quiz:
            return redirect(url_for('classrooms.take_quiz', classroom_id=classroom.id))
        else:
            flash(u'A classroom does not exist with that name. Please try again.', 'danger')
    return render_template('enter_classroom.html', title='get in chief', form=form)


# displays a specific classroom TODO if logged in and classroom owner, add option to edit/add a quiz
@classrooms.route("/classroom/<int:classroom_id>", methods=['GET', 'POST'])
def classroom(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    quizzes = classroom.added_quizzes
    # if there is an active quiz, pass it to the template; else pass None
    # TIM -> "REMOVED DUE TO ACTIVE_QUIZ BEING MOVED TO CLASSROOM FOCUS, MAYBE ADD IN LATER?"
    #active_quiz = None
    #for quiz in quizzes:
    #    if quiz.active:
    #        active_quiz = quiz
    if current_user.is_authenticated:
        return render_template('classroom.html', title=classroom.name, classroom=classroom) #, active_quiz=active_quiz <- THIS WAS REMOVED FROM END OF THIS LINE
    else:
        quiz = Quiz.query.filter_by(classroom_host_id=classroom_id).first()
        return render_template('take_quiz.html', title='TakeQuiz', classroom=classroom, quiz=quiz)

        print(classroom_id)
        return render_template('take_quiz.html', classroom_id=classroom_id)  


@classrooms.route("/classroom/<int:classroom_id>/add_quiz", methods=['GET', 'POST'])
@login_required
def add_quiz(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
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
        return redirect(url_for('classrooms.classroom', classroom_id=classroom.id))
    return render_template('add_quiz.html', title=classroom.name, classroom=classroom, form=form)
    # TODO allow user to select a quiz they have already made, or create a new one, to be put into this classroom



# sets a quiz to the active classroom
# !currently there is a bug where if you click on the nav bar the change gets 
# !reset, however, routing to the page separately or refreshing the page does
# !not break the active-ness
@classrooms.route("/classroom/<int:quiz_id>/set_active", methods=['GET', 'POST'])
@login_required
def set_active(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    classroom = Classroom.query.get_or_404(quiz.classroom_host_id)
    print(quiz)
    print(classroom)
    classroom.active_quiz = quiz_id
    db.session.commit()
    print(classroom.active_quiz)

    return render_template('classroom.html', classroom=classroom)

   
# Removes the active quiz for a class
@classrooms.route("/classroom/remove_active", methods=['GET', 'POST'])
@login_required
def remove_active():
    # gets the name and class_id from the URL params
    class_id = request.args.get('classroom_id', None)
    print(class_id)

    #TODO: make custom exceptions and catch them somewhere along the line to give the user a useful error page. 
    # if name is None:
    #     raise Exception('No \'name\' supplied!')
    if class_id is None:
        raise Exception('No \'classroom_id\' supplied!')

    classroom = Classroom.query.get(class_id)
    if classroom is None:
        return "No Classroom Found", 404
    classroom.active_quiz = None
    db.session.commit()
    print(classroom.active_quiz)

    return "set Empty", 200
  
  
  
  
#Allows user to take an active quiz 
#The stuff that is printed is displayed in the terminal and is for testing purposes
#this is still a work in progress but it does stuff rn
@classrooms.route("/classroom/<int:classroom_id>/take", methods=['GET', 'POST'])
def take_quiz(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    # TODO maybe try filtering by name=classroom.active_quiz
    quiz = Quiz.query.filter_by(classroom_host_id=classroom_id).first() #add active=True arg later
    #print("This is the question: " + quiz.question_content)
    
    #dictionary of true and false for each input
    dicts = {}
    keys = len(quiz.question_answers)
    print(keys)
    i = 0
    for option in quiz.question_answers:
        print(option.content)
        dicts[option.content] = option.correct
    
    
    print(dicts)
    answered = request.form.getlist('studentResponse') #gets a list of what the student respondeed with
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
  

#Need to query the databases for all the student responses based on a classroom id
#Get all the falses and true
#Send that information to the front to display as lists

@login_required
@classrooms.route("/classroom/<int:classroom_id>/results", methods=['GET', 'POST'])
def view_results(classroom_id):

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


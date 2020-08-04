from flask import (render_template, url_for, flash,
                   redirect, Blueprint,session,
                   request, make_response)
from flask_login import current_user, login_required
from sqlalchemy import exists, and_

from bettercrative import db
from bettercrative.classrooms.forms import ClassroomForm, EnterClassroomForm, AddQuizForm
from bettercrative.models import Classroom, Quiz, Response, Question, assoc, Answer, Student

classrooms = Blueprint('classrooms', __name__)


@classrooms.route("/classroom/new", methods=['GET', 'POST'])
@login_required
def new_classroom():
    """ Create a new classroom. """
    classForm = ClassroomForm()
    if classForm.validate_on_submit():
        classroom = Classroom(name=classForm.name.data, owner=current_user)
        db.session.add(classroom)
        db.session.commit()
        flash(u'New classroom \"' + classroom.name + '\" created!', 'success')
        return redirect(url_for('classrooms.classroom', classroom_id=classroom.id))


# TODO exception handling for student enter classroom w/o active quiz
@classrooms.route("/classroom/enter", methods=['GET', 'POST'])
def enter_classroom():
    """ Student sign-in to classroom. Classroom must have an active quiz. """
    form = EnterClassroomForm()
    if form.validate_on_submit():
        classroom = Classroom.query.filter_by(name=form.room_id.data).first()
        if classroom and classroom.active_quiz:
            print("-------------------------------------------------------------------")
            print("ADDING STUDENT")
            print("-------------------------------------------------------------------")
            student = Student()
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('classrooms.take_quiz', classroom_id=classroom.id,student=student.id))
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
    if current_user.is_authenticated:
        form = ClassroomForm()
        return render_template('classroom.html', title=classroom.name, classroom=classroom, form = form)
    else:
        quiz = classroom.active_quiz
        student=Student()
        return render_template('take_quiz.html', title='TakeQuiz', classroom=classroom, quiz=quiz, student = student)


@classrooms.route("/classroom/<int:classroom_id>/add_quiz", methods=['GET', 'POST'])
@login_required
def add_quiz(classroom_id):
    """
    Add a quiz to a classroom. Can choose an existing quiz that belongs to the user or create a new one.

    Parameters:
            classroom_id (int): the ID of the classroom to add a quiz to
    """
    classroom = Classroom.query.get_or_404(classroom_id)

    # Setting up the form
    form = AddQuizForm()

    # add default option to "create a quiz" in the dropdown
    default_choice = (0, "Create a Quiz")
    quizzes = Quiz.query.filter_by(user_id=current_user.id).filter(~exists().where(and_(assoc.c.quiz_id == Quiz.id, assoc.c.classroom_id == classroom.id)))

    # putting all quizzes of that user in the list
    quiz_list = [(quiz.id, quiz.name) for quiz in quizzes]
    quiz_list.append(default_choice)
    list.reverse(quiz_list)
    form.quiz.choices = quiz_list

    # Handle POST request
    if form.validate_on_submit():
        # get chosen quiz's ID from the form, grab that quiz and attach it to the current classroom
        quiz_id = form.quiz.data
        if quiz_id == 0:
            return redirect(url_for('quizzes.new_quiz', classroom_id=classroom_id))
        else:
            quiz = Quiz.query.filter_by(id=quiz_id).first()
            classroom.added_quizzes.append(quiz)
            db.session.commit()
            flash(u'Quiz \"' + quiz.name + '\" added to \"' + classroom.name + '\"!', 'success')
            return redirect(url_for('classrooms.classroom', classroom_id=classroom.id))

    # Handle GET request
    return render_template('add_quiz.html', title=classroom.name, classroom=classroom, form=form, quiz_list=quiz_list)


# TODO: currently there is a bug where if you click on the nav bar the change gets reset, however, routing to the
#  page separately or refreshing the page does not break the active-ness
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
    classroom_id = request.args.get('classroom_id', None)
    classroom = Classroom.query.get_or_404(classroom_id)
    print("-------------------------------------------------------------------")
    print("DEBUGGING LINE HERE")
    print(classroom)
    print("-------------------------------------------------------------------")
    classroom.active_quiz = quiz_id
    db.session.commit()
   
    form = ClassroomForm()
    return render_template('classroom.html', title=classroom.name, classroom=classroom, form = form)


@classrooms.route("/classroom/remove_active", methods=['GET', 'POST'])
@login_required
def remove_active():
    """ Sets the given quiz to inactive in the current classroom.
    
        Parameters: 
                classroom_id (int): the ID of the classroom to inactive the quiz in
    """
    class_id = request.args.get('classroom_id', None)

    if class_id is None:
        raise Exception('No \'classroom_id\' supplied!')

    classroom = Classroom.query.get(class_id)
    if classroom is None:
        return "No Classroom Found", 404
    classroom.active_quiz = None
    db.session.commit()

    return "set Empty", 200


@classrooms.route("/classroom/remove_quiz/<int:classroom_id>/<int:quiz_id>", methods=['GET', 'POST'])
@login_required
def remove_quiz(classroom_id, quiz_id):
    """ Removes the given quiz from the given classroom.

        Parameters:
                classroom_id (int): the ID of the classroom to remove the quiz from
                quiz_id (int): the ID of the quiz to be removed
    """

    classroom = Classroom.query.get(classroom_id)
    quiz = Quiz.query.get(quiz_id)
    classroom.added_quizzes.remove(quiz)
    db.session.commit()
    flash(u'Quiz Removed!', 'success')
    return redirect(url_for('classrooms.classroom', classroom_id=classroom_id))


@classrooms.route("/classroom/<int:classroom_id>/take", methods=['GET', 'POST'])
def take_quiz(classroom_id):
    """ Student takes the given quiz.

        Parameters:
                classroom_id (int): the ID of the classroom the student is signed in to
    """
    print("-------------------------------------------------------------------")
    print("TAKE QUIZ ARGS")
    args = request.args
    for key in args.keys():
        print(key, " | ", args[key])
        
    if args:
        current_student = Student.query.filter_by(id=int(args['student'])).first()
        
    print("-------------------------------------------------------------------")
    classroom = Classroom.query.get_or_404(classroom_id)
    print("-------------------------------------------------------------------")
    print("DEBUGGING LINE HERE")
    print(classroom.active_quiz)
    print("-------------------------------------------------------------------")
    quiz_id = classroom.active_quiz
    quiz = Quiz.query.get_or_404(quiz_id)
    page = request.args.get('page', 1, type=int)
    questions = Question.query.filter_by(quiz=quiz).paginate(page=page, per_page=1)
    student=Student()
    # dictionary of true and false for each input
    dicts = {}
    
    i = page - 1
    
    for option in quiz.questions[i].answers:
        dicts[option.content] = option.correct

    # gets a list of what the student responded with
    answered = request.form.getlist('studentResponse')
    response = Response(classroom_host_id=classroom.id, quiz_reference=quiz.id, question_num=page)

    for studentResponse in answered:
        result = dicts[studentResponse]
        response = Response.query.filter_by(classroom_host_id=classroom.id, quiz_reference=quiz.id, question_num=page).first()
        if response:
            response.value = studentResponse
            response.correct = dicts[response.value]
        else:
            response = Response(classroom_host_id=classroom.id, quiz_reference=quiz.id, value=studentResponse, question_num=page, correct=result)
            db.session.add(response)
    
    
    
    db.session.commit()
    return render_template('take_quiz.html', classroom=classroom, quiz=quiz, questions=questions, student=current_student)


# query database for all responses from this specific classroom, send lists of right and wrong answers to front
@login_required
@classrooms.route("/classroom/<int:classroom_id>/results", methods=['GET', 'POST'])
def view_results(classroom_id):
    """ View the student responses from the given classroom.

        Parameters: 
                classroom_id (int): the ID of the classroom to retrieve answers from
    """
    print("WRONG ANSWERS-------------")
    sum_wrong = 0
    wrong_answers = Response.query.filter_by(classroom_host_id=classroom_id, correct=False).all()
    for y in wrong_answers:
        sum_wrong += 1
        print(y)

    print(sum_wrong)
    print("RIGHT ANSWERS ----------------")
    sum_right = 0
    correct_responses = Response.query.filter_by(classroom_host_id=classroom_id, correct=True).all()
    for z in correct_responses:
        sum_right += 1
        print(z)
    
    responses = Response.query.filter_by(classroom_host_id=classroom_id).all()
    
    classroom = Classroom.query.filter_by(id=classroom_id).first()
    quiz = Quiz.query.filter_by(id=classroom.active_quiz).first()
    students = {response.student_id: responses for response in responses}

    print("-------------------------------------------------------------------")
    print("DEBUGGING LINE HERE")
    print("-------------------------------------------------------------------")
    print(quiz.questions)
    print(len(quiz.questions))
    print(type(quiz.questions))

    return render_template('classroom_results.html', title='results of quiz', rightAnswers=correct_responses,
                           wrongAnswers=wrong_answers, sumRight=sum_right, sumWrong=sum_wrong, classroomid=classroom_id, responses=responses, quiz=quiz, students=students)


#Answers of each student 
@classrooms.route("/classroom/received_answer", methods=['GET', 'POST'])
def received_answer():

    args = request.args
    
    # Current quiz, questions, answer
    quiz = Quiz.query.filter_by(id = args['quiz_id']).first()
    questions = Question.query.filter_by(quiz = quiz).paginate(page=int(args['page_num']), per_page = 1)
    current_answer = Answer.query.filter_by(id= args['answer_id']).first()
    current_question = Question.query.filter_by(id = current_answer.question_id).first()
    current_student = Student.query.filter_by(id= args['student_id']).first()
    print("-------------------------------------------------------------------")
    print("Received value is ")
    print(request.args)

    print("-------------------------------------------------------------------")
    

    
    


    
    # Creating the response object of the user
    
    response = Response(
        classroom_host_id = args['classroom_id'],
        student_id = current_student.id,
        quiz_reference = args['quiz_id'],
        question_num = args['page_num'],
        value = args['value'],
        correct = current_answer.correct,
        answer_reference = args['answer_id']
    )

    

    
    # Delete answer if user unclicks the button they selected.    
    if current_question.category  != 'True-False':
        regular_responses(current_answer,response)
    else:
        tf_responses(current_answer, response, current_question)

    #update database
    db.session.commit()
 
    return "nice!"


@classrooms.route("/classroom/<int:classroom_id>/edit_classroom_name", methods=['GET','POST'])
def edit_classroom_name(classroom_id):
    args = request.args
    print(args)
    classroom = Classroom.query.filter_by(id=classroom_id).first()
    form = ClassroomForm()
    if form.validate_on_submit:
        classroom.name = args['name']
        db.session.commit()
   
    
    return render_template('classroom.html', title=classroom.name, classroom=classroom, form = form)

@classrooms.route("/account/delete_classroom")
@login_required
def delete_classroom():
    """ Delete the specified classroom owned by the current user. 
    
        Parameters:
                classroom_id (int): the ID of the classroom to be deleted.
    """
    classroom_id = request.args.get('classroom_id', None)
    classroom = Classroom.query.filter_by(id=classroom_id).first()
    db.session.delete(classroom)
    db.session.commit()
    db.session.flush()
    flash(u'Classroom Removed!', 'success')
    return "deleted classroom", 200

def regular_responses(current_answer,response):

    """
    if the response is in the database:
        delete that response
    else:
        add that response to the database
    """
    
    response_in_the_db = Response.query.filter_by(answer_reference =response.answer_reference , question_num =response.question_num).first()
    if response_in_the_db is None:
        db.session.add(response)
    else:
        db.session.delete(response_in_the_db)

def tf_responses(current_answer, response, current_question):
    # for answer in current_question.answers:
    """
    if the answer is in the database:
        is it identical to the current answer? (case 3)
            don't do anything
        is it different from the current answer? (case 2)
            delete this answer
            add the response
    else:
        add the response
    """

    for answer in current_question.answers:
    
        response_in_the_db = Response.query.filter_by(answer_reference =answer.id, question_num =response.question_num).first()
        if response_in_the_db is None:
            db.session.add(response)
        else:
            db.session.delete(response_in_the_db)


            


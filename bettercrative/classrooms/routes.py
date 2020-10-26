from flask import (render_template, url_for, flash,
                   redirect, Blueprint,session,
                   request, make_response, jsonify)
from flask_login import current_user, login_required
from sqlalchemy import exists, and_
from collections import defaultdict
from bettercrative import db
from bettercrative.users.routes import users, quizzes
from bettercrative.quizzes.routes import quizzes, quiz
from bettercrative.classrooms.response_handling import *
from bettercrative.classrooms.forms import ClassroomForm, EnterClassroomForm, AddQuizForm, StudentForm, SetActiveForm
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
            student = Student(quiz_reference = classroom.active_quiz)
            db.session.add(student)
            db.session.commit()
            if classroom.username_required:    
                print("-------------------------------------------------------------------")
                print("STUDENTS NEED TO PUT A USERNAME HERE")
                print("-------------------------------------------------------------------")   
                return redirect(url_for('classrooms.student_name', classroom_id = classroom.id, student=student.id))
            else:   
                return redirect(url_for('classrooms.take_quiz', classroom_id=classroom.id,student=student.id))
        else:
            flash(u'A classroom does not exist with that name. Please try again.', 'danger')
    return render_template('enter_classroom.html', title='get in chief', form=form)

@classrooms.route('/classroom/student_name', methods=['GET','POST'])
def student_name():
    args = request.args

    if 'classroom_id' not in args and 'student' not in args:
        raise('classroom_id key and student key not found')

    form = StudentForm()
  
    
    if form.validate_on_submit():
        
        student = Student.query.filter_by(id=int(args['student'])).first()
        student.name = form.name.data
        db.session.commit()
        return redirect(url_for('classrooms.take_quiz', classroom_id= args['classroom_id'], student= student.id))
    return render_template('student_name.html', form = form, classroom_id = args['classroom_id'], student= args['student'])

@classrooms.route("/classroom/<int:classroom_id>", methods=['GET', 'POST'])
def classroom(classroom_id):
    """ 
    Display the given classroom's dashboard.

    Parameters:
            classroom_id (int): the ID of the classroom to display
    """
    classroom = Classroom.query.get_or_404(classroom_id)
    activeform = SetActiveForm()
    
    if current_user.is_authenticated:
        form = ClassroomForm()
        # this is so the "view results" button only shows up if there's something to view
        has_responses = classroom.active_quiz is not None and len(Response.query.filter_by(quiz_reference=classroom.active_quiz).all()) > 0
        return render_template('classroom.html', title=classroom.name, classroom=classroom, form=form, has_responses=has_responses, activeform=activeform)
    else:
        quiz = classroom.active_quiz
        student = Student()

        return render_template('take_quiz.html', title='TakeQuiz', classroom=classroom, quiz=quiz, student=student)


def is_complete(quiz):
    """
    Checks a quiz for completeness. A quiz is complete if:
    - there is at least one question (one is added by default on quiz creation)
    - every question has a category
    - every question has content
    - for multiple choice, every answer has content and at least one of them is marked correct
    :param quiz: the quiz to check
    :return: true if quiz is complete
    """

    complete = True
    # the quiz must have at least one question
    if quiz.questions is None:
        complete = False
        print("no questions")
    else:
        for question in quiz.questions:
            # all questions must have content and a category
            if question.category is None or question.content is None:
                complete = False
                print("question % 2d either has no category or has no content" % question.index)
                break
            if question.category == 'Multiple Choice':
                has_correct_answer = False
                for answer in question.answers:
                    # all answers must have content
                    if answer.content is None:
                        complete = False
                        print("answer %2d to question %2d has no content" % (answer.index, question.index))
                        break
                    if answer.correct:
                        has_correct_answer = True
                # at least one answer must be correct
                if not has_correct_answer:
                    complete = False
                    print("question %2d has no correct answers" % question.index)
                    break
            if question.category == 'True-False':
                # true/false questions must be either true or false
                if not question.answers[0].correct and not question.answers[1].correct:
                    complete = False
                    print("question %2d has not been marked true or false" % question.index)
                    break
    return complete


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

    # putting all quizzes of that user (that have names set) in the list
    quiz_list = [(quiz.id, quiz.name) for quiz in quizzes if quiz.name]
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
@classrooms.route("/classroom/<int:classroom_id>/<int:quiz_id>/set_active", methods=['GET', 'POST'])
@login_required
def set_active(classroom_id, quiz_id):
    """
    Sets the given quiz as active in the classroom it's in.
    
    Parameters: 
            quiz_id (int): the ID of the quiz to set active
            classroom_id (int): the ID of the classroom to make it active in
    """
    
    classroom = Classroom.query.get_or_404(classroom_id)
    quiz = Quiz.query.get_or_404(quiz_id)
    
    activeform = SetActiveForm()
    
    if is_complete(quiz) and activeform.validate_on_submit():
        
        classroom.username_required = activeform.require_usernames.data
        classroom.generate_qr = activeform.generate_qr.data
        classroom.active_quiz = quiz_id
        db.session.commit()
        flash(u'Quiz \"' + quiz.name + '\" is now active in \"' + classroom.name + '\"!', 'success')
    else:
        print("got here")
        flash(u'Quiz \"' + quiz.name + '\" is incomplete. Please check all questions have content and sufficient answers.', 'danger')

    return redirect(url_for('classrooms.classroom', classroom_id=classroom.id, activeform=activeform))


@classrooms.route('/classroom/unset_and_edit', methods=['POST'])
@login_required
def unset_and_edit():
    form = request.form
    if 'quiz_id' not in form:
        raise('quiz_id key is not found')
    
    quiz = Quiz.query.filter_by(id=int(form['quiz_id'])).first()
    quiz.unset()
    return redirect( url_for('quizzes.quiz', quiz_id=quiz.id))


@classrooms.route('/classroom/unset', methods = ['POST'])
@login_required
def unset():
   
    form = request.form
    if 'quiz_id' not in form and 'classroom_id' not in form:
        raise('quiz_id key is not found')
    
    quiz = Quiz.query.filter_by(id = int(form['quiz_id'])).first()
    quiz.unset()

    return redirect( url_for('users.quizzes'))


@classrooms.route("/classroom/<int:classroom_id>/remove_active", methods=['GET', 'POST'])
@login_required
def remove_active(classroom_id):
    """ Sets the given quiz to inactive in the current classroom.
    
        Parameters: 
                classroom_id (int): the ID of the classroom to inactive the quiz in
    """
    if classroom_id is None:
        raise Exception('No \'classroom_id\' supplied!')

    classroom = Classroom.query.get(classroom_id)
    if classroom is None:
        return "No Classroom Found", 404
    classroom.active_quiz = None
    db.session.commit()

    return redirect(url_for('classrooms.classroom', classroom_id=classroom.id))


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


@classrooms.route("/classroom/correct_answer", methods=['GET', 'POST'])
def correct_answer():
    args = request.args

    if 'response_id' not in args:
        raise KeyError('response_id key not found')
    if 'change_to' not in args:
        raise ValueError('no grade supplied to change this answer to')

    response = Response.query.filter_by(id=int(args['response_id'])).first()
    change_to = args['change_to']

    if change_to == "incorrect":
        response.correct = False
    elif change_to == "correct":
        response.correct = True
    elif change_to == "reset":
        response.correct = None

    db.session.commit()
    return "graded by teacher", 200


@classrooms.route("/classroom/<int:classroom_id>/take", methods=['GET', 'POST'])
def take_quiz(classroom_id):
    """ Student takes the given quiz.

        Parameters:
                classroom_id (int): the ID of the classroom the student is signed in to
    """

    args = request.args
    
    # Things to Render: classroom, quiz, Paginate the questions , student
    classroom = Classroom.query.get_or_404(classroom_id)
    quiz_id = classroom.active_quiz
    quiz = Quiz.query.get_or_404(quiz_id)
    page = request.args.get('page', 1, type=int)
    questions = Question.query.filter_by(quiz=quiz).order_by('index').paginate(page=page, per_page=1)
    
    if 'teacher' in args:
        teacher = args['teacher']
    else:
        teacher = False
    
    if 'student' not in args:
        current_student = Student(quiz_reference=quiz_id)
        db.session.add(current_student)
        db.session.commit()
        return redirect(url_for('classrooms.take_quiz', quiz=quiz, classroom_id=classroom.id, student=current_student.id, teacher=True))

    else:
        current_student = Student.query.filter_by(id=int(args['student'])).first()
    return render_template('take_quiz.html', classroom=classroom, quiz=quiz, questions=questions, student=current_student, teacher=teacher)


@classrooms.route("/classroom/teacher_take_quiz", methods=['GET', 'POST'])
@login_required
def teacher_take_quiz():
    args = request.args
    student = Student.query.filter_by(id = args['student_id']).first()
    db.session.delete(student)
    db.session.commit()
    
    return redirect(url_for('main.home'))


@classrooms.route("/classroom/process_take_quiz", methods = ['GET', 'POST'])
def process_take_quiz():
    args = request.args
    if args['teacher'] == 'True':
        return redirect(url_for('classrooms.teacher_take_quiz', student_id=args['student_id']))
    else:
        return redirect(url_for('main.home'))


# query database for all responses from this specific classroom, send lists of right and wrong answers to front
@login_required
@classrooms.route("/classroom/<int:classroom_id>/results", methods=['GET', 'POST'])
def view_results(classroom_id):
    """ View the student responses from the given classroom.

        Parameters: 
                classroom_id (int): the ID of the classroom to retrieve answers from
                quiz_id (int): the ID of the quiz to retrieve answers from
    """

    classroom = Classroom.query.filter_by(id=classroom_id).first()

    totalResponses = {}
    responses = defaultdict(list)
    
    # For every quiz, store that quizzes info 
    for quiz in classroom.added_quizzes:
        for student in quiz.students:
            for response in student.responses:
                responses[(student.id, response.question.id)].append(response)
            totalResponses[quiz.id] = responses


    return render_template('classroom_results.html', title='results of quiz',totalResponses=totalResponses, classroom=classroom)


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
    

    # Creating the response object of the user
    
    response = Response(
        classroom_host_id = args['classroom_id'],
        student_id = current_student.id,
        quiz_reference = args['quiz_id'],
        question_id = current_answer.question_id,
        question_num = args['page_num'],
        value = args['value'],
        correct = current_answer.correct,
        answer_reference = args['answer_id']
    )

    
    

    
    # Delete answer if user unclicks the button they selected.    
    if current_question.category  == 'Multiple Choice':
        regular_responses(current_student,current_answer,response)
    elif current_question.category == 'True-False':
        tf_responses(current_student,current_answer, response, current_question)
    elif current_question.category == 'Short Answer':
        sa_response(current_student,current_answer,response, current_question)
    else:
        coding_response(current_student, current_answer, response, current_question)
    
    #update database
    db.session.commit()
    
    
    
    return "nice!"


@classrooms.route("/classroom/<int:classroom_id>/edit_classroom_name", methods=['GET','POST'])
def edit_classroom_name(classroom_id):
    args = request.args
    classroom = Classroom.query.filter_by(id=classroom_id).first()
    form = ClassroomForm()
    activeform = SetActiveForm()
    if form.validate_on_submit:
        classroom.name = args['name']
        db.session.commit()
   
    
    return render_template('classroom.html', title=classroom.name, classroom=classroom, form = form, activeform = activeform)

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

@classrooms.route("/calculate_chart_data", methods=['GET'])
def calculate_chart_data():
    """ Calculates chart data and labels, then sends a GET request
        classroom_id: classroom that the students responses are being taken from
    """

    quiz_id = request.args.get('quiz_id', None)
    class_id = request.args.get('class_id', None)
    chart_type = request.args.get('chart_type', None)
    print(chart_type)

    # get all students that answeres this quiz within this classroom

    quiz = Quiz.query.filter_by(id=quiz_id).first()
    classroom = Classroom.query.filter_by(id=class_id).first()

    if classroom is None:
        return ('No Classroom Found'), 404

    if quiz is None:
        return "No Quiz Found", 404


    student_ids = classroom.get_id_list(quiz.students)

    chart_labels = []
    chart_data = []
    num_questions = len(quiz.questions)
    data = [chart_labels, chart_data, num_questions]
    if(chart_type=='doughnut'):
        # each label is a question
        for question in quiz.questions:
            chart_labels.append(question.name)
            chart_data.append(0)
        # count the number correct for each question
        for studentid in student_ids:
            student = Student.query.filter_by(id=studentid).first()
            for response in student.responses:
                if response.correct:
                    chart_data[response.question_num-1] += 1
    else:
        numCorrect = 0
        # for each student, calculate their score (for now every question is worth one point)
        for studentid in student_ids:
            chart_labels.append("Student#"+str(studentid))
            student = Student.query.filter_by(id=studentid).first()
            for response in student.responses:
                if response.correct:
                    numCorrect = numCorrect + 1
            chart_data.append(numCorrect)
            print(numCorrect)
            numCorrect = 0

    return jsonify(data), 200

@classrooms.route("/calculate_question_chart_data", methods=['GET'])
def calculate_question_chart_data():
    """ Calculates chart data and labels, then sends a GET request
        classroom_id: classroom that the students responses are being taken from
    """

    quiz_id = request.args.get('quiz_id', None)
    class_id = request.args.get('class_id', None)
    question_id = request.args.get('question_id', None)

    # get all students that answeres this quiz within this classroom

    quiz = Quiz.query.filter_by(id=quiz_id).first()
    classroom = Classroom.query.filter_by(id=class_id).first()
    question = Question.query.filter_by(id=question_id).first()

    if classroom is None:
        return 'No Classroom Found', 404

    if quiz is None:
        return "No Quiz Found", 404

    if question is None:
        return "No Question Found", 404

    student_ids = classroom.get_id_list(quiz.students)

    chart_labels = []
    chart_data = []
    num_questions = len(quiz.questions)
    data = [chart_labels, chart_data, num_questions]
    
    # each label is a question
    for answer in question.answers:
        chart_labels.append(answer.content)
        chart_data.append(0)
    # count the number correct for each question
    for studentid in student_ids:
        student = Student.query.filter_by(id=studentid).first()
        for response in student.responses:
            if(response.question_id == int(question_id)):
                answer = Answer.query.filter_by(id=response.answer_reference).first()
                chart_data[answer.index] += 1
    return jsonify(data), 200

# changes active quiz for result page
@classrooms.route("/change_active_result", methods=['GET', 'POST'])
def change_active_result():
    """
        q_id: quiz id
        c_id: classroom id
    """
    c_id = request.args.get("c_id", None)
    q_id = request.args.get("q_id", None)
    
    classroom = Classroom.query.filter_by(id=c_id).first()
    classroom.active_result = q_id
    db.session.commit()
    return "succsessful change of active result quiz",200

from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, Response)
from flask_login import current_user, login_required
from bettercrative import db
from bettercrative.classrooms.routes import classroom
from bettercrative.models import Quiz, Classroom, User, Question, Answer
from bettercrative.quizzes.forms import QuizForm, QuestionForm, AnswerForm
from datetime import date

quizzes = Blueprint('quizzes', __name__)


@quizzes.route("/quiz/new", methods=['GET', 'POST'])
@login_required
def new_quiz(classroom_id=None):
    """ Create a new quiz.

        Optional parameters:
            classroom_id (int): ID for a classroom. If supplied, add this new quiz to that classroom.
    """
    form = QuizForm()

    
    if form.validate_on_submit():
        quiz = Quiz(
            name=form.name.data,
            date_created=date.today(),
            owner=current_user
        )
        # for testing purposes
        # default_question = Question(quiz_id=quiz.id)
        # quiz.questions.append(default_question)
        # a1 = Answer(question_id=default_question.id)
        # default_question.answers.append(a1)
        #default_question.answers.append(("first answer", "True"))
        db.session.add(quiz)
       
        db.session.commit()
        flash(u'New quiz \"' + quiz.name + '\" created!', 'success')
        if classroom_id:
            classroom.added_quizzes.append(quiz)
        return redirect(url_for('quizzes.quiz', quiz_id=quiz.id))
    return render_template('create_quiz.html', title='New Quiz', form=form)


@quizzes.route("/quiz/<int:quiz_id>")
@login_required
def quiz(quiz_id):
    """ Display the given quiz. Teacher's editing view. 

        Parameters: 
                quiz_id (int): The ID of the quiz to display.
    """
    form = QuestionForm()
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz.html', title=quiz.name, quiz=quiz, form = form)


@quizzes.route("/quiz/add")
@login_required
def add_question():
    """ Add a blank question to the given quiz.

        Parameters: 
                quiz_id (int): The ID of the quiz to add the question to.
    """
    print("adding Question")
    quiz_id = request.args.get('quiz_id', None)
    if quiz_id is None:
        return "No quiz id!", 400

    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz is None:
        return "Quiz not found!", 404

    question = Question(quiz_id=quiz_id)
    if question is None:
        return "Question creation fail - If you see this something is very wrong", 500

    sql = "select count(question.id) from question, quiz where quiz.id = question.quiz_id"
    numQuestions = db.session.execute(sql).first()[0] + 1

    question.name = "Question " + str(numQuestions)
    if question.name is None:
        return "Question name creation fail, something went wrong with counting the quiz questions!", 500
    print(numQuestions);

    db.session.add(question)

    quiz.questions.append(question)

    # load new question data

    db.session.commit()
    print("success")
    return "addedQuestion - Success", 200

@quizzes.route("/quiz/remove")
@login_required
def remove_question():
    """ Remove a question from the given quiz.
        Parameters: 
                question_id (int): the ID of the question to be removed.
                quiz_id (int): the quiz to remove the question from.
    """
    print("Removing Question")
    question_id = request.args.get('question_id', None)

    if question_id is None:
        return "No question id!", 400

    question = Question.query.filter_by(id=question_id).first()
    if question is None:
        return "Question not found!", 404
    print(f'question: {question}')

    quiz = Quiz.query.filter_by(id=question.quiz_id).first()
    if quiz is None:
        return "oops fuk", 500

    if(quiz is not None):
        quiz.questions.remove(question)

    print(f'removed')
    db.session.flush()
    
    db.session.delete(question)

    print(f'deleted')

    # load new question data

    db.session.commit()
    return "lit", 200

@quizzes.route("/quiz/shift_question")
@login_required
def shift_question():
    """ Remove a question from the given quiz.
        Parameters: 
                question_id (int): the ID of the question to be removed.
                quiz_id (int): the quiz to remove the question from.
    """
    question_id = request.args.get('question_id', None)
    direction = request.args.get('direction', None)
    print("Shifting Question " + direction)

    if direction is None:
        return "No direction given!", 400
    if question_id is None:
        return "No question id!", 400

    question = Question.query.filter_by(id=question_id).first()
    if question is None:
        return "Question not found!", 404

    quiz = Quiz.query.filter_by(id=question.quiz_id).first()
    if quiz is None:
        return "oops fuk", 500

    # target is the question that we want to swap in a direction
    targetIdx = quiz.questions.index(question)

    if(direction == "left"):
        destinationIdx = targetIdx - 1
    else:
        destinationIdx = targetIdx + 1

    quiz.questions.insert(destinationIdx, quiz.questions.pop(targetIdx))
    
    # load new question data

    db.session.commit()
    return "lit", 200

@quizzes.route("/quiz/add_content", methods = ['GET', 'POST'])
@login_required
def add_question_content():

    """ Adds question content within the question in the quiz.
        Paramters:
            question_id (int): the ID of the question for content to be added.
    """
    print(request.args)
    question_id = request.args.get('question_id',None)

    #Find the current question and then update it's value by showing the form
    current_question = Question.query.filter_by(id = question_id).first()
    current_quiz = current_question.quiz_id

    form = QuestionForm()
    
    #handle POST request
    if form.validate_on_submit():
        flash(f'IT VALIDATED')
        current_question.content = form.content.data
        current_question.category = form.category.data
        current_question.answers = form.answers.data
    
        db.session.commit()
        return redirect(url_for('quizzes.current_quiz'))
    #handle GET Request
    print('rendering template')
    return render_template('quiz.html', title = 'question', quiz = current_quiz , form = form)



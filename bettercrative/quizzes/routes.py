from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, Response)
from flask_login import current_user, login_required
from bettercrative import db
from bettercrative.classrooms.routes import classroom
from bettercrative.models import Quiz, Classroom, User, Question
from bettercrative.quizzes.forms import QuizForm

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
            question_content=form.question_content.data, 
            owner=current_user
        )
        db.session.add(quiz)
        # add each answer to the question
        for answer in form.question_answers.data:
            new_answer = Answer(**answer)
            quiz.question_answers.append(new_answer)
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
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz.html', title=quiz.name, quiz=quiz)


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

    db.session.add(question)

    quiz.questions.append(question)
    
    #load new question data

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


    quiz.questions.remove(question)

    print(f'removed')

    db.session.delete(question)
    
    print(f'deleted')

    #load new question data

    db.session.commit()
    return "lit", 200

from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import current_user, login_required
from wtforms import FormField, FieldList

from bettercrative import db
from bettercrative.models import Quiz, Question, Answer, Classroom
from bettercrative.quizzes.forms import QuizForm, QuestionForm, AnswerForm, QuestionFormOverall

quizzes = Blueprint('quizzes', __name__)


@quizzes.route("/quiz/new/", defaults={'classroom_id': None}, methods=['GET', 'POST'])
@quizzes.route("/quiz/new/<int:classroom_id>", methods=['GET', 'POST'])
@login_required
def new_quiz(classroom_id):
    """ Create a new quiz.

        Optional parameters:
            classroom_id (int): ID for a classroom. If supplied, add this new quiz to that classroom.
    """
    form = QuizForm()

    if form.validate_on_submit():
        quiz = Quiz(
            name=form.name.data,
            owner=current_user
        )
        first_question = Question(quiz_id=quiz.id, name="Question 1")
        db.session.add(first_question)
        quiz.questions.append(first_question)
        db.session.add(quiz)

        db.session.commit()
        flash(u'New quiz \"' + quiz.name + '\" created!', 'success')
        quiz.active = first_question.id
        print(quiz.active)
        if classroom_id:
            classroom = Classroom.query.get(classroom_id)
            classroom.added_quizzes.append(quiz)
            db.session.commit()
            flash(u'Quiz \"' + quiz.name + '\" added to \"' + classroom.name + '\"!', 'success')
            return redirect(url_for('classrooms.classroom', classroom_id=classroom_id))
        return redirect(url_for('quizzes.quiz', quiz_id=quiz.id))
    return render_template('create_quiz.html', title='New Quiz', form=form)


@quizzes.route("/quiz/<int:quiz_id>")
@login_required
def quiz(quiz_id):
    """ Display the given quiz. Teacher's editing view. 

        Parameters: 
                quiz_id (int): The ID of the quiz to display.
    """
    qzform = QuizForm()
    form = QuestionFormOverall()

    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz.html', title=quiz.name, quiz=quiz, qzform=qzform, form=form)


@quizzes.route("/quiz/edit-name/<int:quiz_id>", methods=['GET', 'POST'])
@login_required
def edit_quiz_name(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    print("editing name")

    qzform = QuizForm()
    form = QuestionFormOverall()

    if qzform.validate_on_submit():
        print("Validated")
        quiz.name = qzform.name.data
        db.session.commit()
        return redirect(url_for('quizzes.quiz', quiz_id=quiz_id))
    return render_template('quiz.html', title=quiz.name, quiz=quiz, qzform=qzform, form=form)


@quizzes.route("/quiz/add")
@login_required
def add_question():
    """ Add a blank question to the given quiz.

        Parameters: 
                quiz_id (int): The ID of the quiz to add the question to.
    """

    # Get the id from the GET request
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

    question.name = "Question "
    if question.name is None:
        return "Question name creation fail, something went wrong with counting the quiz questions!", 500

    db.session.add(question)

    quiz.questions.append(question)

    # load new question data

    db.session.commit()

    quiz.active = question.id

    question.name += str(question.index + 1)

    db.session.commit()

    printQuestion(question)
    print("success")
    return "addedQuestion - Success", 200


@quizzes.route("/quiz/add-answer")
@login_required
def add_answer():
    """ Add a blank answer to the given question.

        Parameters:
                question_id (int): The ID of the question to add the answer to.
    """
    print("adding Answer")
    question_id = request.args.get('question_id', None)
    if question_id is None:
        return "No quiz id!", 400

    question = Question.query.get_or_404(question_id)
    if question is None:
        return "Question not found!", 404

    answer = Answer(question_id=question_id)
    if answer is None:
        return "Answer creation fail - If you see this something is very wrong", 500

    db.session.add(answer)

    question.answers.append(answer)

    # load new answer data

    db.session.commit()
    print("success")
    return redirect(url_for('quizzes.quiz', quiz_id=question.quiz_id))


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

    if quiz is not None:
        quiz.questions.remove(question)

    # setting active question
    current_active_question = quiz.active
    if current_active_question == question.id:
        current_active_question = quiz.questions[-1].id

    print(f'removed')
    db.session.flush()

    db.session.delete(question)

    print(f'deleted')

    db.session.commit()

    quiz.active = current_active_question

    db.session.flush()
    db.session.commit()
    return "lit", 200


@quizzes.route("/quiz/remove-answer")
@login_required
def remove_answer():
    """ Remove an answer from the given question.
        Parameters:
                answer_id (int): the ID of the answer to be removed.
    """
    print("Removing Answer")
    answer_id = request.args.get('answer_id', None)

    if answer_id is None:
        return "No answer id!", 400

    answer = Answer.query.filter_by(id=answer_id).first()
    if answer is None:
        return "Question not found!", 404
    print(f'question: {answer}')

    question = Question.query.filter_by(id=answer.question_id).first()
    if question is None:
        return "oops fuk", 500

    question.answers.remove(answer)
    print(f'removed')
    db.session.flush()

    print(f'deleted')

    # load new answer data

    db.session.commit()
    return "lit", 200


@quizzes.route("/quiz/shift_question")
@login_required
def shift_question():
    """ shift a question to a given location.
        Parameters: 
                question_id (int): the ID of the question to be removed.
                direction (String): direction to shift
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

    if direction == "left":
        destinationIdx = targetIdx - 1
    else:
        destinationIdx = targetIdx + 1

    quiz.questions.insert(destinationIdx, quiz.questions.pop(targetIdx))

    # load new question data

    db.session.commit()
    return "lit", 200


@quizzes.route("/quiz/set_question_type")
@login_required
def set_question_type():
    question_id = request.args.get('question_id', None)
    qtype = request.args.get('qtype', None)
    print(question_id)
    current_question = Question.query.filter_by(id=question_id).first()
    current_question.category = qtype
    print(current_question)
    quiz = Quiz.query.filter_by(id=current_question.quiz_id).first()
    print(quiz)
    if current_question.category == 'Multiple Choice':
        for i in range(4):
            current_question.answers.append(Answer())
    if current_question.category == 'True-False':
        true = Answer(question_id=question_id, content='True', index=0)
        false = Answer(question_id=question_id, content='False', index=1)
        db.session.add(true)
        db.session.add(false)

    db.session.commit()
    return redirect(url_for('quizzes.quiz', quiz_id=quiz.id))


@quizzes.route("/quiz/question/<int:question_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz = question.quiz

    form = QuestionFormOverall()
    qzform = QuizForm()

    if form.validate_on_submit():
        question.content = form.question_form.content.data
        for i, aform in enumerate(form.answer_form):
            question.answers[i].content = aform.content.data
            question.answers[i].correct = aform.correct.data

        db.session.commit()
        flash(u'Successfully updated question!', 'success')
        return redirect(url_for('quizzes.quiz', quiz_id=quiz.id))
    return render_template('quiz.html', quiz=quiz, form=form, qzform=qzform)


@quizzes.route("/quiz/change_active_question")
@login_required
def change_active_question():
    """ Sets the active question of a provided quiz to the provided question
        Parameters:
            question_id (int): the ID of the question
            quiz (int): the ID of the quiz
    """
    question_id = request.args.get('question_id', None)
    quiz_id = request.args.get('quiz_id', None)

    question = Question.query.filter_by(id=question_id).first()
    if question is None:
        return "oops fuk", 500

    quiz = Quiz.query.filter_by(id=quiz_id).first()
    if quiz is None:
        return "oops fuk", 500

    quiz.active = question.id

    db.session.commit()
    return "lit", 200


"""
-------------------------------------------------------------------
DEBUGGING FUNCTIONS SECTION [REMOVE LATER]
-------------------------------------------------------------------
"""


def printQuestion(question: Question) -> None:
    print(f'question id: {question.id} | question name: {question.name} | \
        question content: {question.content} | question category: {question.category} \
            | quiz_id(FOREIGN KEY): {question.quiz_id} | \
                question index : {question.index}')

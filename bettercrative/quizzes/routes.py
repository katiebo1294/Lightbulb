from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import current_user, login_required
from wtforms import FormField, FieldList, RadioField

from bettercrative import db
from bettercrative.models import Quiz, Question, Answer, Classroom
from bettercrative.quizzes.forms import QuizForm, QuestionForm, AnswerForm, QuestionFormOverall, QuestionFormOverallSA, QuestionFormOverallTF

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
    
    form = QuestionFormOverall()
    
    qzform = QuizForm()
    quiz = Quiz.query.get_or_404(quiz_id)
    saform = QuestionFormOverallSA()
    tfform = QuestionFormOverallTF()
    return render_template('quiz.html', title=quiz.name, quiz=quiz, qzform=qzform, form=form, saform = saform,tfform=tfform)


@quizzes.route("/quiz/edit-name/<int:quiz_id>", methods=['GET', 'POST'])
@login_required
def edit_quiz_name(quiz_id):
    
    quiz = Quiz.query.get_or_404(quiz_id)
    
    

    qzform = QuizForm()
    form = QuestionFormOverall()
    
    if qzform.validate_on_submit():
        
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
        return "No quiz found under that id", 500

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
    return "Removed Question", 200


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
        return "No question found under that id", 500

    question.answers.remove(answer)
    print(f'removed')
    db.session.flush()

    print(f'deleted')

    # load new answer data

    db.session.commit()
    return "Removed answer", 200


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
        return "No quiz found under that quiz id", 500

    # target is the question that we want to swap in a direction
    targetIdx = quiz.questions.index(question)

    if direction == "left":
        destinationIdx = targetIdx - 1
    else:
        destinationIdx = targetIdx + 1

    quiz.questions.insert(destinationIdx, quiz.questions.pop(targetIdx))

    # load new question data

    db.session.commit()
    return "Shifted question", 200


@quizzes.route("/quiz/set_question_type", methods=['GET','POST']) 
@login_required
def set_question_type():
    question_id = request.args.get('question_id', None)
    qtype = request.args.get('qtype', None)
    
    current_question = Question.query.filter_by(id=question_id).first()
    current_question.category = qtype
    
    quiz = Quiz.query.filter_by(id=current_question.quiz_id).first()
    
    
    if current_question.category == 'Multiple Choice':
        for i in range(4):
            current_question.answers.append(Answer())
    elif current_question.category == 'True-False':
        true = Answer(question_id=question_id, content='True', index=0)
        false = Answer(question_id=question_id, content='False', index=1)
        db.session.add(true)
        db.session.add(false)
    elif current_question.category == 'Short Answer':
        short_answer = Answer(question_id=question_id, index = 0)
        db.session.add(short_answer)
        db.session.commit()
        print(f'q type is {current_question.category}')
        print('REDIRECTING WITH FORM')
        return redirect(url_for('quizzes.quiz', quiz_id=quiz.id, question_type='Short Answer'))

    db.session.commit()
    print("-------------------------------------------------------------------")
    print("done w/ setting q type")
    print("-------------------------------------------------------------------")
    return redirect(url_for('quizzes.quiz', quiz_id=quiz.id))


@quizzes.route("/quiz/question/<int:question_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz = question.quiz
    qzform = QuizForm()

    if question.category == 'Short Answer':
        
        form = QuestionFormOverallSA()
        
        if form.validate_on_submit():
            received_form = request.form
            print(request.form)
            question.content = received_form['question_form-content']
            received_answer = received_form['answer_form-content']
            db.session.add(question)
            answer = question.answers[0]
            answer.content = received_answer
            answer.correct = True
            db.session.add(answer)
            db.session.commit()
            return redirect(url_for('quizzes.quiz', quiz_id=quiz.id))

    else:
        if question.category == 'True-False':

            form = QuestionFormOverallTF()
            #form validation
            if form.validate_on_submit():
                #getting the form
                received_form = request.form
                correct_answer = 0
                #getting the correct answer and new question name
                for key in received_form.keys():
                    if('answer_form' and 'correct' in key):
                        correct_answer=bool(int(received_form[key]))
                        new_content_name = received_form['question_form-content']
                for answer in question.answers:
                    if answer.content == str(correct_answer):
                        answer.correct = True
                        db.session.add(answer)
                    else:
                        answer.correct = False
                        db.session.add(answer)
                
                question.content = new_content_name
                db.session.add(question)
                db.session.commit()
                flash(u'Successfully updated question!', 'success')
                return redirect(url_for('quizzes.quiz', quiz_id = quiz.id))
        else:
            form = QuestionFormOverall()
            if form.validate_on_submit():
                if form.question_form.content.data:
                    question.content = form.question_form.content.data
                for i, aform in enumerate(form.answer_form):
                    if aform.content.data:
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
        return "No question found under that id", 500

    quiz = Quiz.query.filter_by(id=quiz_id).first()
    if quiz is None:
        return "No quiz found under that id", 500

    quiz.active = question.id

    db.session.commit()
    return "active question changed", 200

@quizzes.route("/account/delete_quiz")
@login_required
def delete_quiz():
    """ Delete the specified quiz owned by the current user. 
    
        Parameters:
                quiz_id (int): the ID of the quiz to be deleted.
    """
    quiz_id = request.args.get('quiz_id', None)
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    #remove active quiz from classroom if the quiz removed is the active quiz
    
    for classroom in quiz.classroom_hosts:
        if classroom.active_quiz == quiz_id:
            classroom.active_quiz = None
            db.session.add(classroom)
    
    db.session.delete(quiz)

    

    db.session.commit()
    db.session.flush()
    flash(u'Quiz Removed', 'success')
    return "Quiz removed", 200



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

def form_errors(form):
    print("-------------------------------------------------------------------")
    print("Form Errors HERE")
    print(form.errors)
    print("-------------------------------------------------------------------")
def printQuestion(question: Question) -> None:
    print(f'question id: {question.id} | question name: {question.name} | \
        question content: {question.content} | question category: {question.category} \
            | quiz_id(FOREIGN KEY): {question.quiz_id} | \
                question index : {question.index}')

def form_errors(form):
    print("-------------------------------------------------------------------")
    print("Form Errors HERE")
    print(form.errors)
    print("-------------------------------------------------------------------")
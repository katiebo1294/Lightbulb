from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, Response)
from flask_login import current_user, login_required
from bettercrative import db
from bettercrative.classrooms.routes import classroom
from bettercrative.models import Quiz, Answer, Classroom, User, Questions
from bettercrative.quizzes.forms import QuizForm

quizzes = Blueprint('quizzes', __name__)


@quizzes.route("/quiz/new", methods=['GET', 'POST'])
@login_required
def new_quiz():
    form = QuizForm()
    if form.validate_on_submit():
        quiz = Quiz(
            name=form.name.data,
            question_content=form.question_content.data, 
            owner=current_user
        )
        db.session.add(quiz)
        # add each question to the quiz
        for answer in form.question_answers.data:
            new_answer = Answer(**answer)
            # add each answer to the question
            quiz.question_answers.append(new_answer)
        db.session.commit()
        flash(u'New quiz \"' + quiz.name + '\" created!', 'success')
        return redirect(url_for('quizzes.quiz', id=quiz.id))
    return render_template('create_quiz.html', title='New Quiz', form=form)


@quizzes.route("/quiz/<int:id>")
@login_required
def quiz(id):
    quiz = Quiz.query.get_or_404(id)
    return render_template('quiz.html', title=quiz.name, quiz=quiz)

# Adds a new blank question to Quiz.  
@quizzes.route("/quiz/add")
@login_required
def add_question():
    # gets the name and class_id from the URL params
    print("adding Question")
    quiz_id = request.args.get('quiz_id', None)
    if quiz_id is None:
        return "No quiz id!", 400

    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz is None:
        return "Quiz not found!", 404

    question = Questions(quiz_id = quiz_id)
    if question is None:
        return "Question creation fail - If you see this something is very wrong", 500

    db.session.add(question)

    quiz.questions.append(question)
    
    #load new question data

    #quiz.active_question == quiz.name

    db.session.commit()
    print("success")
    return "addedQuestion - Success", 200
    #return render_template('quiz.html', title=quiz.name, quiz=quiz)

# Removes given quiz 
@quizzes.route("/quiz/remove")
@login_required
def remove_question():
    print("Removing Question")
    # gets the name and class_id from the URL params
    question_id = request.args.get('question_id', None)

    if question_id is None:
        return "No question id!", 400

    question = Questions.query.filter_by(id = question_id).first()
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
    # return render_template('quiz.html', title=quiz.name, quiz=quiz)

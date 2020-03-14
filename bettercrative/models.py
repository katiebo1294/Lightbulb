import enum
from datetime import datetime
from bettercrative import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    classrooms = db.relationship('Classroom', backref='owner', lazy=True, cascade="all, delete, delete-orphan")
    quizzes = db.relationship('Quiz', backref='owner', lazy=True, cascade="all, delete, delete-orphan")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config(['SECRET_KEY'], expires_sec))
        return s.dumps({'id': self.id}).decode('utf-8')

    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            id = s.loads(token)['id']
        except:
            return None
        return User.query.get(id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    date_created = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Multiple quizzes can be attached to a classroom; only one active at a time; quizzes can be in multiple classrooms
    added_quizzes = db.relationship('Quiz', secondary='cl_qz_link', lazy='subquery', backref=db.backref('classroom_host', lazy=True))
    # active quiz ID is stored here, or NULL if no active quiz
    active_quiz = db.Column(db.Integer, nullable=True, default=None)
    
    def __repr__(self):
        return f"Classroom('{self.name}', '{self.date_created}', '{self.user_id}', '{self.added_quizzes}', '{self.active_quiz}')"

# Quiz is a static model, once we create a quiz we do not modify the data inside when referenceing,
# if we are using the quiz we copy contents so we can reuse the same quiz
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    # currently, a classroom has just one question with a list of answers attached to it
    question_content = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date, nullable=False, default=datetime.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # each quiz in a classroom is a copy of the base quiz, so each copy can be active in one classroom
    #classroom_host_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=True)
    # if a quiz is not in a classroom, value is none; otherwise True/False depending on if it is the active quiz
    #active_question = db.Column(db.String, nullable=True)
    questions = db.relationship('Question', backref='quiz', lazy=True, collection_class=list, cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"Quiz('{self.name}', '{self.date_created}', '{self.user_id}', '{self.classroom_host_id}')"

# helper table for the many-to-many relationship between classrooms and quizzes
assoc = db.Table('cl_qz_link', 
    db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.id'), primary_key=True),
    db.Column('quiz_id', db.Integer, db.ForeignKey('quiz.id'), primary_key=True)
    )


class Question(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    category = db.Column(db.Enum('Multiple Choice', 'True/False', 'Short Answer', 'IDE', name = 'question_types'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    
    #answers = an array of tuples, once we migrate to PostgreSQL: (content, correctness)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    responses = db.relationship('Response', backref='student', lazy=True, collection_class=list, cascade="all, delete, delete-orphan")
    # roster?
    
# stores a student's response to a quiz question
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classroom_host_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    quiz_reference = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    isCorrect = db.Column(db.Enum("True", "False", name = "isCorrect"))
    
    def __repr__(self):
            return f"Response('{self.quiz_reference}', '{self.isCorrect}')"

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
    # Multiple quizzes can be attached to a classroom (only one can be active at a time)
    added_quizzes = db.relationship('Quiz', backref='classroom_host', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"Classroom('{self.name}', '{self.date_created}', '{self.user_id}', '{self.active_quiz}')"

# Quiz is a static model, once we create a quiz we do not modify the data inside when referenceing,
# if we are using the quiz we copy contents so we can reuse the same quiz
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    question_content = db.Column(db.String, nullable=False)
    question_answers = db.relationship('Answer', backref='quiz', lazy=True, collection_class=list,
                                       cascade="all, delete, delete-orphan")
    date_created = db.Column(db.Date, nullable=False, default=datetime.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Quiz may be active in one classroom at a time, or none (specified by nullable=True)
    classroom_host_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=True)
    # if a quiz is not in a classroom, value is none; otherwise True/False depending on if it is the active quiz
    # WE SHOULD MOVE THIS TO CLASSROOM TO MATCH THE FLOW CHART, HAVE CLASSROOM LIST WHICH IS THE ACTIVE QUIZ
    active = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return f"Quiz('{self.name}', '{self.date_created}', '{self.user_id}', '{self.classroom_host_id}')"


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    correct = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Answer('{self.content}')"
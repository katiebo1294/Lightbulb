from bettercrative import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    classrooms = db.relationship('Classroom', backref='classroom_owner', lazy=True)
    quizzes = db.relationship('Quiz', backref='quiz_owner', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config(['SECRET_KEY'], expires_sec))
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Classroom(db.Model):
    __tablename__ = 'classroom'
    classroom_id = db.Column(db.Integer, primary_key=True)
    classroom_Name = db.Column(db.String(100), nullable=False)
    key = db.Column(db.String(15), nullable=False)
    classroom_owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return f"Classroom('{self.classroom_Name}')"


class Quiz(db.Model):
    __tablename__ = 'quiz'
    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_Name = db.Column(db.Integer, nullable=False)
    quiz_owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return f"Quiz('{self.quiz_Name}')"

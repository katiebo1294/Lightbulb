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
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    users_classroom = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=False)
    users_quizzes = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)



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
    user = db.relationship('User', backref='classroom_owner')

    def __repr__(self):
        return f"Classroom('{self.classroom_Name}')"


class Quizzes(db.Model):
    __tablename__ = 'quizzes'
    quizzes_id = db.Column(db.Integer, primary_key=True)
    quizzes_Name = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref='quiz_owner')

    def __repr__(self):
        return f"Quizzes('{self.quizzes_Name}')"
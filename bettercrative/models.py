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
    """
        Represents a user (teacher).

        ...
        Attributes
        ----------
        id: int
            the user's ID in the database.
        username: str
            the user's chosen username.
        email: str
            the email associated with the user's account.
        image_file: str
            represents the file uploaded for their profile picture.
        password: str
            the user's chosen password.
        classrooms: list(Classroom)
            a list of the user's created classrooms (see Classroom below).
        quizzes: list(Quizzes)
            a list of the user's created quizzes (see Quiz below).

        Methods
        -------
        get_reset_token(expires_sec=1800):
            Returns: a token to reset the user's password.
        verify_reset_token(token):
            verifies the token supplied in order to reset the password.
    """
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
    """ Represents a classroom.

        ... 
        Attributes
        ----------
        id: int
            the classroom's ID in the database.
        name: str
            the name of the classroom. Also used for student sign-in.
        date_created: date
            the date the classroom was created.
        user_id: int
            the ID of the user who created this classroom.
        added_quizzes: list(Quiz)
            a list of the quizzes that have been added to this classroom (see Quiz below).
        active_quiz: int
            the ID of the quiz that is currently active in this classroom (see Quiz below).
    """    
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
    """ Represents a quiz.

        ...
        Attributes
        ----------
        id: int
            the quiz's ID in the database.
        name: str
            the name of the quiz.
        date_created: date
            the date the quiz was created.
        user_id: int
            the ID of the user who created the quiz.
        questions: list(Question)
            a list of the questions that are in the quiz (see Question below.)
    """
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

    """ A helper table to link the Quiz and Classroom models above in a many-to-many relationship.

        ...
        Attributes
        ----------
        classroom_id: int
            the ID of a classroom in the database.
        quiz_id: int
            the ID of a quiz in the database.
    """
assoc = db.Table('cl_qz_link', 
    db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.id'), primary_key=True),
    db.Column('quiz_id', db.Integer, db.ForeignKey('quiz.id'), primary_key=True)
    )


class Question(db.Model):
    """ Represents a question on a quiz.

        ...
        Attributes
        ----------
        id: int
            the question's ID in the database.
        content: str
            the content of the question.
        category: str
            the type of question. Can be multiple choice, true or false, short answer, or IDE (coding).
        quiz_id: int
            the ID of the quiz this question belongs to.
    """    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    category = db.Column(db.Enum('Multiple Choice', 'True/False', 'Short Answer', 'IDE', name = 'question_types'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    
    #answers = an array of tuples, once we migrate to PostgreSQL: (content, correctness)

class Student(db.Model):
    """ Represents a student user.

        ...
        Attributes
        ----------
        id: int
            the student's ID in the database.
        responses: list(Response)
            a list of responses the student has made to quiz questions (see Response below).
    """
    id = db.Column(db.Integer, primary_key=True)
    responses = db.relationship('Response', backref='student', lazy=True, collection_class=list, cascade="all, delete, delete-orphan")
    # TODO roster? maybe in classroom/user models too
    

class Response(db.Model):
    """ Represents a student's response to a quiz question.

        ...
        Attributes
        ----------
        id: int
            the response's ID in the database.
        classroom_host_id: int
            the ID of the classroom this response is from.
        quiz_reference: int
            the ID of the quiz this response is from.
        isCorrect: str
            whether or not the answer is correct. Can be true or false.
        """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classroom_host_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    quiz_reference = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    isCorrect = db.Column(db.Enum("True", "False", name = "isCorrect"))
    
    def __repr__(self):
            return f"Response('{self.quiz_reference}', '{self.isCorrect}')"

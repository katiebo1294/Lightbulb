from datetime import datetime
from typing import List
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.ext.orderinglist import ordering_list

from bettercrative import db, helpers, login_manager


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
    classrooms = db.relationship('Classroom', backref='owner', cascade="all, delete, delete-orphan")
    quizzes = db.relationship('Quiz', backref='owner', cascade="all, delete, delete-orphan")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
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
    name = db.Column(db.String(60), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Multiple quizzes can be attached to a classroom; only one active at a time; quizzes can be in multiple classrooms
    added_quizzes = db.relationship('Quiz', secondary='cl_qz_link', back_populates='classroom_hosts', cascade='none')
    # active quiz ID is stored here, or None if no active quiz
    active_quiz = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=True, default=None)
    username_required = db.Column(db.Boolean, default=False)
    generate_qr = db.Column(db.Boolean, default=False)
    # the active quiz for the results page
    active_result = db.Column(db.Integer, nullable=True)
    def __repr__(self):
        return f"Classroom('{self.name}', '{self.date_created}', '{self.user_id}', '{self.added_quizzes}', '{self.active_quiz}')"
    """
    Description:
        method for getting the ID's of all objects in that particular Object instance in the database.
    Parameter:
        object
            can be Classroom.added_quizzes, Student.responses, etc.

            e.g:
            to get all response ids from a list of repsonses from a quiz -> Classroom.get_id_list(Quiz.responses)
            to get all students ids from a list of students from a quiz -> Classroom.get_id_list(Quiz.students)
    Return:
        list of ids
    """

    @staticmethod
    def get_id_list(object:List):
        id_list = [item.id for item in object]
        print(id_list)
        return id_list

    
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
                 db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.id')),
                 db.Column('quiz_id', db.Integer, db.ForeignKey('quiz.id')),
                 db.UniqueConstraint('classroom_id', 'quiz_id', name='cl_qz')
                 )


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
        date_created: datetime
            the date the quiz was created.
        date_modified: datetime
            the date the quiz was last edited.
        user_id: int
            the ID of the user who created the quiz.
        classroom_hosts: list(Classroom)
            a list of the classrooms this quiz is in.
        questions: list(Question)
            a list of the questions that are in the quiz (see Question below.)
        current_question: int
            the ID of the currently active question.
        responses: list(Response)
            a list of the responses to this quiz.
        students: list(Student)
            a list of the students that have taken this quiz.
        is_active: int
            the ID of the classroom this quiz is active in; None otherwise.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    classroom_hosts = db.relationship('Classroom', secondary='cl_qz_link', back_populates='added_quizzes',
                                      cascade='none')
    activated_classrooms= db.relationship('Classroom', backref='quiz', cascade='delete, all')
    questions = db.relationship('Question', backref='quiz', order_by="Question.index",
                                collection_class=ordering_list('index'),
                                cascade="all, delete, delete-orphan")
    current_question = db.Column(db.Integer, unique=False, nullable=True, default=None)
    responses = db.relationship("Response", backref = 'quiz', cascade = 'delete, all')
    students = db.relationship("Student", backref = 'quiz', cascade = 'delete, all')
    is_active = db.Column(db.Integer, unique=False, nullable=True, default=None)

    """
        Description:
            this function checks if a certain quiz is activated in one of the classrooms
        Parameters:
            self - Quiz instance
        Return:
            True - Quiz is active in a classroom
            False - Quiz not active anywhere
    """
    def quiz_activated(self):
        if self.activated_classrooms:
            return True
        else:
            return False
    
    """
        Description:
            this function will unset the given quiz instance on all classrooms it is active on.
        Parameters:
            self - Quiz instance
        Return:
            N/A
    """
    def unset(self):
        for classroom in self.classroom_hosts:
            classroom.active_quiz = None
        db.session.commit()

    def __repr__(self):
        return f"Quiz('{self.name}', '{self.date_created}', '{self.user_id}', '{self.classroom_hosts}')"


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
        index: int
            the index of the question in the list.
        answers: Answer[]
            a list of Answer objects (see Answer below).
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    # could be text content or an image file
    content = db.Column(db.Text, nullable=True)
    category = db.Column(db.Enum('Multiple Choice', 'True-False', 'Short Answer', 'IDE', name='question_types'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    index = db.Column(db.Integer)
    answers = db.relationship('Answer', backref='question', collection_class=ordering_list('index'),
                              cascade="all, delete, delete-orphan", order_by="Answer.index")
    responses = db.relationship('Response', backref='question', cascade='delete, all')

    
    def __repr__(self):
        return f"Question('{self.name}', '{self.content}', '{self.category}', '{self.quiz_id}', '{self.index}')"


class Answer(db.Model):
    """ Represents an answer to a quiz question.

        ...
        Attributes
        ----------
        id: int
            the answer's ID in the database.
        content: str
            the content of the answer.
        correct: boolean
            whether or not the answer is correct.
        question_id: int
            the ID of the question this answer belongs to.
    """
    id = db.Column(db.Integer, primary_key=True)
    # could be text content or an image file
    content = db.Column(db.Text, nullable=True)
    correct = db.Column(db.Boolean, nullable=False, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    index = db.Column(db.Integer)
    
    response = db.relationship("Response", backref='answer', cascade='all, delete')

    """
        Description:
            gives the question referenced by the answer
        Parameters:
            
        Return:
            returns a Question object
    """
    def question(self):
        return Question.query.filter_by(id=self.question_id).first()
    def __repr__(self):
        return f"Answer('id:{self.id}' ,'content: {self.content}', 'correct: {self.correct}', 'question_id: {self.question_id}', 'index: {self.index}', 'index: {self.index}')"


# id = db.Column(db.Integer, primary_key=True) responses = db.relationship('Response', backref='student', lazy=True,
# collection_class=list, cascade="all, delete, delete-orphan")
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
    student_id = db.Column(db.ForeignKey('student.id', ondelete='CASCADE'))
    student = db.relationship('Student', back_populates='responses')
    classroom_host_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    quiz_reference = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    value = db.Column(db.Text, nullable=False)
    question_num = db.Column(db.Integer, nullable=False)
    correct = db.Column(db.Boolean, nullable=True, default = None)
    answer_reference = db.Column(db.Integer, db.ForeignKey('answer.id'))
    
    def __repr__(self):
        return f"Response('{self.classroom_host_id}','{self.student_id}', '{self.quiz_reference}', '{self.question_num}', '{self.value}', '{self.correct}')"


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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    responses = db.relationship('Response', back_populates='student', cascade='delete, all')
    quiz_reference = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable = False)
    question_reference = db.Column(db.Integer, db.ForeignKey('question.id'), nullable = True)
    name = db.Column(db.String, nullable = True)
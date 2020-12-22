import datetime
import random

from bettercrative import create_app, bcrypt
from bettercrative import db
from bettercrative.models import User, Classroom, Quiz, Question, Answer

app = create_app()
app.app_context().push()


def get_random_date():
    year = random.randint(2017, 2019)
    month = random.randint(1, 12)
    end_day = 30
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        end_day += 1
    elif month == 2:
        end_day -= 2
    day = random.randint(1, end_day)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime.datetime(year, month, day, hour, minute, second)


db.drop_all()
db.create_all()
# Katie's test account
katie_password = bcrypt.generate_password_hash('testing').decode('utf-8')
katie = User(username='testuser', email='test@email.com', password=katie_password)
db.session.add(katie)
class_names = ['Computing Education (CSCI 497R)', 'Computer Systems II (CSCI 347)', 'Calculus II (MATH 225)',
               'Computer Programming & Linear Data Structures (CSCI 145)', 'Probability & Statistics (MATH 341)']
for i in range(0, 5):
    katie_classroom = Classroom(name=class_names[i], date_created=get_random_date())
    while True:
        date_modified = get_random_date()
        if date_modified >= katie_classroom.date_created:
            break
    katie_classroom.date_modified = date_modified
    katie.classrooms.append(katie_classroom)

# two quizzes, each with 2 MC questions and 4 answers to each
quiz_1 = Quiz(name='Computer Science Department Trivia')
question_1 = Question(name='Question 1', content='Who is the best CS professor?', category='Multiple Choice')
quiz_1.questions.append(question_1)
answer_1_1 = Answer(content='Hao', correct=True)
answer_1_2 = Answer(content='Clauson', correct=False)
answer_1_3 = Answer(content='Meehan', correct=False)
answer_1_4 = Answer(content='Yudong', correct=False)
question_1.answers.append(answer_1_1)
question_1.answers.append(answer_1_2)
question_1.answers.append(answer_1_3)
question_1.answers.append(answer_1_4)
question_2 = Question(name='Question 2', content='Which is the best department at Western?', category='Multiple Choice')
quiz_1.questions.append(question_2)
answer_2_1 = Answer(content='Psychology', correct=False)
answer_2_2 = Answer(content='Education', correct=False)
answer_2_3 = Answer(content='History', correct=False)
answer_2_4 = Answer(content='Computer Science', correct=True)
question_2.answers.append(answer_2_1)
question_2.answers.append(answer_2_2)
question_2.answers.append(answer_2_3)
question_2.answers.append(answer_2_4)
katie.quizzes.append(quiz_1)
quiz_2 = Quiz(name='Math Concepts Review')
question_1 = Question(name='Question 1', content='What is 2 + 2?', category='Multiple Choice')
quiz_2.questions.append(question_1)
answer_1_1 = Answer(content='5', correct=False)
answer_1_2 = Answer(content='-609', correct=False)
answer_1_3 = Answer(content='4', correct=True)
answer_1_4 = Answer(content='37', correct=False)
question_1.answers.append(answer_1_1)
question_1.answers.append(answer_1_2)
question_1.answers.append(answer_1_3)
question_1.answers.append(answer_1_4)
question_2 = Question(name='Question 2', content='What is the square root of 49?', category='Multiple Choice')
quiz_2.questions.append(question_2)
answer_2_1 = Answer(content='3i', correct=False)
answer_2_2 = Answer(content='7', correct=True)
answer_2_3 = Answer(content='100', correct=False)
answer_2_4 = Answer(content='5.67', correct=False)
question_2.answers.append(answer_2_1)
question_2.answers.append(answer_2_2)
question_2.answers.append(answer_2_3)
question_2.answers.append(answer_2_4)
katie.quizzes.append(quiz_2)

# add some empty quizzes to test the quiz datatable
quiz_names = ['Decision Trees', 'AI Formative Assessment', 'Lecture 1: Intro to Machine Organization',
              'Systems Architecture OCR', 'Network Diagrams Terminology', 'Introduction to Cryptography',
              'Quiz: Stacks and Queues', 'Databases', 'Module B: Linear Programming',
              'Set Theory Pop Quiz', 'Permutations and Combinations', 'Differential Equations Vocabulary',
              'Calculus II Exam 1', 'Game Design: Mathematics of Game Theory', 'Steps of Data Analysis']
for i in range(0, 15):
    date_created = get_random_date()
    while True:
        date_modified = get_random_date()
        if date_modified >= date_created:
            break
    quiz = Quiz(name=quiz_names[i], date_created=date_created, date_modified=date_modified)
    katie.quizzes.append(quiz)
# add quizzes to CS classrooms and make one active in CSCI 497R
katie.classrooms[0].added_quizzes.append(Quiz.query.filter_by(name='Steps of Data Analysis').first())
katie.classrooms[0].added_quizzes.append(quiz_1)
katie.classrooms[1].added_quizzes.append(Quiz.query.filter_by(name='Lecture 1: Intro to Machine Organization').first())
katie.classrooms[1].added_quizzes.append(Quiz.query.filter_by(name='Systems Architecture OCR').first())
katie.classrooms[3].added_quizzes.append(Quiz.query.filter_by(name='Quiz: Stacks and Queues').first())
katie.classrooms[3].added_quizzes.append(Quiz.query.filter_by(name='Module B: Linear Programming').first())
katie.classrooms[0].active_quiz = quiz_1.id
quiz_1.is_active = katie.classrooms[0].id
# add quizzes to math classrooms and make one active in MATH 225
katie.classrooms[2].added_quizzes.append(Quiz.query.filter_by(name='Calculus II Exam 1').first())
katie.classrooms[2].added_quizzes.append(Quiz.query.filter_by(name='Differential Equations Vocabulary').first())
katie.classrooms[2].added_quizzes.append(quiz_2)
katie.classrooms[4].added_quizzes.append(Quiz.query.filter_by(name='Set Theory Pop Quiz').first())
katie.classrooms[4].added_quizzes.append(Quiz.query.filter_by(name='Permutations and Combinations').first())
katie.classrooms[2].active_quiz = quiz_2.id
quiz_2.is_active = katie.classrooms[2].id
db.session.commit()
# Tim's test account
tim_password = bcrypt.generate_password_hash('test').decode('utf-8')
tim = User(username='test', email='test@test.com', password=tim_password)
db.session.add(tim)
tim_classroom = Classroom(name='test')
tim.classrooms.append(tim_classroom)
db.session.commit()
# Adrian's test account
adrian_password = bcrypt.generate_password_hash('steel123').decode('utf-8')
adrian = User(username='steel', email='steel@gmail.com', password=adrian_password)
db.session.add(adrian)
adrian_classroom = Classroom(name='cs497')
adrian.classrooms.append(adrian_classroom)
db.session.commit()

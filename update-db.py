from bettercrative import create_app, bcrypt
from bettercrative.models import User, Classroom, Quiz, Question, Answer

app = create_app()
app.app_context().push()
from bettercrative import db

db.drop_all()
db.create_all()
# Katie's test account
katie_password = bcrypt.generate_password_hash('testing').decode('utf-8')
katie = User(username='testuser', email='test@email.com', password=katie_password)
db.session.add(katie)
katie_classroom = Classroom(name='testclass')
katie.classrooms.append(katie_classroom)
# two quizzes, each with 2 MC questions and 4 answers to each
quiz_1 = Quiz(name='Computer Science Quiz')
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
quiz_2 = Quiz(name='Math Quiz')
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
question_2 = Question(name='Question 1', content='What is the square root of 49?', category='Multiple Choice')
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
katie_classroom.added_quizzes.append(quiz_1)
katie_classroom.active_quiz = quiz_1.id
db.session.commit()
# Tim's test account
tim_password = bcrypt.generate_password_hash('test').decode('utf-8')
tim = User(username='test', email='test@test.com', password=tim_password)
db.session.add(tim)
tim_classroom = Classroom(name='test')
tim.classrooms.append(tim_classroom)
db.session.commit()
# Adrians's test account
adrian_password = bcrypt.generate_password_hash('steel123').decode('utf-8')
adrian = User(username='steel', email='steel@gmail.com', password=adrian_password)
db.session.add(adrian)
adrian_classroom = Classroom(name='cs497')
adrian.classrooms.append(adrian_classroom)
db.session.commit()

# test user
test_password = bcrypt.generate_password_hash('password').decode('utf-8')
testuser = User(username='user', email='user@email.com', password=test_password)
db.session.add(testuser)
# two classrooms
classroom_1 = Classroom(name='first classroom')
testuser.classrooms.append(classroom_1)
classroom_2 = Classroom(name='second classroom')
testuser.classrooms.append(classroom_2)
# two quizzes
quiz_1 = Quiz(name='This is my first quiz', question_content='Who is the best CS professor?')
quiz_1.question_answers[0] = Answer(content='Hao', correct=True)
quiz_1.question_answers[1] = Answer(content='Clauson', correct=False)
quiz_1.question_answers[2] = Answer(content='Meehan', correct=False)
quiz_1.question_answers[3] = Answer(content='Yudong', correct=False)
testuser.quizzes.append(quiz_1)
quiz_2 = Quiz(name='This is my second quiz', question_content='What major is the best at Western?')
quiz_2.question_answers[0] = Answer(content='Chemistry', correct=False)
quiz_2.question_answers[1] = Answer(content='Psychology', correct=False)
quiz_2.question_answers[2] = Answer(content='Computer science', correct=True)
quiz_2.question_answers[3] = Answer(content='Accounting', correct=False)
testuser.quizzes.append(quiz_2)
# Add both quizzes to first classroom, second quiz to second classroom, make first active in c1 and second active in c2
classroom_1.quizzes.append(quiz_1)
classroom_1.quizzes.append(quiz_2)
classroom_1.active_quiz = quiz_1.id
quiz_1.active = True
classroom_2.quizzes.append(quiz_1)
classroom_2.active_quiz = quiz_2.id
quiz_2.active = True
db.session.commit()
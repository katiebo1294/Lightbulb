from bettercrative import create_app, bcrypt
from bettercrative.models import User, Classroom
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
from bettercrative import create_app, bcrypt
from bettercrative.models import User, Classroom
app = create_app()
app.app_context().push()
from bettercrative import db
db.drop_all()
db.create_all()
hashed_password = bcrypt.generate_password_hash('testing').decode('utf-8')
user = User(username='testuser', email='test@email.com', password=hashed_password)
db.session.add(user)
classroom = Classroom(name='testclass')
user.classrooms.append(classroom)
db.session.commit()

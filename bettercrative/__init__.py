from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from bettercrative.config import Config


# Application factory
# Blueprint registartion

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.app = app

    app.app_context().push()
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from bettercrative.users.routes import users
    from bettercrative.classrooms.routes import classrooms
    from bettercrative.main.routes import main
    from bettercrative.quizzes.routes import quizzes

    app.register_blueprint(users)
    app.register_blueprint(classrooms)
    app.register_blueprint(main)
    app.register_blueprint(quizzes)

    return app


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'users.info'
mail = Mail()
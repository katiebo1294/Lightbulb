from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from bettercrative.config import Config
# Application factory
# Blueprint registration
from bettercrative.errors.routes import not_found


def create_app(config_class=Config):
    app = Flask(__name__)
    Bootstrap(app)
    app.config.from_object(config_class)
    db.app = app

    app.app_context().push()
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    migrate.init_app(app, db)

    #  app.config.from_object(os.environ['APP_SETTINGS'])
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from bettercrative.users.routes import users
    from bettercrative.classrooms.routes import classrooms
    from bettercrative.main.routes import main
    from bettercrative.quizzes.routes import quizzes
    from bettercrative.errors.routes import errors

    app.register_blueprint(users)
    app.register_blueprint(classrooms)
    app.register_blueprint(main)
    app.register_blueprint(quizzes)
    app.register_blueprint(errors)

    app.register_error_handler(404, not_found)

    return app


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'users.info'
mail = Mail()

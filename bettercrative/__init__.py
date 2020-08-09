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
from bettercrative.errors.routes import bad_request, unauthorized, forbidden,  not_found


def get_alphabet_index(index):
    alpha = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    s = ""
    quotient = index
    while quotient > 26:
        remainder = int(quotient % 26)
        # Takes care of edge case when rightmost letter is Z
        if remainder == 0:
            quotient -= 26
        s += alpha[remainder - 1]
        quotient = int(quotient / 26)
    s += alpha[quotient - 1]
    return s[::-1]


def append_form(form):
    form.answer_form.append_entry()

def remove_form(form):
    form.answer_form.pop()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.jinja_options['extensions'].append('jinja2.ext.loopcontrols')
    Bootstrap(app)
    app.config.from_object(config_class)
    db.app = app

    app.app_context().push()
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    migrate.init_app(app, db)

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

    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, not_found)

    app.jinja_env.globals.update(get_alphabet_index=get_alphabet_index)
    app.jinja_env.globals.update(append_form=append_form)
    
    return app


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'users.info'
mail = Mail()

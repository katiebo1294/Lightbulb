from bettercrative import create_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app()
app.app_context().push()
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    app.run(debug=True)
    manager.run()



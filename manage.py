import unittest

from app.init_app import socketIo, app

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import blueprint
from app.main import db


app.register_blueprint(blueprint)
app.app_context().push()
app.config['ERROR_404_HELP'] = False

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    socketIo.run(app)


@manager.command
def test():
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()

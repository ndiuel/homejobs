import email
import os
import requests

from flask.globals import request
from app import create_app
from app.models import db
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand
from datetime import timedelta, datetime, date, time
from app.models import User
from app.models.role import ADMIN_ROLES
from app import services

app = create_app(os.getenv('FLASK_ENV') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def drop_all():
    db.drop_all()


@manager.command
def create_all():
    db.create_all()


@manager.command
def create_default_user():
    User(
        username="ndiuel",
        email="mail@mail.com",
        phone_no="07052230829",
        password="me"
    )


        

if __name__ == '__main__':
    manager.run()


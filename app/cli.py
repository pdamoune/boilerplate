import os
import click

from . import db
from app.models import User, Role


def register(app):
    """
        Run flask with no arguments
    """
    @app.cli.command()
    def dropdb():
        """
        Recreates a local database. You probably should not use this on
        production.
        """
        db.drop_all()
        db.session.commit()

    @app.cli.command()
    def createdb():
        """
        Recreates a local database. You probably should not use this on
        production.
        """
        db.create_all()
        db.session.commit()

    @app.cli.command()
    def recreatedb():
        """
        Recreates a local database. You probably should not use this on
        production.
        """
        db.drop_all()
        db.create_all()
        db.session.commit()

    @app.cli.command()
    def insertroles():
        """
        Creates Roles in databases
        """
        from .models import Role
        Role.insert_roles()

    @app.cli.command()
    def createadmin():
        """
        Create admin account
        """
        u = User(
            username=app.config['ADMIN_EMAIL'],
            email=app.config['ADMIN_EMAIL'],
            password=app.config['ADMIN_PASSWORD'],
            role_id=3)
        db.session.add(u)
        print("[Created] " + str(u))
        db.session.commit()

    @app.cli.command()
    def createusers():
        """Creates users."""
        perm = {'user': 1, 'moderator': 2, 'administrator': 3}
        users = [
            ['philippe1', 'philippe1@test.com', 'test', perm['user']],
            ['testmod132', 'testmod12@test.com', 'test', perm['moderator']],
            ['testadmin132', 'testadmin13@test.com', 'test', perm['administrator']],
        ]
        for user in users:
            if User.query.filter_by(username=user[0]).first():
                print(f'Username {user[0]} already exists.')
                continue
            if User.query.filter_by(email=user[1]).first():
                print(f'Email {user[1]} already used.')
                continue
            u = User(
                username=user[0],
                email=user[1],
                password=user[2],
                role_id=user[3])
            db.session.add(u)
            print("[Created] " + str(user))
        db.session.commit()

    @app.cli.command()
    def fake():
        """
        Creates fake users and posts. You probably should not use this on
        production.
        """
        from app.fake import users, posts
        users(30)
        posts(30)

    @app.cli.command()
    @click.argument('test_name', required=False)
    def test(test_name=None):
        """Run a specific unit test."""
        import unittest
        print("test")
        if test_name is None:
            tests = unittest.TestLoader().discover('tests')
        else:
            tests = unittest.TestLoader().loadTestsFromName(
                'tests.' + test_name)
        unittest.TextTestRunner(verbosity=2).run(tests)

    @app.cli.command()
    def clean():
        """
        Remove *.pyc and *.pyo files recursively starting at current directory
        """
        for dirpath, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                if filename.endswith('.pyc') or filename.endswith('.pyo'):
                    full_pathname = os.path.join(dirpath, filename)
                    print('Removing %s' % full_pathname)
                    os.remove(full_pathname)
            if '__pycache__' in dirpath and not os.listdir(dirpath):
                os.rmdir(dirpath)

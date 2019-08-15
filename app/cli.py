import os
import shutil
from . import db
from app.models import User, Role


def register(app):
    """
        Run flask with no arguments
    """
    @app.cli.command()
    def dropdb():
        """
        Delete all database data.
        """
        db.drop_all()
        db.session.commit()
        print('All data has been deleted.')

    @app.cli.command()
    def createdb():
        """
        Creates a local database. You probably should not use this on
        production.
        """
        db.create_all()
        print('Database created')

    @app.cli.command()
    def recreatedb():
        """
        Delete all database data and create a new one
        """
        db.drop_all()
        db.create_all()
        db.session.commit()
        print('Deleted all database data and created a new one')

    @app.cli.command()
    def insertroles():
        """
        Creates Roles in databases
        """
        from .models import Role
        Role.insert_roles()
        print('Roles inserted')

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
        db.session.commit()
        print("[Created] " + str(u))

    @app.cli.command()
    def createtestusers():
        """Creates users."""
        perm = {'user': 1, 'moderator': 2, 'administrator': 3}
        users = [
            [
                'test_classic',
                'test_classic@test.com',
                'test',
                perm['user']],
            [
                'test_samepassword1',
                'test_samepassword1@test.com',
                'samepassword',
                perm['user']],
            [
                'test_samepassword2',
                'test_samepassword2@test.com',
                'samepassword',
                perm['user']],
            [
                'test_moderator',
                'test_moderator@test.com',
                'test',
                perm['moderator']],
            [
                'test_administrator',
                'test_admin@test.com',
                'test',
                perm['administrator']],
        ]
        for user in users:
            if User.query.filter_by(username=user[0]).first():
                print('Users already created')
                break
            u = User(
                username=user[0],
                email=user[1],
                password=user[2],
                role_id=user[3])
            db.session.add(u)
            print("[Created] " + str(user))
        db.session.commit()

    @app.cli.command()
    def createfakeusers():
        """
        Creates fake users and posts. You probably should not use this on
        production.
        """
        from faker import Faker
        fake = Faker()
        i = 0
        while i < 10:
            u = User(email=fake.email(),
                     username=fake.user_name(),
                     password='password')
            db.session.add(u)
            i += 1
        db.session.commit()

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
            if dirpath == "./tmp":
                print('Removing %s' % dirpath)
                shutil.rmtree(dirpath)
        print('tmp, *.pyc and *.pyo files deleted')

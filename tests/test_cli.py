import unittest
import time
from app import create_app, db, cli, config
from app.models import User
from tests import c


class CLITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\033[36m[CLITestCase] \033[m")

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        cli.register(self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_createdb(self):
        runner = self.app.test_cli_runner()
        result = runner.invoke(args=['createdb'])
        self.assert_('Database created' in result.output)

    def test_dropdb(self):
        runner = self.app.test_cli_runner()
        result = runner.invoke(args=['dropdb'])
        self.assert_('All data has been deleted.' in result.output)

    def test_recreatedb(self):
        runner = self.app.test_cli_runner()
        result = runner.invoke(args=['recreatedb'])
        self.assert_('Deleted all database data and created a new one' in result.output)

    def test_insertroles(self):
        self.test_createdb()
        runner = self.app.test_cli_runner()
        result = runner.invoke(args=['insertroles'])
        self.assert_('Roles inserted' in result.output)

    def test_createadmin(self):
        self.test_createdb()
        runner = self.app.test_cli_runner()
        result = runner.invoke(args=['createadmin'])
        u = User.query.first()
        self.assertTrue(u.email == config['testing'].ADMIN_EMAIL)

    def test_createtestusers(self):
        self.test_createdb()
        runner = self.app.test_cli_runner()
        result = runner.invoke(args=['createtestusers'])
        u = User.query.all()
        self.assertTrue(len(u) != 0)
        result = runner.invoke(args=['createtestusers'])
        self.assert_('Users already created')

    def test_createfakeusers(self):
        self.test_createdb()
        runner = self.app.test_cli_runner()
        result = runner.invoke(args=['createfakeusers'])
        u = User.query.all()
        self.assertTrue(len(u) != 0)

    def test_clean(self):
        runner = self.app.test_cli_runner()
        result = runner.invoke(args=['clean'])
        self.assertIn('*.pyc and *.pyo files deleted', result.output)

    # def test_createdb(self):
    #     register.createdb()

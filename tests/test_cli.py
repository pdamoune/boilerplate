import unittest
import time
from app import create_app, db, cli, config, admin
from app.models import User
from tests import SetUpClass


class CLITestCase(SetUpClass):
    def setUp(self):
        self.setUpApp()
        cli.register(self.app)

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

    def test_createroles(self):
        self.test_createdb()
        runner = self.app.test_cli_runner()
        result = runner.invoke(args=['createroles'])
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

    def test_createall(self):
        runner = self.app.test_cli_runner()
        result = runner.invoke(args=['createall'])
        self.assert_('Deleted all ' in result.output)
        self.assert_('Roles inserted' in result.output)
        self.assert_("[Created] <User 'admin@admin.com'>" in result.output)
        self.assert_("[Created] ['test_classic'" in result.output)
        self.assert_('Fake users created' in result.output)

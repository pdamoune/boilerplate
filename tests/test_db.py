import unittest
from flask import current_app
from app import create_app, db


class TestDb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\033[36m[TestDb] \033[m")

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        # db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_other(self):
        self.assertFalse(False)

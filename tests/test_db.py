import unittest
from flask import current_app
from app import create_app


class OtherTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        # db.create_all()

    def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
        self.app_context.pop()

    def test_other(self):
        self.assertFalse(False)

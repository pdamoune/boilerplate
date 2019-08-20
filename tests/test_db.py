import unittest
from flask import current_app
from app import create_app, db, admin
from tests import SetUpClass


class TestDb(SetUpClass):
    def setUp(self):
        self.setUpApp()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_other(self):
        self.assertFalse(False)

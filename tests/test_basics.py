# import unittest
from flask import current_app
from app import create_app, db, admin
from tests import SetUpClass


class BasicsTestCase(SetUpClass):
    def setUp(self):
        self.setUpApp()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

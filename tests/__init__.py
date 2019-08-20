import unittest
from app import create_app, db, admin
from app.models import Role


class SetUpClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print(f"\033[36m[{cls.__name__}] \033[m")

    def setUpApp(self):
        admin._views = []
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

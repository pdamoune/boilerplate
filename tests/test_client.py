import unittest
from app import create_app, db
from app.models import User, Role


class FlaskClientTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\033[36m[UserModelTestCase] \033[m")

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="index"' in response.get_data(as_text=True))

    def test_notfound_page(self):
        response = self.client.get('/error')
        self.assertEqual(response.status_code, 404)
        self.assertTrue('Not Found' in response.get_data(as_text=True))

    def test_internalerror_page(self):
        response = self.client.get('/internal')
        self.assertEqual(response.status_code, 500)
        self.assertTrue('Internal Server Error' in response.get_data(as_text=True))

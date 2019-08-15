import re
import unittest
from app import create_app, db
from app.models import User, Role
from wtforms import ValidationError



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
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('id="index"' in r.get_data(as_text=True))

    def test_notfound_page(self):
        r = self.client.get('/error')
        self.assertEqual(r.status_code, 404)
        self.assertTrue('Not Found' in r.get_data(as_text=True))

    def test_internalerror_page(self):
        r = self.client.get('/internal')
        self.assertEqual(r.status_code, 500)
        self.assertTrue('Internal Server Error' in r.get_data(as_text=True))

    def test_login_page(self):
        r = self.client.get('/auth/login')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('Login' in r.get_data(as_text=True))

    def test_register_page(self):
        r = self.client.get('/auth/register')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('Register' in r.get_data(as_text=True))


    def test_register_and_login(self):
        r = self.client.post('/auth/register', data={
            'email': 'test@test.com',
            'username': 'test',
            'password': 'test',
            'password2': 'test'
        })
        self.assertEqual(r.status_code, 302)

        # login with the new account
        r = self.client.post('/auth/login', data={
            'email': 'test@test.com',
            'password': 'test'
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(re.search('Log Out',
                                  r.get_data(as_text=True)))

        # Log Out
        r = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('You have been logged out' in r.get_data(
            as_text=True))

    def test_wrong_user_or_password(self):
        r = self.client.post('/auth/login', data={
            'email': 'test@test.com',
            'password': 'test',
        })
        self.assertTrue('Invalid email or password.' in r.get_data(
            as_text=True))

    def test_username_or_email_already_exists(self):
        data = {
            'email': 'test@test.com',
            'username': 'test',
            'password': 'test',
            'password2': 'test'
        }
        r = self.client.post('/auth/register', data=data)
        self.assertEqual(r.status_code, 302)

        r = self.client.post('/auth/register', data=data)
        self.assertTrue('Email already registered.' in r.get_data(
            as_text=True))

        data['email'] = 'test1@test.com'
        r = self.client.post('/auth/register', data=data)
        self.assertTrue('Username already in use.' in r.get_data(
            as_text=True))

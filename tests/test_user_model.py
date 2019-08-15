import unittest
import time
from app import create_app, db, config
from app.models import User, AnonymousUser, Role, Permission


class UserModelTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\033[36m[UserModelTestCase] \033[m")

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_setter(self):
        u = User(email='test@test.com', username='test', password='test')
        self.assertTrue(u.email is not None)
        self.assertTrue(u.username is not None)
        self.assertTrue(u.password_hash is not None)

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.VISITOR))
        self.assertFalse(u.can(Permission.READ))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))


    def test_user_role(self):
        u = User(email='john@example.com', password='cat')
        self.assertTrue(u.can(Permission.VISITOR))
        self.assertTrue(u.can(Permission.READ))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_moderator_role(self):
        u = User(email='test')
        u.role = Role.query.filter_by(name='Moderator').first()
        self.assertTrue(u.can(Permission.VISITOR))
        self.assertTrue(u.can(Permission.READ))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_admin_role(self):
        u = User(email=config['testing'].ADMIN_EMAIL)
        self.assertTrue(u.can(Permission.VISITOR))
        self.assertTrue(u.can(Permission.READ))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertTrue(u.can(Permission.ADMIN))

    def test_add_permission(self):
        self.test_user_role()
        u = User(email='john@example.com', password='cat')
        u.role.add_permission(Permission.MODERATE)
        self.assertTrue(u.can(Permission.MODERATE))
        u.role.add_permission(Permission.MODERATE)
        self.assertTrue(u.can(Permission.MODERATE))

    def test_remove_permission(self):
        self.test_user_role()
        u = User(email='john@example.com', password='cat')
        u.role.remove_permission(Permission.WRITE)
        self.assertFalse(u.can(Permission.WRITE))
        u.role.remove_permission(Permission.WRITE)
        self.assertFalse(u.can(Permission.WRITE))

    def test_reset_permission(self):
        self.test_user_role()
        u = User(email='john@example.com', password='cat')
        u.role.reset_permissions()
        self.assertFalse(u.can(Permission.VISITOR))
        self.assertFalse(u.can(Permission.READ))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_roles_already_exsist(self):
        Role.insert_roles()
        u = User(role=Role(name='Administrator', permissions=15))

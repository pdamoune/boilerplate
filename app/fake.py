from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User


def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password')
        db.session.add(u)
        i += 1
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

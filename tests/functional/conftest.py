import pytest
import sys
import os

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app import app as flask_app
from db import db
from models import User

class AuthActions:
    def __init__(self, client, name='Test User', email='test@example.com', password='TestPass'):
        self.client = client
        self.name = name
        self.email = email
        self.password = password

    def create(self):
        with self.client.application.app_context():
            test_user = User(name=self.name, email=self.email, password=self.password)
            db.session.add(test_user)
            db.session.commit()

    def login(self):
        return self.client.post(
            '/login',
            data={'email': self.email, 'password': self.password}
        )

    def logout(self):
        return self.client.get('/logout')

@pytest.fixture
def test_app():
    # Set up the application for testing
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",  # In-memory database for testing
        "WTF_CSRF_ENABLED": False,  # Disable CSRF for simplicity in tests
    })

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()

@pytest.fixture
def runner(test_app):
    return test_app.test_cli_runner()

@pytest.fixture
def auth(client):
    return AuthActions(client)

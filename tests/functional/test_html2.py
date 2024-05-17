import pytest
import sys
import os

# # Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')))

from db import db
from models import User
from app import app

# Create a test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()

    with app.app_context():
        db.create_all()

        # Create a test user
        test_user = User(name='test_user', email='test@example.com', password='test_password')
        db.session.add(test_user)
        db.session.commit()

        yield client

        db.session.remove()
        db.drop_all()

def test_homepage_logged_in(client):
    # Log in with the test user
    response = client.post('/auth/login', data=dict(
        email='test@example.com',
        password='test_password'
    ), follow_redirects=True)
    assert response.status_code == 200

    # Access the home page
    response = client.get('/views/homepage', follow_redirects=True)
    assert response.status_code == 200


def test_homepage_not_logged_in(client):
    # Attempt to access the home page without logging in
    response = client.get('/views/homepage', follow_redirects=False)
    assert response.status_code == 302


def test_newoutfit_logged_in(client):
    # Log in with the test user
    response = client.post('/auth/login', data=dict(
        email='test@example.com',
        password='test_password'
    ), follow_redirects=True)
    assert response.status_code == 200

    # Access the new outfit page
    response = client.get('/views/newoutfit', follow_redirects=True)
    assert response.status_code == 200


def test_newoutfit_not_logged_in(client):
    # Attempt to access the new outfit page without logging in
    response = client.get('/views/newoutfit', follow_redirects=False)
    assert response.status_code == 302


def test_wardrobe_logged_in(client):
    # Log in with the test user
    response = client.post('/auth/login', data=dict(
        email='test@example.com',
        password='test_password'
    ), follow_redirects=True)
    assert response.status_code == 200

    # Access the wardrobe page
    response = client.get('/views/wardrobe', follow_redirects=True)
    assert response.status_code == 200

def test_wardrobe_not_logged_in(client):
    # Attempt to access the wardrobe page without logging in
    response = client.get('/views/wardrobe', follow_redirects=False)
    assert response.status_code == 302
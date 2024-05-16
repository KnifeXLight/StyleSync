import pytest
import sys
import os
from flask import url_for

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app import app
from db import db
from models import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_home_route(client):
    response = client.get('/')
    assert b'Login' in response.data

def test_register_route(client):
    response = client.get('/auth/register')
    assert b'Register' in response.data

def test_signup(client):
    response = client.post('/auth/register', data={'name': 'Test User', 'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    assert b'Login' in response.data

def test_login(client):
    # Create a test user
    user = User(name='Test User', email='test@example.com', password='password')
    db.session.add(user)
    db.session.commit()

    # Make a POST request to login with the test user credentials
    response = client.post('/auth/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)

def test_logout(client):
    # Create a test user
    user = User(name='Test User', email='test@example.com', password='password')
    db.session.add(user)
    db.session.commit()

    # Log in the test user
    client.post('/auth/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)

    # Make a GET request to logout
    response = client.get('/auth/logout', follow_redirects=True)

    # Check if the logout was successful by checking if the user is redirected to the login page
    assert b'Login' in response.data

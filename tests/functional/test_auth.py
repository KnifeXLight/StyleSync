import re
import sys
import os
import pytest
from flask import url_for, redirect, request, flash, session
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app import app
from db import db
from models import User

# This is a fixture that creates a test client for the app
@pytest.fixture
def client():
    app.config['TESTING'] = 'sqlite:///test.db'
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()

@pytest.fixture
def auth_client(client):
    with app.app_context():
        # Create a test user if it doesn't exist
        yield login_user(User(name='test user', email='test@example.com', password=generate_password_hash('password')))

@pytest.fixture
def logged_in_client(client):
    with app.app_context():
        # Create a test user if it doesn't exist
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            test_user = User(name='test user', email='test@example.com', password=generate_password_hash('password'))
            db.session.add(test_user)
            db.session.commit()

    # Log in the test user
        client.post('/auth/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    
        with client.session_transaction() as sess:
            sess['user_id'] = test_user.id
    
    return client
# Test home page
def test_home(client):
        response = client.get("/")
        assert response.status_code == 200

# Test user registration page
def test_register(client):
        response = client.get("/auth/register")
        assert response.status_code ==  200

# Test user registration
def test_signup(client):
    
    email = "test@example.com"
    name = "Test User"
    password = "testpassword"

    form_data = {
        "email": email,
        "name": name,
        "password": password
    }
    
    with app.test_request_context():
        response = client.post(url_for("authorization.signup"), data=form_data, follow_redirects=True)

    # Assuming you're redirecting to the same page on validation failure
    assert response.status_code == 200

    # Check if user is added to the database
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        assert user is not None
        assert user.email == form_data["email"]
        assert user.name == form_data["name"]

        assert check_password_hash(user.password, password)


# Test when required data is missing
def test_signup_missing_data(client):
    form_data = {
        "email": "",
        "name": "Test User",
        "password": "password123"
    }

    response = client.post("/auth/register", data=form_data, follow_redirects=True)

    # Assuming registration redirects to the same page on validation failure
    assert response.status_code == 200


# Test when password is less than 8 characters
def test_signup_short_password(client):
    form_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "pass"  # Short password
    }

    response = client.post("/auth/register", data=form_data, follow_redirects=True)

    # Assuming registration redirects to the same page on validation failure
    assert response.status_code == 200
    with app.app_context(): # Check flash message for short password
        assert b"Password must be at least 8 characters long" in response.data


def test_login(client):
    with app.app_context():
        response = client.post('/auth/login', data=dict(
        email='test@example.com',
        password='test_password'
    ), follow_redirects=True)
    assert response.status_code == 200
    print (response.data)
    assert response.request.path == '/'

# def test_login(client):
#     url = "/auth/login"
#     data = dict(email="test@example.com", password="password")
#     response = client.post(url, data=data)
#     assert response.status_code == 302

#     url = url_for("html.home", _external=False)
#     response = client.get(url)
#     assert response.status_code == 200
#     assert response.location.endswith('/html/home')
#     print (response.data)
#     assert response.status_code == 200

def test_logout(client):
    with app.app_context():
        # Create a test user
        user = User(name='Test User', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

    # Log in the test user
    client.post('/auth/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)

    # Make a GET request to logout
    response = client.get('/auth/logout', follow_redirects=True)

    # Check if the logout was successful by checking if the user is redirected to the login page
    assert response.status_code == 200  # Ensure the response status code is 200 (OK)
    assert response.request.path == '/'  # Ensure the current URL is the home page URL

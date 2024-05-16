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

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client
    with app.app_context():
        db.drop_all()

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


# from routes.auth import login_post, logout

# # Test case for login_post route
# def test_login_post(client, monkeypatch):
#     # Create a test user
#     with app.app_context():
#         hashed_password = generate_password_hash('password')
#         user = User(name='Test User', email='test@example.com', password=hashed_password)
#         db.session.add(user)
#         db.session.commit()

#     # Define mock request form data
#     with app.test_request_context('/auth/login', method='POST', data={'email': 'test@example.com', 'password': 'password'}):
#         def mock_execute(statement):
#             return user

#         # Patch db session execute method to return the test user
#         monkeypatch.setattr(db.session, 'execute', mock_execute)

#         # Call the login_post function
#         response = login_post()

#         # Assert flash message and redirection
#         assert 'Email or Password is incorrect' not in session
#         assert response.location == url_for('authorization.home', _external=True)

# # Test case for logout route
# def test_logout(client):
#     # Simulate logged-in user
#     with app.test_request_context('/auth/logout'):
#         session['user_id'] = 1

#         # Call the logout function
#         response = logout()

#         # Assert redirection
#         assert response.location == url_for('authorization.home', _external=True)


def test_login(client):
    with app.app_context():
        # Create a test user
        user = User(name='Test User', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

    # Make a POST request to login with the test user credentials
    response = client.post('/auth/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)

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

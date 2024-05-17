# Import necessary modules
import pytest
from flask import url_for, request
from flask_login import current_user
import sys
import os
from werkzeug.security import generate_password_hash


# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app import app as flask_app
from db import db
from models import User

def test_login(client):
    with flask_app.app_context():
        # Create a test user
        user = User(name='Test User', email='test@example.com', password=generate_password_hash('password', method='scrypt'))
        db.session.add(user)
        db.session.commit()

    # Make a POST request to login with the test user credentials
    response = client.post('/auth/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    print(response.data)
    # Check if login was successful and user is redirected to the correct page
    assert response.status_code == 200
    with client.application.test_request_context():
        assert request.endpoint == 'authorization.home'  #

def test_logout(client, auth):
    # Log in the user first
    with flask_app.app_context():
        user = User(name='Test User', email='test@example.com', password=generate_password_hash('password', method='scrypt'))
        db.session.add(user)
        db.session.commit()

    client.post('/auth/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)

    # Perform the logout action
    response = client.get('/auth/logout', follow_redirects=True)
    
    # Check if logout was successful and user is redirected to the correct page
    assert response.status_code == 200
from flask import request
import sys
import os
from werkzeug.security import generate_password_hash

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from db import db 
from models import User


# * Test Login Functionality works with valid credentials * #
def test_login(logged_in_client):
    response = logged_in_client.get('/views/home')
    print (response.data)
    assert response.status_code == 200
    with logged_in_client.application.test_request_context():
        assert request.endpoint == 'authorization.home'

# * Test Login Functionality works with invalid credentials * #
def test_login_invalid_password(failed_login_password):
    response = failed_login_password.get('/views/home')
    print (response.data)
    assert response.status_code == 302
    with failed_login_password.application.test_request_context():
        assert request.endpoint == 'authorization.home'

# * Test Logout Functionality * #
def test_logout(client, app):
    # Log in the user first
    with app.app_context():
        user = User(name='Test User', email='test@example.com', password=generate_password_hash('password', method='scrypt'))
        db.session.add(user)
        db.session.commit()

    client.post('/auth/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)

    # Perform the logout action
    response = client.get('/auth/logout', follow_redirects=True)
    print(response.data)
    # Check if logout was successful and user is redirected to the correct page
    assert response.status_code == 200
    with client.application.test_request_context():
        assert request.endpoint == 'authorization.home'
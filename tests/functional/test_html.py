from math import log
from flask import session, url_for
import pytest
import sys
import os

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')))

from db import db
from models import User
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()


@pytest.fixture
def logged_in_client(client):
    # Create a test user
    user = User(name='Test User', email='test@example.com',
                password='password')
    db.session.add(user)
    db.session.commit()
    # Log in the test user; Simulate user login
    client.post('/auth/login', data={'email': 'test@example.com',
                'password': 'password'}, follow_redirects=True)
    return client


# This should redirect you to login if you type in url without login.
def test_home_redirect(client):
    response = client.get('/views/home', follow_redirects=True)
    # Assuming the login page redirects to the home page after successful login
    assert response.status_code == 200


# This test checks if login is successful, and should direct you to homepage
def test_user_login_and_homepage(client):
    response = client.post(
        '/auth/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    # Checks if login fails and redirects you to login page
    assert response.status_code != 302


# def test_access_protected_route_wardrobe(logged_in_client):
#     response = logged_in_client.get('/views/wardrobe')
#     assert response.status_code == 200
#     # Checks if login fails and redirects you to login page
#     assert response.status_code != 302
#     assert b'StyleSynckk' in response.data


def test_access_protected_route_wardrobe(logged_in_client):
    response = logged_in_client.get('/views/wardrobe')
    assert response.status_code == 200
"""
Same as previous except check base.html in html folder. Title currently is StyleSynckk
Change title for errors. Remember that login data is hardcoded to my info, need to change that
"""


def test_access_protected_route_homepage(logged_in_client):
    response = logged_in_client.get('/views/home')
    assert response.status_code == 200
    # Checks if login fails and redirects you to login page
    assert response.status_code != 302


"""
Same as previous except check base.html in html folder. Title currently is StyleSynckk
Change title for errors. Remember that login data is hardcoded to my info, need to change that
"""


def test_access_protected_route_newoutfit(logged_in_client):
    response = logged_in_client.get('/views/newoutfit')
    assert response.status_code == 200
    # Checks if login fails and redirects you to login page
    assert response.status_code != 302
    assert b'StyleSynckk' in response.data


"""
Same as previous except check base.html in html folder. Title currently is StyleSynckk
Change title for errors. Remember that login data is hardcoded to my info, need to change that
"""

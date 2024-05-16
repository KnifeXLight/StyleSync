import pytest
import sys
import os

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from flask import session, url_for
from app import app
from models import User
from db import db

@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

@pytest.fixture(scope='module')
def logged_in_client(client):
    with app.app_context():
        # Check if the test user already exists in the database
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            # Create a new test user if it doesn't exist
            test_user = User(name='Test User', email='test@example.com', password='password')
            db.session.add(test_user)
            db.session.commit()
    
    # Log in the test user
    response = client.post('/auth/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200  # Ensure login was successful
    with client.session_transaction() as sess:
        sess['user_id'] = 2
    return client


# This should redirct you to login if you type in url without login.
def test_home_redirct(client):
    response = client.get('/views/home', follow_redirects=True)
    assert response.status_code == 200  # Assuming the login page redirects to the home page after successful login
    assert b'StyleSynctest' in response.data  # Adjust this assertion based on the content of your home page
"""
in base.html in auth folder, i changed the title to match the assert data. 
If you change it back to StyleSync, it should fail test and display redirect page.
Look and see and change the title to check.
"""

# This test checks if login is successful, and should direct you to homepage
def test_user_login_and_homepage(logged_in_client):
    response = logged_in_client.get('/views/wardrobe', follow_redirects=True)
    # I hardcoded it so it logins in with my cred, need to change this
    assert logged_in_client.get('/views/home', follow_redirects=True).status_code == 200
    assert logged_in_client.get('/views/home', follow_redirects=True).status_code != 302  # Checks if login fails and redirects you to login page
    assert b'StyleSynckk' in response.data  
"""
Same as previous except check base.html in html folder. Title currently is StyleSynckk
Change title for errors. Remember that login data is hardcoded to my info, need to change that
WTF, if i delete this, the tests below do not work? It makes sense somewhat
"""

def test_access_protected_route_wardrobe(logged_in_client):
    response = logged_in_client.get('/views/wardrobe')
    assert response.status_code == 200
    assert response.status_code != 302  # Checks if login fails and redirects you to login page
    assert b'StyleSynckk' in response.data
"""
Same as previous except check base.html in html folder. Title currently is StyleSynckk
Change title for errors. Remember that login data is hardcoded to my info, need to change that
"""

def test_access_protected_route_homepage(logged_in_client):
    response = logged_in_client.get('/views/home')
    assert response.status_code == 200
    assert response.status_code != 302  # Checks if login fails and redirects you to login page
    assert b'StyleSynckk' in response.data
"""
Same as previous except check base.html in html folder. Title currently is StyleSynckk
Change title for errors. Remember that login data is hardcoded to my info, need to change that
"""

def test_access_protected_route_newoutfit(logged_in_client):
    response = logged_in_client.get('/views/newoutfit')
    assert response.status_code == 200
    assert response.status_code != 302  # Checks if login fails and redirects you to login page
    assert b'StyleSynckk' in response.data
"""
Same as previous except check base.html in html folder. Title currently is StyleSynckk
Change title for errors. Remember that login data is hardcoded to my info, need to change that
"""
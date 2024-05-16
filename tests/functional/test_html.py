import pytest
import sys
import os

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from flask import session
from app import app
from models import User

@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def logged_in_client(client):
    # Simulate user login
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Assuming user ID is 1
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
def test_user_login_and_homepage(client):
    # I hardcoded it so it logins in with my cred, need to change this
    response = client.post('/auth/login', data={'email': 'kms@test.ca', 'password': 'HAHAXD123'}, follow_redirects=True)
    
    assert response.status_code == 200
    assert response.status_code != 302  # Checks if login fails and redirects you to login page
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
import pytest
import sys
import os

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from flask import session
from app import app
from models import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
# this is the original code, I DONT KNOW WHAT TO DO HERE RIGHT NOW!!!!!!!
def test_home(client):
    response = client.get('/views/home', follow_redirects=True)
    assert response.status_code != 200  # Assuming the login page redirects to the home page after successful login
    assert b'Welcome to the home page' in response.data  # Adjust this assertion based on the content of your home page
# CHATGPT answer, SOME CHANGES BUT THE SAME LOL, XDDDDDDDDDD 
def test_redirect_to_login(client):
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200  # Assuming the login page returns status code 200
    assert b'Login Page' in response.data

def test_user_home(client):
    # Assuming the user is logged in
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Assuming user ID is 1
    response = client.get('/views/home')
    assert response.status_code == 302
    assert b'Wardrobe' in response.data  # Assuming 'Wardrobe' is present in the template


def test_user_newoutfit(client):
    # Assuming the user is logged in
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Assuming user ID is 1
    response = client.get('/views/newoutfit')
    assert response.status_code == 302
    # Add more assertions as needed

def test_user_wardrobe(client):
    # Assuming the user is logged in
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Assuming user ID is 1
    response = client.get('/views/wardrobe')
    assert response.status_code == 302
    # Add more assertions as needed

# from manage import create_tables, drop_tables
# from db import db
# from auth import auth_routes_bp
import sys
import os
import requests
# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# from functional import register, login, logout
from app import app
import pytest
from models import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
        respone = client.get("/")
        assert respone.status_code == 200


def test_register(client):
        response = client.get("/auth/register")
        assert response.status_code ==  200

# @pytest.fixture(scope="module")
# def successful_register_post():
#     url = "http://localhost:8888/auth/register"
#     data = {"email": "Jimbob42@test.ca", "name": "Jimbob", "password": "password"}
#     response = requests.post(url, data=data)
#     return response

# def test_successful_register_post(successful_register_post):
#     assert successful_register_post.status_code == 200  # Assuming successful registration returns status code 200



def test_fail_register_post():
    url = "http://localhost:8888/auth/register"
    # Send a registration request with incomplete or invalid data
    data = {"email": "", "name": "Critize", "password": "password"}  # Empty email
    response = requests.post(url, data=data)
    # Assert that the status code of the response does not indicate a successful registration
    assert response.status_code != 200
    data = {"email": "Critize@test.ca", "name": "", "password": "password"}  # Empty email
    response = requests.post(url, data=data)
    # Assert that the status code of the response does not indicate a successful registration
    assert response.status_code != 200
    data = {"email": "Critize", "name": "Critize", "password": ""}  # Empty email
    response = requests.post(url, data=data)
    # Assert that the status code of the response does not indicate a successful registration
    assert response.status_code != 200
    





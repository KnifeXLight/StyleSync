import sys
import os
import requests

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# from functional import register, login, logout
from app import app
from db import db
import pytest
from models import User
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def test_home(client):
        response = client.get("/")
        assert response.status_code == 200


def test_register(client):
        response = client.get("/auth/register")
        assert response.status_code ==  200

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
        assert user.email == email
        assert user.name == name

        assert check_password_hash(user.password, password)

def test_signup_missing_data(client):
    # Test when required data is missing
    form_data = {
        "email": "",
        "name": "Test User",
        "password": "password123"
    }

    response = client.post("/auth/register", data=form_data, follow_redirects=True)

    assert response.status_code != 200
    # Assuming registration redirects to the same page on validation failure

    # Check if redirected to registration page
    assert b"Registration" in response.data
    # Assuming registration page contains "Registration" text

def test_signup_short_password(client):
    # Test when password is less than 8 characters
    form_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "pass"  # Short password
    }

    response = client.post("/auth/register", data=form_data, follow_redirects=True)

    assert response.status_code != 200
    # Assuming registration redirects to the same page on validation failure

    # Check if redirected to registration page
    assert b"Registration" in response.data
    # Assuming registration page contains "Registration" text
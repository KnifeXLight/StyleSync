import re
import sys
import os
from werkzeug.security import check_password_hash

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from db import db
from models import User

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
    email = "test@test.com"
    name = "Test test"
    password = "testtest"

    form_data = {
        "email": email,
        "name": name,
        "password": password
    }
    
    response = client.post("/auth/register", data=form_data, follow_redirects=True)
    assert response.status_code == 200

    # Check if user is added to the database
    with db.session.no_autoflush:
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
    assert response.status_code == 200
    assert b"Password must be at least 8 characters long" in response.data
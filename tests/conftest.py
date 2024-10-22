from email.mime import image
import pytest
import sys
import os
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import session

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from app import create_app

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from db import db
from models import User, Item, Tag, Category, Filter, Outfit, OutfitItem


@pytest.fixture
def app():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def logged_in_client(client, app):
    with client:
        # Create a test user if it doesn't exist
        with app.app_context():
            test_user = User.query.filter_by(email='test@example.com').first()
            if not test_user:
                test_user = User(name='test user', email='test@example.com', password=generate_password_hash('password'))
                db.session.add(test_user)
                db.session.commit()

            # Log in the test user
            client.post('/auth/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
        
            with client.session_transaction() as sess:
                sess['user_id'] = test_user.id
    return client

@pytest.fixture
def test_item(client, app):
    with client:
        with app.app_context():
            item = Item(name="Test Item", user_id=1, image_url="test_image_url")
            db.session.add(item)
            db.session.commit()
            yield item
            # Ensure item exists before attempting to delete
            item_to_delete = db.session.get(Item, item.id)
            if item_to_delete:
                db.session.delete(item_to_delete)
                db.session.commit()


@pytest.fixture
def failed_login_password(client, app):
    with client:
        # Create a test user if it doesn't exist
        with app.app_context():
            test_user = User.query.filter_by(email='test@example.com').first()
            if not test_user:
                test_user = User(name='test user', email='test@example.com', password=generate_password_hash('password'))
                db.session.add(test_user)
                db.session.commit()
        
            # Log in the test user with the wrong password
            client.post('/auth/login', data={'email': 'test@example.com', 'password': 'wrongpassword'}, follow_redirects=True)
    return client


@pytest.fixture
def multiple_items(client, app):
    with client:
        with app.app_context():
            test_user = User.query.filter_by(email='test@example.com').first()
            if test_user:
                item1 = Item(name="Test Item 1", user_id=test_user.id, image_url="test_image_url_1")
                item2 = Item(name="Test Item 2", user_id=test_user.id, image_url="test_image_url_2")
                db.session.add(item1)
                db.session.add(item2)
                db.session.commit()
                yield [item1, item2]
            else:
                yield []


@pytest.fixture
def update_profile(logged_in_client, app):
    with logged_in_client:
        with app.app_context():
        # Send a POST request to update the profile with the provided data
            response = logged_in_client.post('/views/profile', data={'name': "Updated Name", 'email': "updated@example.com"}, follow_redirects=True)
            return response


@pytest.fixture
def test_user(app):
    with app.app_context():
        user = User(name='Test User', email='test@example.com', password=generate_password_hash('password'))
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()
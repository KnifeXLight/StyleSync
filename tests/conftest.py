import pytest
import sys
import os
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import configure_mappers

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from app import create_app

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from db import db
from models import User, Item

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

# Suppress specific SQLAlchemy warnings
configure_mappers()
from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    if "DELETE" in statement:
        context.execution_options = context.execution_options.union({"suppress_warnings": True})

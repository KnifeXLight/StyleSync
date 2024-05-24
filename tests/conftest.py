import pytest
import sys
import os
from werkzeug.security import generate_password_hash

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from app import create_app

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from db import db
from models import User, Item, Tag, Category, Filter

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
            print(item.image_url)
            print(item.name)
            print(item.id)
            yield item
            # db.session.delete(item)
            # db.session.commit()

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
def setup_filter_data(app, multiple_items):
    with app.app_context():
        # Add categories and filters to the database
        category = Category(name="Test Category")
        filter1 = Filter(name="Test Filter 1", category=category)
        filter2 = Filter(name="Test Filter 2", category=category)
        db.session.add_all([category, filter1, filter2])
        db.session.commit()

        # Add tags to the items for filtering
        item1, item2 = multiple_items
        tag1 = Tag(item_id=item1.id, filter_id=filter1.id, category_id=category.id)
        tag2 = Tag(item_id=item2.id, filter_id=filter2.id, category_id=category.id)
        db.session.add_all([tag1, tag2])
        db.session.commit()

        yield {
            'category': category,
            'filter1': filter1,
            'filter2': filter2,
            'tags': [tag1, tag2]
        }
import pytest
from sqlalchemy import inspect
import sys
import os

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app import app
from db import db
from models import User, Items, Categories, Tags, Outfit, OutfitItems

# * Fixture to set up an in-memory SQLite database for testing. * #

@pytest.fixture
def setup_database():
    # Use an in-memory database for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield
        db.drop_all()


# ------------------- #
# * Test to ensure that all required database tables exist. * #
def test_models_exist(setup_database):
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        assert 'user' in tables
        assert 'items' in tables
        assert 'categories' in tables
        assert 'tags' in tables
        assert 'outfit' in tables
        assert 'outfit_items' in tables


# ------------------- #
# * Test to verify the relationship between the User and Items models. * #
def test_user_items_relationship(setup_database):
    with app.app_context():
        # Create a user
        user = User(name='Test User', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

        # Create an item associated with the user
        item = Items(name='Test Item', image_url='http://example.com/image.png', user_id=user.id)
        db.session.add(item)
        db.session.commit()

        # Verify the relationship
        retrieved_user = db.session.get(User, user.id)
        assert len(retrieved_user.items) == 1
        assert retrieved_user.items[0].name == 'Test Item'
        assert retrieved_user.password == 'password'
        
#! Need to fix the hashing of password in models.py
#! Need to add the relationship between the user and outfit
#! Need to add the relationship between the outfit and outfit_items

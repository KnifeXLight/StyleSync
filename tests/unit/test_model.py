from matplotlib import category
import pytest
from sqlalchemy import inspect
import sys
import os

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app import app
from db import db
from models import User, Item, Category, Tag, Outfit, OutfitItem

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
        assert 'item' in tables
        assert 'category' in tables
        assert 'tag' in tables
        assert 'outfit' in tables
        assert 'outfit_item' in tables


# ------------------- #
# * Test to verify the relationship between the User and Items models. * #
def test_user_items_relationship(setup_database):
    with app.app_context():
        # Create a user
        user = User(name='Test User', email='test@example.com', password='password') # type: ignore
        db.session.add(user)
        db.session.commit()
        
        item = Item(name='Test Item', image_url='http://example.com/image.png', user_id=user.id) # type: ignore
        category = Category(name='Test Category') # type: ignore
        db.session.add(item)
        db.session.add(category)
        db.session.commit()


        # Verify the relationship
        retrieved_user = db.session.get(User, user.id)
        assert len(retrieved_user.items) == 1 # type: ignore
        assert retrieved_user.name == 'Test User' # type: ignore
        assert retrieved_user.items[0].name == 'Test Item' # type: ignore
        assert retrieved_user.password == 'password' # type: ignore
        assert retrieved_user.email == 'test@example.com' # type: ignore


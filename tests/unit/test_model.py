# from matplotlib import category
import pytest
from sqlalchemy import inspect
import sys
import os

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from db import db
from models import User, Item, Category, Tag, Outfit, OutfitItem, Filter


# ------------------- #
# * Test to ensure that all required database tables exist. * #
def test_models_exist(app):
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        assert 'user' in tables
        assert 'item' in tables
        assert 'category' in tables
        assert 'tag' in tables
        assert 'item' in tables
        assert 'category' in tables
        assert 'tag' in tables
        assert 'outfit' in tables
        assert 'outfit_item' in tables
        assert 'outfit_item' in tables


# ------------------- #
# * Test to verify the relationship between the User and Items models. * #
def test_user_items_relationship(app):
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


# ------------------- #
# * Test to verify the relationship between the User and Outfit models. * #

def test_user_get_reset_token(app):
    with app.app_context():
        # Provide mock values for configurations
        app.config['SECRET_KEY'] = 'your_secret_key'
        app.config['SECURITY_PASSWORD_SALT'] = 'your_password_salt'

        # Create a user
        user = User(name='Test User', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

        # Generate reset token
        reset_token = user.get_reset_token()

        # Verify that a token is generated
        assert reset_token is not None

        # Verify that the token can be verified
        verified_user = User.verify_reset_token(reset_token)
        assert verified_user == user


def test_user_set_password(app):
    with app.app_context():
        # Create a user
        user = User(name='Test User', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

        # Change password
        new_password = 'new_password'
        user.set_password(new_password)

        # Verify that the password is updated
        assert user.password != 'password'
        assert user.password != new_password
        # assert user.check_password(new_password)


def test_user_verify_reset_token_invalid(app):
    with app.app_context():
        # Test invalid reset token
        invalid_token = 'invalid_token'
        verified_user = User.verify_reset_token(invalid_token)
        assert verified_user is None


def test_user_relationships(app):
    with app.app_context():
        # Create a user
        user = User(name='Test User', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

        # Create related models
        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()

        # Create Filter with valid category_id
        filter = Filter(name='Test Filter', category_id=category.id)

        # Add Filter to session and commit
        db.session.add(filter)
        db.session.commit()

        # Verify relationships
        assert len(category.filters) == 1
        assert category.filters[0].name == 'Test Filter'
        assert len(filter.tags) == 0
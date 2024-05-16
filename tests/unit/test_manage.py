from sqlalchemy import inspect
import sys
import os

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from manage import create_tables, drop_tables, add_mock_data
from models import User, Item, Category, Tag, Outfit, OutfitItem, Filter
from db import db
from app import app
import pytest

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')))


@pytest.fixture
def setup_database():
    app.config['TESTING'] = True
    # Use an in-memory database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield
        db.drop_all()


def test_drop_tables(setup_database):
    with app.app_context():

        # Drop tables and check they don't exist
        drop_tables()
        inspector = inspect(db.engine)  # Re-inspect to refresh the state
        assert 'user' not in inspector.get_table_names()
        assert 'items' not in inspector.get_table_names()
        assert 'tags' not in inspector.get_table_names()
        assert 'categories' not in inspector.get_table_names()
        assert 'outfit' not in inspector.get_table_names()
        assert 'outfit_items' not in inspector.get_table_names()

def test_create_tables(setup_database):
    with app.app_context():
        # Create tables and check they exist
        create_tables()
        inspector = inspect(db.engine)
        assert 'user' in inspector.get_table_names()
        assert 'item' in inspector.get_table_names()
        assert 'tag' in inspector.get_table_names()
        assert 'category' in inspector.get_table_names()
        assert 'outfit' in inspector.get_table_names()
        assert 'outfit_item' in inspector.get_table_names()

def test_add_mock_data(setup_database):
    with app.app_context():
        drop_tables()
        create_tables()
        add_mock_data()

        # Verify users
        user1 = User.query.filter_by(email="test1@example.com").first()
        user2 = User.query.filter_by(email="test2@example.com").first()
        assert user1 is not None
        assert user2 is not None
        assert user1.name == "Test User 1"
        assert user2.name == "Test User 2"

        # Verify categories
        category1 = Category.query.filter_by(name="Clothing").first()
        category2 = Category.query.filter_by(name="Accessories").first()
        assert category1 is not None
        assert category2 is not None

        # Verify filters
        filter1 = Filter.query.filter_by(name="Color").first()
        filter2 = Filter.query.filter_by(name="Size").first()
        assert filter1 is not None
        assert filter2 is not None

        # Verify items
        item1 = Item.query.filter_by(name="Red Shirt").first()
        item2 = Item.query.filter_by(name="Blue Jeans").first()
        item3 = Item.query.filter_by(name="Green Hat").first()
        assert item1 is not None
        assert item2 is not None
        assert item3 is not None

        # Verify tags
        tag1 = Tag.query.filter_by(
            item_id=item1.id, category_id=category1.id, filter_id=filter1.id).first()
        tag2 = Tag.query.filter_by(
            item_id=item2.id, category_id=category1.id, filter_id=filter2.id).first()
        tag3 = Tag.query.filter_by(
            item_id=item3.id, category_id=category2.id, filter_id=filter1.id).first()
        assert tag1 is not None
        assert tag2 is not None
        assert tag3 is not None

        # Verify outfits
        outfit1 = Outfit.query.filter_by(user_id=user1.id).first()
        outfit2 = Outfit.query.filter_by(user_id=user2.id).first()
        assert outfit1 is not None
        assert outfit2 is not None

        # Verify outfit items
        outfit_item1 = OutfitItem.query.filter_by(
            outfit_id=outfit1.id, item_id=item1.id).first()
        outfit_item2 = OutfitItem.query.filter_by(
            outfit_id=outfit1.id, item_id=item2.id).first()
        outfit_item3 = OutfitItem.query.filter_by(
            outfit_id=outfit2.id, item_id=item3.id).first()
        assert outfit_item1 is not None
        assert outfit_item2 is not None
        assert outfit_item3 is not None

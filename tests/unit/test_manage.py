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
        add_mock_data()
        
        # Verify users
        user1 = User.query.filter_by(email="test1@example.com").first()
        user2 = User.query.filter_by(email="test2@example.com").first()
        assert user1 is not None, "User 1 not created"
        assert user2 is not None, "User 2 not created"
        assert user1.name == "Test User 1"
        assert user2.name == "Test User 2"

        # Verify categories
        category1 = Category.query.filter_by(name="Type").first()
        category2 = Category.query.filter_by(name="Weather").first()
        category3 = Category.query.filter_by(name="Style").first()
        assert category1 is not None, "Category 'Type' not created"
        assert category2 is not None, "Category 'Weather' not created"
        assert category3 is not None, "Category 'Style' not created"

        # Verify filters
        filters = Filter.query.all()
        filter_names = [filter.name for filter in filters]
        expected_filters = [
            'Upper Wear', 'Leg Wear', 'Shoes', 'Accessories',
            'Sunny', 'Windy', 'Snowy', 'Clear', 'Rainy',
            'Casual', 'Street', 'Formal', 'Sporty', 'Classic', 'Fancy'
        ]
        for filter_name in expected_filters:
            assert filter_name in filter_names, f"Filter '{filter_name}' not created"

        # Verify items
        items = Item.query.all()
        item_names = [item.name for item in items]
        expected_items = [
            'beige tote', 'black purse', 'ghostbracelet3', 'ghosthat2', 'olive green tote', 'white cap',
            'black leather A-line skirt', 'black leather H-line skirt', 'dark washed denim bell jeans',
            'light washed denim skirt', 'dark washed denim short', 'dark washed jeans', 'light pink tennis skirt',
            'black short sleeve dress', 'black sleeveless dress', 'black knee high boots', 'black leather loafers',
            'black stilettos', 'brown flat sandals', 'camel ankle boots', 'black scarf', 'black socks',
            'ghostbracelet2', 'ghosthat3', 'ghosthat4', 'grey scarf', 'red tie', 'beige pants', 'black flip flops',
            'black leather dress shoes', 'black dress shirt', 'black hoodie', 'black leather jacket', 'black nike hoodie',
            'black suit top and tie', 'black suit top', 'blue sweater', 'dusty blue sweater', 'white dress shirt'
        ]
        for item_name in expected_items:
            assert item_name in item_names, f"Item '{item_name}' not created"

        # Verify tags
        tags = Tag.query.all()
        assert len(tags) == 90, f"Expected 90 tags, but got {len(tags)}"

        # Verify outfits
        outfits = Outfit.query.all()
        assert len(outfits) == 4, f"Expected 4 outfits, but got {len(outfits)}"

        # Verify outfit items
        outfit_items = OutfitItem.query.all()
        assert len(outfit_items) == 16, f"Expected 16 outfit items, but got {len(outfit_items)}"
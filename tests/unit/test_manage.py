from sqlalchemy import inspect
import sys
import os

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from manage import create_tables, drop_tables, add_mock_data
from models import User, Item, Category, Tag, Outfit, OutfitItem, Filter
from db import db

def test_drop_tables(app):
    with app.app_context():
        # Drop tables and check they don't exist
        drop_tables(app)
        inspector = inspect(db.engine)  # Re-inspect to refresh the state
        assert 'user' not in inspector.get_table_names()
        assert 'items' not in inspector.get_table_names()
        assert 'tags' not in inspector.get_table_names()
        assert 'categories' not in inspector.get_table_names()
        assert 'outfit' not in inspector.get_table_names()
        assert 'outfit_items' not in inspector.get_table_names()

def test_create_tables(app):
    with app.app_context():
        # Create tables and check they exist
        create_tables(app)
        inspector = inspect(db.engine)
        assert 'user' in inspector.get_table_names()
        assert 'item' in inspector.get_table_names()
        assert 'tag' in inspector.get_table_names()
        assert 'category' in inspector.get_table_names()
        assert 'outfit' in inspector.get_table_names()
        assert 'outfit_item' in inspector.get_table_names()


def test_add_mock_data(app):
    with app.app_context():
        add_mock_data(app)
        
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


# ---------------------------- #

# ! Test is working outside of application context
# import sys
# from unittest.mock import patch
# from manage import create_tables, drop_tables, add_mock_data

# @patch('manage.create_app')
# def test_create_tables_arg(mock_create_app):
#     mock_app = mock_create_app.return_value
#     with mock_app.app_context():
#         with patch.object(sys, 'argv', ['manage.py', 'create']):
#             create_tables(mock_app)
#             # Add your assertions here to check if tables are created successfully

# @patch('manage.create_app')
# def test_drop_tables_arg(mock_create_app):
#     mock_app = mock_create_app.return_value
#     with mock_app.app_context():
#         with patch.object(sys, 'argv', ['manage.py', 'drop']):
#             drop_tables(mock_app)
#             # Add your assertions here to check if tables are dropped successfully

# @patch('manage.create_app')
# def test_add_mock_data_arg(mock_create_app):
#     mock_app = mock_create_app.return_value
#     with mock_app.app_context():
#         with patch.object(sys, 'argv', ['manage.py', 'seed']):
#             add_mock_data(mock_app)
#             # Add your assertions here to check if mock data is added successfully

# @patch('manage.create_app')
# def test_reset_tables_arg(mock_create_app):
#     mock_app = mock_create_app.return_value
#     with mock_app.app_context():
#         with patch.object(sys, 'argv', ['manage.py', 'reset']):
#             drop_tables(mock_app)
#             create_tables(mock_app)
#             add_mock_data(mock_app)
#             # Add your assertions here to check if tables are reset successfully

# @patch('manage.create_app')
# def test_invalid_command_arg(mock_create_app):
#     with patch.object(sys, 'argv', ['manage.py', 'invalid']):
#         assert "Invalid command. Please use 'create', 'drop', or 'seed' as arguments"

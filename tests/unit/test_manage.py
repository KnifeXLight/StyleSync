import pytest
from sqlalchemy import inspect
import sys
import os

# Add the app_folder to the system path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app import app
from db import db
from manage import create_tables, drop_tables

@pytest.fixture
def setup_database():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

def test_create_and_drop_tables(setup_database):
    with app.app_context():
        inspector = inspect(db.engine)

        # Drop tables and check they don't exist
        drop_tables()
        inspector = inspect(db.engine)  # Re-inspect to refresh the state
        assert 'user' not in inspector.get_table_names()
        assert 'items' not in inspector.get_table_names()
        assert 'tags' not in inspector.get_table_names()
        assert 'categories' not in inspector.get_table_names()
        assert 'outfit' not in inspector.get_table_names()
        assert 'outfit_items' not in inspector.get_table_names()
        assert 'user' not in inspector.get_table_names()
        assert 'items' not in inspector.get_table_names()
        assert 'tags' not in inspector.get_table_names()
        assert 'categories' not in inspector.get_table_names()
        assert 'outfit' not in inspector.get_table_names()
        assert 'outfit_items' not in inspector.get_table_names()

        # Create tables and check they exist
        create_tables()
        inspector = inspect(db.engine)
        assert 'user' in inspector.get_table_names()
        assert 'items' in inspector.get_table_names()
        assert 'tags' in inspector.get_table_names()
        assert 'categories' in inspector.get_table_names()
        assert 'outfit' in inspector.get_table_names()
        assert 'outfit_items' in inspector.get_table_names()

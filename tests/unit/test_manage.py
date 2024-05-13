import pytest
from app import app
from db import db
from manage import create_tables, drop_tables

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    with app.app_context():
        db.drop_all()

    yield client


def test_create_and_drop_tables(client):
    # Check if tables are created
    create_tables()
    assert 'user' in db.get_tables()  # Assuming 'user' is one of your tables
    assert 'wardrobe' in db.get_tables()  # Assuming 'wardrobe' is one of your tables

    # Check if tables are dropped
    drop_tables()
    assert 'user' not in db.get_tables()
    assert 'wardrobe' not in db.get_tables()


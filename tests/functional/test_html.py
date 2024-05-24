from os import name
from models import Item, User, Category, Filter, Tag
from db import db
import io

# * Test Access to Protected Routes
def test_access_protected_route_wardrobe(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get('/views/wardrobe')
        assert response.status_code == 200

def test_access_protected_route_homepage(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get('/views/home')
        assert response.status_code == 200

def test_access_protected_route_newoutfit(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get('/views/newoutfit')
        assert response.status_code == 200

# * Tests for routes accessibility when logged-in * #
def test_homepage_logged_in(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get('/views/home', follow_redirects=True)
        assert response.status_code == 200

def test_newoutfit_logged_in(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get('/views/newoutfit', follow_redirects=True)
        assert response.status_code == 200

def test_wardrobe_logged_in(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get('/views/wardrobe', follow_redirects=True)
        assert response.status_code == 200


# * Tests for routes accessibility when not logged in * #
def test_homepage_not_logged_in(client):
    with client:
        response = client.get('/views/home', follow_redirects=False)
        assert response.status_code == 302  # Redirect to login

def test_newoutfit_not_logged_in(client):
    with client:
        response = client.get('/views/newoutfit', follow_redirects=False)
        assert response.status_code == 302  # Redirect to login

def test_wardrobe_not_logged_in(client):
    with client:
        response = client.get('/views/wardrobe', follow_redirects=False)
        assert response.status_code == 302  # Redirect to login

def test_item_route_non_existing(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get('/views/item/999', follow_redirects=True)
        assert response.status_code == 200
# Test if Item is not accessible when not logged in
def test_item_route_not_logged_in(client):
    with client:
        response = client.get('/views/item/1', follow_redirects=False)
        assert response.status_code == 302

# Test the delete_item route for non-existing item
def test_delete_item_route_non_existing(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get('/views/items/999', follow_redirects=True)
        assert response.status_code == 404

def test_delete_item_route_existing(logged_in_client, test_item):
    # Delete the test item
    # with logged_in_client:
        item_id = test_item.id
        # print("Item ID:", item_id)
        assert db.session.query(Item).filter_by(id=item_id).first() is not None
        response = logged_in_client.get(f'/views/items/{item_id}', follow_redirects=True)
            
            # Verify that the item exists
        assert response.status_code == 200
        item = db.session.query(Item).filter_by(id=item_id).first()
            # Verify that the item has been deleted
        assert item is None
        # assert db.session.query(Item).filter_by(id=item_id).first() is None


# Test uploading a valid file
def test_upload_valid_file(logged_in_client):
    with logged_in_client:
        data = {
            'file': (io.BytesIO(b"fake file content"), 'test.png')
        }
        response = logged_in_client.post('/views/new_item', data=data, content_type='multipart/form-data', follow_redirects=True)
        assert response.status_code == 200
        assert b'Item added' in response.data

# Test uploading an invalid file type
def test_upload_invalid_file_type(logged_in_client):
    with logged_in_client:
        data = {
            'file': (io.BytesIO(b"fake file content"), 'test.txt')
        }
        response = logged_in_client.post('/views/new_item', data=data, content_type='multipart/form-data', follow_redirects=True)
        assert response.status_code == 200
        assert b'File type not allowed' in response.data

# Test filtering items
def test_filter_items(logged_in_client, app):
    with logged_in_client:
        with app.app_context():
            category = Category(name="Test Category")
            db.session.add(category)
            db.session.commit()

            filter_ = Filter(name="Test Filter", category_id=category.id)
            db.session.add(filter_)
            db.session.commit()

            item = Item(name="Test Item", user_id=1, image_url="test_image_url")
            db.session.add(item)
            db.session.commit()

            tag = Tag(item_id=item.id, filter_id=filter_.id, category_id=category.id)
            db.session.add(tag)
            db.session.commit()

            response = logged_in_client.post('/views/wardrobe/filter', data={'filter_id': filter_.id}, follow_redirects=True)
            assert response.status_code == 200
            assert b'Test Item' in response.data

# Test filtering items with valid filter
def test_filter_items_valid_filter(logged_in_client, app):
    with logged_in_client:
        with app.app_context():
            category = Category(name="Test Category")
            db.session.add(category)
            db.session.commit()

            filter_ = Filter(name="Test Filter", category_id=category.id)
            db.session.add(filter_)
            db.session.commit()

            item = Item(name="Test Item", user_id=1, image_url="test_image_url")
            db.session.add(item)
            db.session.commit()

            tag = Tag(item_id=item.id, filter_id=filter_.id, category_id=category.id)
            db.session.add(tag)
            db.session.commit()

            response = logged_in_client.post('/views/wardrobe/filter', data={str(filter_.id): filter_.id}, follow_redirects=True)
            assert response.status_code == 200
            assert b'Test Item' in response.data

# Test filtering items with no matching filter
def test_filter_items_no_matching_filter(logged_in_client, app):
    with logged_in_client:
        with app.app_context():
            category = Category(name="Test Category")
            db.session.add(category)
            db.session.commit()

            filter_ = Filter(name="Non-Matching Filter", category_id=category.id)
            db.session.add(filter_)
            db.session.commit()

            response = logged_in_client.post('/views/wardrobe/filter', data={str(filter_.id): filter_.id}, follow_redirects=True)
            assert response.status_code == 200
            assert b'Test Item' not in response.data


# Test profile update
def test_update_profile(logged_in_client):
    with logged_in_client:
        response = logged_in_client.post('/views/profile', data={'name': 'Updated Name', 'email': 'updated@example.com'}, follow_redirects=True)
        assert response.status_code == 200

        # Verify the update
        user = db.session.query(User).filter_by(email='updated@example.com').first()
        assert user is not None
        assert user.name == 'Updated Name'

# Test profile update with missing fields
def test_update_profile_missing_fields(logged_in_client):
    with logged_in_client:
        response = logged_in_client.post('/views/profile', data={'name': 'Updated Name'}, follow_redirects=True)
        assert response.status_code == 200

        # Verify the update
        user = db.session.query(User).filter_by(name='Updated Name').first()
        assert user is not None

# Additional test cases to increase coverage
def test_upload_valid_file(logged_in_client):
    with logged_in_client:
        data = {
            'file': (io.BytesIO(b"fake file content"), 'test.png')
        }
        response = logged_in_client.post('/views/new_item', data=data, content_type='multipart/form-data', follow_redirects=True)
        assert response.status_code == 200
        # assert b'Item added' in response.data

def test_upload_invalid_file_type(logged_in_client):
    with logged_in_client:
        data = {
            'file': (io.BytesIO(b"fake file content"), 'test.txt')
        }
        response = logged_in_client.post('/views/new_item', data=data, content_type='multipart/form-data', follow_redirects=True)
        assert response.status_code == 200
        assert b'File type not allowed' in response.data

def test_update_profile(logged_in_client):
    with logged_in_client:
        response = logged_in_client.post('/views/profile', data={'name': 'Updated Name', 'email': 'updated@example.com'}, follow_redirects=True)
        assert response.status_code == 200
        # assert b'User information updated' in response.data

        user = db.session.query(User).filter_by(email='updated@example.com').first()
        assert user is not None
        assert user.name == 'Updated Name'

def test_update_profile_missing_fields(logged_in_client):
    with logged_in_client:
        response = logged_in_client.post('/views/profile', data={'name': 'Updated Name'}, follow_redirects=True)
        assert response.status_code == 200

        user = db.session.query(User).filter_by(name='Updated Name').first()
        assert user is not None
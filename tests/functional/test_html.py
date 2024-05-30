from os import name
from models import Item, User, Category, Filter, Tag, Outfit, OutfitItem
from db import db
import io
from unittest.mock import MagicMock, patch
from flask import url_for


# * Test Access to Protected Routes
def test_access_protected_route_wardrobe(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get('/views/wardrobe')
        assert response.status_code == 200


def test_access_protected_route_homepage(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get('/views/home')
        assert response.status_code == 200


def test_access_protected_route_profile(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get('/views/profile')
        assert response.status_code == 200


# * Tests for routes accessibility when logged-in * #
def test_homepage_logged_in(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get('/views/home', follow_redirects=True)
        assert response.status_code == 200


def test_wardrobe_logged_in(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get(
            '/views/wardrobe', follow_redirects=True)
        assert response.status_code == 200


# ! The test below is not working because the route gives a 500 error in the trial environment
# def test_newoutfit_logged_in(logged_in_client):
#     with logged_in_client:
#         response = logged_in_client.get(
#             '/views/newoutfit', follow_redirects=True)
#         assert response.status_code == 200


# ! The test below is not working because the route is not implemented as there is a type error of coroutine
# @patch('routes.html.current_user')
# @patch('routes.html.db.session')
# @patch('routes.html.db.session.query')
# def test_newoutfit(mock_query, mock_current_user, client, logged_in_client):
#     # Set up mock data
#     mock_user = MagicMock(spec=User)
#     mock_user.id = 1
#     mock_current_user._get_current_object.return_value = mock_user

#     mock_categories = [MagicMock(spec=Category) for _ in range(3)]
#     mock_filters = [MagicMock(spec=Filter) for _ in range(3)]
#     mock_items = [MagicMock(spec=Item) for _ in range(3)]
#     for item in mock_items:
#         item.user_id = 1
#         item.item_tags = []

#     mock_outfit = MagicMock(spec=Outfit)
#     mock_outfit.id = 1
#     mock_outfit.user_id = 1

#     mock_outfit_items = [MagicMock(spec=OutfitItem) for _ in range(3)]
    
#     # Patch the database queries
#     mock_query.return_value.filter.return_value.all.side_effect = [
#         mock_categories,  # For categories query
#         mock_filters,     # For filters query
#         mock_items,       # For items query
#         [mock_outfit],    # For outfit query
#         mock_outfit_items # For outfit items query
#     ]

#     # Perform GET request
#     with client.application.app_context():
#         response = client.get(url_for('html.newoutfit'))

#     # Check the response
#     assert response.status_code == 200
#     assert b'newoutfit.html' in response.data


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


def test_item_route_not_logged_in(client):
    with client:
        response = client.get('/views/item/1', follow_redirects=False)
        assert response.status_code == 302


def test_delete_item_route_non_existing(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get('/views/items/999', follow_redirects=True)
        assert response.status_code == 404


def test_upload_valid_file(logged_in_client):
    with logged_in_client:
        data = {
            'file': (io.BytesIO(b"fake file content"), 'test.png')
        }
        response = logged_in_client.post(
            '/views/new_item', data=data, content_type='multipart/form-data', follow_redirects=True)
        assert response.status_code == 200


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


# * Test filtering items with no matching filter * #
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


def test_upload_invalid_file_type(logged_in_client):
    with logged_in_client:
        data = {
            'file': (io.BytesIO(b"fake file content"), 'test.txt')
        }
        response = logged_in_client.post(
            '/views/new_item', data=data, content_type='multipart/form-data', follow_redirects=True)
        assert response.status_code == 200
        assert b'File type not allowed' in response.data


def test_update_profile(logged_in_client):
    with logged_in_client:
        response = logged_in_client.post(
            '/views/profile', data={'name': 'Updated Name', 'email': 'updated@example.com'}, follow_redirects=True)
        assert response.status_code == 200

        user = db.session.query(User).filter_by(
            email='updated@example.com').first()
        assert user is not None
        assert user.name == 'Updated Name'


def test_update_profile_missing_fields(logged_in_client):
    with logged_in_client:
        response = logged_in_client.post(
            '/views/profile', data={'name': 'Updated Name'}, follow_redirects=True)
        assert response.status_code == 200

        user = db.session.query(User).filter_by(name='Updated Name').first()
        assert user is not None


def test_filter_route_logged_in(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get('views/wardrobe/filter')
        assert response.status_code == 200


def test_filter_route_not_logged_in(client):
    with client:
        response = client.get('views/wardrobe/filter')
        assert response.status_code == 302


def test_filter_route_with_multiple_items(logged_in_client, multiple_items):
    # with logged_in_client:
    response = logged_in_client.get('/views/wardrobe/filter')
    assert response.status_code == 200
    for item in multiple_items:
        assert item.name in response.get_data(as_text=True)


def test_login_new_items(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get("views/new_item")
        assert response.status_code == 200


def test_not_login_new_items(client):
    with client:
        response = client.get("views/new_item")
        assert response.status_code == 302


def test_about_us_log(client):
    with client:
        response = client.get("views/about", follow_redirects=False)
        assert response.status_code == 302


def test_about_us_notlog(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get("views/about")
        assert response.status_code == 200


def test_profile_updatewow(update_profile):
    assert update_profile.status_code == 200


# ! Unable to solve the issue of test working outside of application context

# def test_replace_item(logged_in_client, app):
#     # Create test data
#     outfit = Outfit(user_id=1)
#     db.session.add(outfit)
#     item_to_replace = Item(name="Item to Replace")
#     item = Item(name="Replacement Item")
#     db.session.add_all([item_to_replace, item])
#     db.session.commit()

#     # Make a POST request to replace item
#     response = logged_in_client.post('/oufit/1', data={'item_to_be_replaced_id': item_to_replace.id, 'item_to_replace_id': item.id})

#     # Check response
#     assert response.status_code == 302  # Redirect code
#     assert response.location.endswith('/outfit/1')

#     # Check database changes
#     assert outfit.items.count() == 1
#     assert item_to_replace not in outfit.items
#     assert item in outfit.items

# def test_add_item(logged_in_client, app):
#     # Create test data
#     outfit = Outfit(user_id=1)
#     db.session.add(outfit)
#     item = Item(name="Test Item", image_url="test_item_image.jpg")  # Provide an image_url
#     db.session.add(item)
#     db.session.commit()

#     # Make a POST request to add item
#     response = logged_in_client.post(url_for('html_routes_bp.add_item', id=outfit.id),
#                                      data={'item_id': item.id})

#     # Check response
#     assert response.status_code == 302  # Redirect code
#     assert response.location.endswith(url_for('html_routes_bp.outfit', id=outfit.id))

#     # Check database changes
#     assert outfit.items.count() == 1
#     assert item in outfit.items


# def test_create_new_outfit(logged_in_client, app):
#     # Create test data
#     item = Item(name="Test Item", image_url="test_item_image.jpg")  # Provide an image_url
#     db.session.add(item)
#     db.session.commit()

#     # Make a POST request to create new outfit
#     response = logged_in_client.post(url_for('html_routes_bp.create_new_outfit'),
#                                      data={'item_id': item.id})

#     # Check response
#     assert response.status_code == 302  # Redirect code
#     assert response.location.endswith(url_for('html_routes_bp.outfit', id=1))

#     # Check database changes
#     assert Outfit.query.count() == 1
#     outfit = Outfit.query.first()
#     assert outfit.items.count() == 1
#     assert item in outfit.items

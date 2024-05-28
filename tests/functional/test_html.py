from os import name
from models import Item, User, Category, Filter, Tag, Outfit, OutfitItem
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

def test_newoutfit_logged_in(logged_in_client):
    with logged_in_client:
        response = logged_in_client.get(
            '/views/newoutfit', follow_redirects=True)
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


"""
This code was used to check if it goes 204 if nothing was inputted
However, because of response = logged_in_client.post(url_for
the post immediately triggers the if request.method == "POST":
block of the route, so it auto runs no matter what.
It then updates the database if no data was input
but also does not change anything i believe.
"""
# def test_profile_post(app, logged_in_client):
#     with app.test_request_context(method='POST'):
#         # Call the route function directly
#         response = app.html_routes_bp.change_name_profile()

#     # Assert that the response status code is 204
#     assert response.status_code == 204


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


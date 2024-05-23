from models import Item
from db import db

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


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
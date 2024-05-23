def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_register_route(client):
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_signup(client):
    response = client.post('/auth/register', data={'name': 'Test User', 'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    assert b'Login' in response.data
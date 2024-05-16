# # test_functional.py
# import requests

# # Function to simulate user registration
# def register(email, name, password):
#     url = "http://localhost:8888/auth/register"
#     data = {"email": email, "name": name, "password": password}
#     response = requests.post(url, data=data)
#     return response.status_code

# # Function to simulate user login
# def login(email, password):
#     url = "http://localhost:8888/auth/login"
#     data = {"email": email, "password": password}
#     response = requests.post(url, data=data)
#     return response.status_code

# # Function to simulate user logout
# def logout():
#     url = "http://localhost:8888/auth/logout"
#     response = requests.get(url)
#     return response.status_code

# # Test case for functional testing of user registration, login, and logout
# def test_register_login_logout():
#     email = "test@example.com"
#     name = "Test User"
#     password = "password"

#     # Simulate registration
#     register_status_code = register(email, name, password)
    
#     # Simulate login
#     login_status_code = login(email, password)

#     # Simulate logout
#     logout_status_code = logout()

#     # Check registration, login, and logout status codes
#     assert register_status_code == 200
#     assert login_status_code == 200
#     assert logout_status_code == 200

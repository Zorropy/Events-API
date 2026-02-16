import pytest
import requests
import time

# Base URL for the running Flask application
BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture
def auth_token():
    """
    Fixture to provide a valid JWT access token for authenticated requests.
    - Registers a new unique user.
    - Authenticates the user to retrieve the access token.
    - Returns the JWT as a string.
    """
    unique_user = f"fixture_user_{int(time.time())}"
    password = "password123"

    # Step 1: Register a new test user
    requests.post(f"{BASE_URL}/api/auth/register", json={
        "username": unique_user,
        "password": password
    })

    # Step 2: Login to obtain the JWT token
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": unique_user,
        "password": password
    })

    # Return the token string to be used in other tests
    return response.json().get("access_token")
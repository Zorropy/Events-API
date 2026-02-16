import requests
import time

BASE_URL = "http://127.0.0.1:5000"


# 1. API Availability
def test_health_endpoint():
    """Verify that the API health endpoint is reachable and returns healthy status"""
    response = requests.get(f"{BASE_URL}/api/health")
    assert response.status_code == 200
    assert response.json().get("status") == "healthy"


# 2. User Registration
def test_register_user():
    """Verify that a new user can be registered with a unique username"""
    unique_name = f"user_{int(time.time())}"
    payload = {"username": unique_name, "password": "testpassword123"}
    response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)

    assert response.status_code == 201
    assert response.json().get("user").get("username") == unique_name


# 3. User Authentication
def test_login_returns_jwt():
    """Verify that valid credentials return a JWT access token"""
    unique_name = f"login_{int(time.time())}"
    requests.post(f"{BASE_URL}/api/auth/register", json={"username": unique_name, "password": "password"})

    response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": unique_name, "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()


# 4. Event Creation (Happy Path)
def test_create_event_success(auth_token):
    """Verify that an authenticated user can create a new event"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "title": "Automated Test Event",
        "date": "2026-05-20T18:00:00",
        "location": "Duisburg"
    }
    response = requests.post(f"{BASE_URL}/api/events", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json().get("title") == "Automated Test Event"


# 5. Event Creation (Unauthorized)
def test_create_event_unauthorized():
    """Ensure event creation fails without a valid authentication token"""
    response = requests.post(f"{BASE_URL}/api/events", json={"title": "No Token"})
    assert response.status_code == 401


# 6. Event Creation (Validation Error)
def test_create_event_missing_title(auth_token):
    """Ensure event creation fails when the required title is missing"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {"date": "2026-05-20T18:00:00"}
    response = requests.post(f"{BASE_URL}/api/events", json=payload, headers=headers)
    assert response.status_code == 400


# 7. Event Listing
def test_get_all_events():
    """Verify that the events list endpoint returns a 200 status and a list object"""
    response = requests.get(f"{BASE_URL}/api/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 8. Single Event Retrieval
def test_get_single_event(auth_token):
    """Verify that a specific event can be retrieved by its ID"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Create an event to retrieve
    res = requests.post(f"{BASE_URL}/api/events", json={"title": "Find Me", "date": "2026-01-01T10:00:00"},
                        headers=headers)
    event_id = res.json().get("id")

    response = requests.get(f"{BASE_URL}/api/events/{event_id}")
    assert response.status_code == 200
    assert response.json().get("id") == event_id


# 9. Resource Not Found
def test_get_event_not_found():
    """Ensure a 404 error is returned for non-existent event IDs"""
    response = requests.get(f"{BASE_URL}/api/events/99999")
    assert response.status_code == 404


# 10. Authentication Failure
def test_login_invalid_password():
    """Ensure login fails with incorrect credentials"""
    response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "admin", "password": "wrongpassword"})
    assert response.status_code == 401
# tests/test_models.py
import pytest
from models import User

def test_user_password_hashing():
    """
    Verify password hashing logic:
    - Ensure passwords are not stored in plaintext.
    - Validate password verification returns True for correct credentials.
    - Validate password verification returns False for incorrect credentials.
    """
    # Initialize test user
    user = User(username="TestUser")

    # Set password (triggers internal hashing)
    user.set_password("secret123")

    # Assert password is not stored as plaintext
    assert user.password_hash != "secret123"

    # Verify correct password authentication
    assert user.check_password("secret123") is True

    # Verify failed authentication with incorrect password
    assert user.check_password("wrong_password") is False
from app.auth import get_password_hash, verify_password, create_access_token, create_reset_token, decode_token


def test_password_hashing():
    password = "1234567"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True


def test_create_access_token():
    token = create_access_token({"sub": "test@example.com"})
    payload = decode_token(token)
    assert payload["sub"] == "test@example.com"
    assert payload["scope"] == "access_token"


def test_create_reset_token():
    token = create_reset_token("reset@example.com")
    payload = decode_token(token)
    assert payload["sub"] == "reset@example.com"
    assert payload["scope"] == "password_reset"
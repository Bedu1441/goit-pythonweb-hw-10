from app.auth import create_reset_token


def test_signup(client):
    response = client.post(
        "/auth/signup",
        json={
            "email": "user1@example.com",
            "username": "user1",
            "password": "1234567",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user1@example.com"
    assert data["role"] == "user"


def test_login(client):
    client.post(
        "/auth/signup",
        json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "1234567",
        },
    )
    response = client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "1234567"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_request_password_reset(client):
    client.post(
        "/auth/signup",
        json={
            "email": "reset@example.com",
            "username": "resetuser",
            "password": "1234567",
        },
    )
    response = client.post("/auth/request_password_reset", json={"email": "reset@example.com"})
    assert response.status_code == 200
    assert "message" in response.json()


def test_reset_password(client):
    client.post(
        "/auth/signup",
        json={
            "email": "change@example.com",
            "username": "changeuser",
            "password": "1234567",
        },
    )
    token = create_reset_token("change@example.com")
    response = client.post(
        f"/auth/reset_password/{token}",
        json={"new_password": "7654321"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password has been reset successfully"
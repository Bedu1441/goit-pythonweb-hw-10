def test_signup_duplicate_email(client):
    payload = {
        "email": "dup@example.com",
        "username": "dupuser",
        "password": "1234567",
    }

    response_1 = client.post("/auth/signup", json=payload)
    response_2 = client.post("/auth/signup", json=payload)

    assert response_1.status_code == 201
    assert response_2.status_code == 409
    assert response_2.json()["detail"] == "Account already exists"


def test_login_invalid_password(client):
    client.post(
        "/auth/signup",
        json={
            "email": "badlogin@example.com",
            "username": "badlogin",
            "password": "1234567",
        },
    )

    response = client.post(
        "/auth/login",
        data={"username": "badlogin@example.com", "password": "wrongpass"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_reset_password_invalid_token(client):
    response = client.post(
        "/auth/reset_password/invalidtoken",
        json={"new_password": "7654321"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_refresh_token_returns_new_access_token(client):
    client.post(
        "/auth/signup",
        json={
            "email": "refresh@example.com",
            "username": "refreshuser",
            "password": "1234567",
        },
    )

    login_response = client.post(
        "/auth/login",
        data={"username": "refresh@example.com", "password": "1234567"},
    )

    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "refresh_token" in login_data

    refresh_response = client.post(
        "/auth/refresh",
        json={"refresh_token": login_data["refresh_token"]},
    )

    assert refresh_response.status_code == 200
    refresh_data = refresh_response.json()
    assert "access_token" in refresh_data
    assert refresh_data["token_type"] == "bearer"


def test_refresh_with_invalid_token(client):
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "invalid.refresh.token"},
    )

    assert response.status_code == 401
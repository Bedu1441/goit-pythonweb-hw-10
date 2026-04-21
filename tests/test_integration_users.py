from app import crud, schemas


def get_token(client, email, password):
    response = client.post("/auth/login", data={"username": email, "password": password})
    return response.json()["access_token"]


def test_me(client):
    client.post(
        "/auth/signup",
        json={
            "email": "me@example.com",
            "username": "meuser",
            "password": "1234567",
        },
    )
    token = get_token(client, "me@example.com", "1234567")
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"


def test_admin_can_update_default_avatar(client, session):
    admin = crud.create_user(
        session,
        schemas.UserCreate(
            email="admin@example.com",
            username="adminuser",
            password="1234567",
        ),
        role="admin",
    )

    token = get_token(client, admin.email, "1234567")
    response = client.patch(
        "/users/default-avatar",
        json={"avatar_url": "https://example.com/avatar.png"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["avatar"] == "https://example.com/avatar.png"


def test_user_cannot_update_default_avatar(client):
    client.post(
        "/auth/signup",
        json={
            "email": "simple@example.com",
            "username": "simpleuser",
            "password": "1234567",
        },
    )
    token = get_token(client, "simple@example.com", "1234567")
    response = client.patch(
        "/users/default-avatar",
        json={"avatar_url": "https://example.com/avatar.png"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
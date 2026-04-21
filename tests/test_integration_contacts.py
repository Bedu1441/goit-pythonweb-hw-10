def get_token(client, email, password):
    response = client.post("/auth/login", data={"username": email, "password": password})
    return response.json()["access_token"]


def test_create_contact(client):
    client.post(
        "/auth/signup",
        json={
            "email": "contacts@example.com",
            "username": "contactsuser",
            "password": "1234567",
        },
    )
    token = get_token(client, "contacts@example.com", "1234567")
    response = client.post(
        "/contacts/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@doe.com",
            "phone": "123456789",
            "birthday": "2000-01-01",
            "additional_data": "friend",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["first_name"] == "John"


def test_get_contacts(client):
    client.post(
        "/auth/signup",
        json={
            "email": "list@example.com",
            "username": "listuser",
            "password": "1234567",
        },
    )
    token = get_token(client, "list@example.com", "1234567")

    client.post(
        "/contacts/",
        json={
            "first_name": "Anna",
            "last_name": "Lee",
            "email": "anna@lee.com",
            "phone": "123456789",
            "birthday": "2001-01-01",
            "additional_data": "colleague",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get("/contacts/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) >= 1
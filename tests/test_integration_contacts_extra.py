def get_token(client, email, password):
    response = client.post("/auth/login", data={"username": email, "password": password})
    return response.json()["access_token"]


def test_get_missing_contact(client):
    client.post(
        "/auth/signup",
        json={
            "email": "missing@example.com",
            "username": "missinguser",
            "password": "1234567",
        },
    )

    token = get_token(client, "missing@example.com", "1234567")
    response = client.get(
        "/contacts/9999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Contact not found"


def test_update_missing_contact(client):
    client.post(
        "/auth/signup",
        json={
            "email": "upmissing@example.com",
            "username": "upmissinguser",
            "password": "1234567",
        },
    )

    token = get_token(client, "upmissing@example.com", "1234567")
    response = client.put(
        "/contacts/9999",
        json={"first_name": "Updated"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Contact not found"


def test_delete_missing_contact(client):
    client.post(
        "/auth/signup",
        json={
            "email": "delmissing@example.com",
            "username": "delmissinguser",
            "password": "1234567",
        },
    )

    token = get_token(client, "delmissing@example.com", "1234567")
    response = client.delete(
        "/contacts/9999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Contact not found"


def test_search_contacts_returns_result(client):
    client.post(
        "/auth/signup",
        json={
            "email": "searchplus@example.com",
            "username": "searchplususer",
            "password": "1234567",
        },
    )

    token = get_token(client, "searchplus@example.com", "1234567")

    client.post(
        "/contacts/",
        json={
            "first_name": "Anna",
            "last_name": "Taylor",
            "email": "anna.taylor@example.com",
            "phone": "123456789",
            "birthday": "2001-01-01",
            "additional_data": "friend",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        "/contacts/search?query=Anna",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["first_name"] == "Anna"
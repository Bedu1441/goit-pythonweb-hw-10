from app import crud, schemas


def test_create_user(session):
    body = schemas.UserCreate(
        email="unit@example.com",
        username="unituser",
        password="1234567",
    )
    user = crud.create_user(session, body)
    assert user.id is not None
    assert user.email == "unit@example.com"
    assert user.role == "user"


def test_create_contact(session):
    user_body = schemas.UserCreate(
        email="owner@example.com",
        username="owneruser",
        password="1234567",
    )
    user = crud.create_user(session, user_body)

    contact_body = schemas.ContactCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="123456789",
        birthday=None,
        additional_data="friend",
    )
    contact = crud.create_contact(session, contact_body, user.id)
    assert contact.id is not None
    assert contact.owner_id == user.id


def test_search_contacts(session):
    user_body = schemas.UserCreate(
        email="search@example.com",
        username="searchuser",
        password="1234567",
    )
    user = crud.create_user(session, user_body)

    contact_body = schemas.ContactCreate(
        first_name="Alice",
        last_name="Smith",
        email="alice@example.com",
        phone="000111222",
        birthday=None,
        additional_data=None,
    )
    crud.create_contact(session, contact_body, user.id)

    result = crud.search_contacts(session, user.id, "Ali")
    assert len(result) == 1
    assert result[0].first_name == "Alice"
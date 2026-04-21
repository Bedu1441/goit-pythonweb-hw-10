"""
CRUD functions for users and contacts.
"""

from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import extract

from app import models, schemas
from app.auth import get_password_hash


def get_user_by_email(db: Session, email: str):
    """
    Get user by email.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, body: schemas.UserCreate, avatar: str | None = None, role: str = "user"):
    """
    Create a new user.
    """
    user = models.User(
        email=body.email,
        username=body.username,
        hashed_password=get_password_hash(body.password),
        avatar=avatar,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_password(db: Session, user: models.User, new_password: str):
    """
    Update user's password.
    """
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    return user


def update_default_avatar(db: Session, user: models.User, avatar_url: str):
    """
    Update avatar for a user.
    """
    user.avatar = avatar_url
    db.commit()
    db.refresh(user)
    return user


def create_contact(db: Session, body: schemas.ContactCreate, owner_id: int):
    """
    Create a contact for a user.
    """
    contact = models.Contact(**body.model_dump(), owner_id=owner_id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def get_contacts(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    """
    Return paginated contacts for a user.
    """
    return (
        db.query(models.Contact)
        .filter(models.Contact.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_contact(db: Session, contact_id: int, owner_id: int):
    """
    Get a single contact by id for a specific owner.
    """
    return (
        db.query(models.Contact)
        .filter(models.Contact.id == contact_id, models.Contact.owner_id == owner_id)
        .first()
    )


def update_contact(db: Session, contact_id: int, body: schemas.ContactUpdate, owner_id: int):
    """
    Update an existing contact.
    """
    contact = get_contact(db, contact_id, owner_id)
    if contact is None:
        return None

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)

    db.commit()
    db.refresh(contact)
    return contact


def remove_contact(db: Session, contact_id: int, owner_id: int):
    """
    Delete a contact.
    """
    contact = get_contact(db, contact_id, owner_id)
    if contact is None:
        return None

    db.delete(contact)
    db.commit()
    return contact


def search_contacts(db: Session, owner_id: int, query: str):
    """
    Search contacts by first name, last name, or email.
    """
    pattern = f"%{query}%"
    return (
        db.query(models.Contact)
        .filter(
            models.Contact.owner_id == owner_id,
            (models.Contact.first_name.ilike(pattern))
            | (models.Contact.last_name.ilike(pattern))
            | (models.Contact.email.ilike(pattern)),
        )
        .all()
    )


def get_upcoming_birthdays(db: Session, owner_id: int):
    """
    Get contacts with birthdays in the next 7 days.
    """
    today = date.today()
    upcoming = today + timedelta(days=7)

    contacts = db.query(models.Contact).filter(models.Contact.owner_id == owner_id).all()
    result = []

    for contact in contacts:
        if contact.birthday:
            birthday_this_year = contact.birthday.replace(year=today.year)
            if today <= birthday_this_year <= upcoming:
                result.append(contact)

    return result
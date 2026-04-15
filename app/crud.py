from datetime import date, timedelta

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import Contact, User
from app.schemas import ContactCreate, ContactUpdate, UserCreate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(
    db: Session,
    user: UserCreate,
    hashed_password: str,
    avatar_url: str | None = None,
):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        avatar_url=avatar_url,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def confirm_user_email(db: Session, email: str):
    user = get_user_by_email(db, email)
    if user:
        user.confirmed = True
        db.commit()
        db.refresh(user)
    return user


def update_user_avatar(db: Session, user: User, avatar_url: str):
    user.avatar_url = avatar_url
    db.commit()
    db.refresh(user)
    return user


def create_contact(db: Session, contact: ContactCreate, owner_id: int):
    db_contact = Contact(**contact.model_dump(), owner_id=owner_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session, owner_id: int):
    return db.query(Contact).filter(Contact.owner_id == owner_id).all()


def get_contact(db: Session, contact_id: int, owner_id: int):
    return (
        db.query(Contact)
        .filter(Contact.id == contact_id, Contact.owner_id == owner_id)
        .first()
    )


def update_contact(db: Session, contact_id: int, contact: ContactUpdate, owner_id: int):
    db_contact = get_contact(db, contact_id, owner_id)
    if db_contact:
        for key, value in contact.model_dump().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int, owner_id: int):
    db_contact = get_contact(db, contact_id, owner_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


def search_contacts(
    db: Session,
    owner_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
):
    query = db.query(Contact).filter(Contact.owner_id == owner_id)

    filters = []
    if first_name:
        filters.append(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        filters.append(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        filters.append(Contact.email.ilike(f"%{email}%"))

    if filters:
        query = query.filter(or_(*filters))

    return query.all()


def get_upcoming_birthdays(db: Session, owner_id: int):
    contacts = db.query(Contact).filter(Contact.owner_id == owner_id).all()
    today = date.today()
    next_week = today + timedelta(days=7)
    result = []

    for contact in contacts:
        birthday_this_year = contact.birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        if today <= birthday_this_year <= next_week:
            result.append(contact)

    return result
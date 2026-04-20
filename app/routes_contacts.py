import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud import (
    create_contact,
    delete_contact,
    get_contact,
    get_contacts,
    get_upcoming_birthdays,
    search_contacts,
    update_contact,
)
from app.database import get_db
from app.dependencies import get_current_confirmed_user
from app.schemas import ContactCreate, ContactResponse, ContactUpdate


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact_route(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_confirmed_user),
):
    logger.info("User %s is creating a contact", current_user.email)
    return create_contact(db, contact, current_user.id)


@router.get("/", response_model=list[ContactResponse], status_code=status.HTTP_200_OK)
def get_contacts_route(
    skip: int = 0,
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_confirmed_user),
):
    logger.info(
        "User %s requested contacts list with skip=%s limit=%s",
        current_user.email,
        skip,
        limit,
    )
    return get_contacts(db, current_user.id, skip, limit)


@router.get("/birthdays", response_model=list[ContactResponse], status_code=status.HTTP_200_OK)
def get_birthdays_route(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_confirmed_user),
):
    logger.info("User %s requested upcoming birthdays", current_user.email)
    return get_upcoming_birthdays(db, current_user.id)


@router.get("/search", response_model=list[ContactResponse], status_code=status.HTTP_200_OK)
def search_contacts_route(
    first_name: str | None = Query(default=None),
    last_name: str | None = Query(default=None),
    email: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_confirmed_user),
):
    logger.info("User %s is searching contacts", current_user.email)
    return search_contacts(db, current_user.id, first_name, last_name, email)


@router.get("/{contact_id}", response_model=ContactResponse, status_code=status.HTTP_200_OK)
def get_contact_route(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_confirmed_user),
):
    logger.info("User %s requested contact id=%s", current_user.email, contact_id)
    contact = get_contact(db, contact_id, current_user.id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse, status_code=status.HTTP_200_OK)
def update_contact_route(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_confirmed_user),
):
    logger.info("User %s is updating contact id=%s", current_user.email, contact_id)
    updated_contact = update_contact(db, contact_id, contact, current_user.id)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact


@router.delete("/{contact_id}", status_code=status.HTTP_200_OK)
def delete_contact_route(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_confirmed_user),
):
    logger.info("User %s is deleting contact id=%s", current_user.email, contact_id)
    deleted_contact = delete_contact(db, contact_id, current_user.id)
    if deleted_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted"}
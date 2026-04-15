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
from app.dependencies import get_current_user
from app.schemas import ContactCreate, ContactResponse, ContactUpdate


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact_route(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_contact(db, contact, current_user.id)


@router.get("/", response_model=list[ContactResponse])
def get_contacts_route(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_contacts(db, current_user.id)


@router.get("/birthdays", response_model=list[ContactResponse])
def get_birthdays_route(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_upcoming_birthdays(db, current_user.id)


@router.get("/search", response_model=list[ContactResponse])
def search_contacts_route(
    first_name: str | None = Query(default=None),
    last_name: str | None = Query(default=None),
    email: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return search_contacts(db, current_user.id, first_name, last_name, email)


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact_route(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    contact = get_contact(db, contact_id, current_user.id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact_route(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    updated_contact = update_contact(db, contact_id, contact, current_user.id)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact


@router.delete("/{contact_id}")
def delete_contact_route(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    deleted_contact = delete_contact(db, contact_id, current_user.id)
    if deleted_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted"}
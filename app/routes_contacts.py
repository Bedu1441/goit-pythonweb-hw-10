"""
Contact CRUD routes.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post(
    "/",
    response_model=schemas.ContactResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create contact",
    description="Create a new contact for the currently authenticated user.",
)
def create_contact(
    body: schemas.ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new contact for current user.
    """
    return crud.create_contact(db, body, current_user.id)


@router.get(
    "/",
    response_model=List[schemas.ContactResponse],
    summary="Get all contacts",
    description="Return all contacts of the currently authenticated user with pagination support.",
)
def get_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return all contacts for current user.
    """
    return crud.get_contacts(db, current_user.id, skip, limit)


@router.get(
    "/search",
    response_model=List[schemas.ContactResponse],
    summary="Search contacts",
    description="Search contacts by first name, last name, or email.",
)
def search_contacts(
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Search contacts by query string.
    """
    return crud.search_contacts(db, current_user.id, query)


@router.get(
    "/birthdays",
    response_model=List[schemas.ContactResponse],
    summary="Get upcoming birthdays",
    description="Return contacts whose birthdays are within the next 7 days.",
)
def upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return contacts with upcoming birthdays.
    """
    return crud.get_upcoming_birthdays(db, current_user.id)


@router.get(
    "/{contact_id}",
    response_model=schemas.ContactResponse,
    summary="Get contact by id",
    description="Return a single contact by its identifier.",
)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return a single contact by id.
    """
    contact = crud.get_contact(db, contact_id, current_user.id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
    return contact


@router.put(
    "/{contact_id}",
    response_model=schemas.ContactResponse,
    summary="Update contact",
    description="Update an existing contact owned by the currently authenticated user.",
)
def update_contact(
    contact_id: int,
    body: schemas.ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update an existing contact.
    """
    contact = crud.update_contact(db, contact_id, body, current_user.id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
    return contact


@router.delete(
    "/{contact_id}",
    response_model=schemas.ContactResponse,
    summary="Delete contact",
    description="Delete a contact owned by the currently authenticated user.",
)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a contact.
    """
    contact = crud.remove_contact(db, contact_id, current_user.id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
    return contact
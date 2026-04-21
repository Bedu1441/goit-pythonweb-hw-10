"""
User-related routes.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import get_db
from app.dependencies import get_current_user, get_current_admin_user
from app.models import User
from app.redis_cache import clear_user_cache

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me",
    response_model=schemas.UserResponse,
    summary="Get current user",
    description="Return information about the currently authenticated user.",
)
def me(current_user: User = Depends(get_current_user)):
    """
    Return the currently authenticated user.
    """
    return current_user


@router.patch(
    "/default-avatar",
    response_model=schemas.UserResponse,
    summary="Update default avatar",
    description="Allow only admin users to update their default avatar.",
)
def update_default_avatar(
    body: schemas.AvatarUpdateRequest,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user),
):
    """
    Update default avatar. Only admins are allowed.
    """
    updated_user = crud.update_default_avatar(db, admin_user, body.avatar_url)
    clear_user_cache(updated_user.email)
    return updated_user
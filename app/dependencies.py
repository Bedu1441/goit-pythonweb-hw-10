"""
Reusable FastAPI dependencies.
"""

import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth import decode_token
from app.database import get_db
from app.models import User
from app.redis_cache import get_user_from_cache, set_user_to_cache

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Return current authenticated user.
    First tries Redis cache, then falls back to database.
    """
    payload = decode_token(token)
    email = payload.get("sub")
    if email is None:
        logger.warning("Token validation failed: missing subject")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    cached_user = get_user_from_cache(email)
    if cached_user:
        logger.info("Cache hit for user: %s", email)
        return User(**cached_user)

    logger.info("Cache miss for user: %s", email)
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        logger.warning("Authenticated user not found in database: %s", email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    set_user_to_cache(
        email,
        {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "hashed_password": user.hashed_password,
            "avatar": user.avatar,
            "is_confirmed": user.is_confirmed,
            "role": user.role,
        },
    )
    return user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Return current user only if role is admin.
    """
    if current_user.role != "admin":
        logger.warning(
            "Forbidden admin action attempt by user: %s with role: %s",
            current_user.email,
            current_user.role,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    logger.info("Admin access granted for: %s", current_user.email)
    return current_user
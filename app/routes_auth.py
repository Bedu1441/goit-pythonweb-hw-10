"""
Authentication routes.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas, crud
from app.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    create_reset_token,
    decode_token,
    get_email_from_reset_token,
)
from app.conf.messages import (
    ACCOUNT_EXISTS,
    INVALID_CREDENTIALS,
    PASSWORD_RESET_SENT,
    PASSWORD_RESET_SUCCESS,
)
from app.database import get_db
from app.email_utils import send_password_reset_email
from app.redis_cache import clear_user_cache

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email, username, and password.",
)
def signup(body: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    existing_user = crud.get_user_by_email(db, body.email)
    if existing_user:
        logger.warning("Signup attempt with existing email: %s", body.email)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ACCOUNT_EXISTS,
        )

    user = crud.create_user(db, body)
    logger.info("New user registered: %s", body.email)
    return user


@router.post(
    "/login",
    response_model=schemas.TokenPair,
    summary="Login user",
    description="Authenticate user with email and password and return access and refresh tokens.",
)
def login(
    body: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return JWT access and refresh tokens.
    """
    user = authenticate_user(db, body.username, body.password)
    if user is None:
        logger.warning("Failed login attempt for: %s", body.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_CREDENTIALS,
        )

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    logger.info("Successful login: %s", user.email)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post(
    "/refresh",
    response_model=schemas.Token,
    summary="Refresh access token",
    description="Generate a new access token using a valid refresh token.",
)
def refresh_access_token(body: schemas.RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Generate a new access token from a refresh token.
    """
    payload = decode_token(body.refresh_token)
    if payload.get("scope") != "refresh_token":
        logger.warning("Invalid refresh token scope")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    email = payload.get("sub")
    user = crud.get_user_by_email(db, email)
    if user is None:
        logger.warning("Refresh token used for missing user: %s", email)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    new_access_token = create_access_token(data={"sub": user.email})
    logger.info("Access token refreshed for: %s", user.email)
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post(
    "/request_password_reset",
    summary="Request password reset",
    description="Generate a password reset token and send reset instructions to the user's email.",
)
def request_password_reset(body: schemas.RequestEmail, db: Session = Depends(get_db)):
    """
    Generate and send password reset token.
    """
    user = crud.get_user_by_email(db, body.email)
    if user:
        token = create_reset_token(user.email)
        send_password_reset_email(user.email, token)
        logger.info("Password reset requested for: %s", user.email)
    else:
        logger.warning("Password reset requested for non-existing email: %s", body.email)

    return {"message": PASSWORD_RESET_SENT}


@router.post(
    "/reset_password/{token}",
    summary="Reset password",
    description="Reset user password using a valid password reset token.",
)
def reset_password(token: str, body: schemas.ResetPasswordBody, db: Session = Depends(get_db)):
    """
    Reset password using a valid token.
    """
    email = get_email_from_reset_token(token)
    user = crud.get_user_by_email(db, email)
    if user is None:
        logger.warning("Password reset attempted for missing user: %s", email)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    crud.update_user_password(db, user, body.new_password)
    clear_user_cache(user.email)
    logger.info("Password reset completed for: %s", email)
    return {"message": PASSWORD_RESET_SUCCESS}
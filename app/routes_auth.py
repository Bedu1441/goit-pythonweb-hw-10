from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    create_email_token,
    decode_email_token,
    get_password_hash,
    verify_password,
)
from app.crud import confirm_user_email, create_user, get_user_by_email
from app.database import get_db
from app.email_utils import send_verification_email
from app.schemas import Token, UserCreate, UserLogin, UserResponse


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists",
        )

    hashed_password = get_password_hash(user.password)
    avatar_url = f"https://ui-avatars.com/api/?name={user.username.replace(' ', '+')}"
    new_user = create_user(db, user, hashed_password, avatar_url=avatar_url)

    token = create_email_token(new_user.email)
    background_tasks.add_task(
        send_verification_email,
        new_user.email,
        new_user.username,
        token,
    )

    return new_user


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_data.email)

    if user is None or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not confirmed",
        )

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/confirmed_email/{token}")
def confirmed_email(token: str, db: Session = Depends(get_db)):
    try:
        email = decode_email_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token",
        )

    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification error",
        )

    if user.confirmed:
        return {"message": "Your email is already confirmed"}

    confirm_user_email(db, email)
    return {"message": "Email confirmed"}


@router.post("/request_email")
def request_email(
    background_tasks: BackgroundTasks,
    email: str,
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.confirmed:
        return {"message": "Your email is already confirmed"}

    token = create_email_token(user.email)
    background_tasks.add_task(
        send_verification_email,
        user.email,
        user.username,
        token,
    )

    return {"message": "Check your email for confirmation"}
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session

from app.cloudinary_service import upload_avatar
from app.crud import update_user_avatar
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import UserResponse


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def read_users_me(
    request: Request,
    current_user=Depends(get_current_user),
):
    return current_user


@router.patch("/avatar", response_model=UserResponse)
def update_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    avatar_url = upload_avatar(file.file, f"user_{current_user.id}")
    user = update_user_avatar(db, current_user, avatar_url)
    return user
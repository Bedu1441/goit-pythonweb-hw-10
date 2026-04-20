import os

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from fastapi import HTTPException, status


load_dotenv()

CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
API_KEY = os.getenv("CLOUDINARY_API_KEY")
API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET,
    secure=True,
)


def upload_avatar(file, public_id: str):
    if not CLOUD_NAME or not API_KEY or not API_SECRET:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cloudinary is not configured",
        )

    try:
        result = cloudinary.uploader.upload(
            file,
            public_id=public_id,
            overwrite=True,
            folder="goit_hw10",
            resource_type="image",
        )
        return result.get("secure_url")
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Avatar upload failed: {error}",
        )
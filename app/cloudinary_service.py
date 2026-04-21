"""
Cloudinary avatar service helpers.
"""

import cloudinary
import cloudinary.uploader
from app.database import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


def upload_avatar(file_path: str, public_id: str) -> str:
    """
    Upload avatar to Cloudinary and return secure URL.
    """
    result = cloudinary.uploader.upload(file_path, public_id=public_id, overwrite=True)
    return result["secure_url"]
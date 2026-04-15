import os

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv


load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


def upload_avatar(file, public_id: str):
    result = cloudinary.uploader.upload(
        file,
        public_id=public_id,
        overwrite=True,
        folder="goit_hw10",
    )
    return result.get("secure_url")
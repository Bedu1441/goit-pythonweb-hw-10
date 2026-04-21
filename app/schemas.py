"""
Pydantic schemas for requests and responses.
"""

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """
    Base user schema.
    """

    email: EmailStr
    username: str = Field(min_length=3, max_length=50)


class UserCreate(UserBase):
    """
    Schema for user registration.
    """

    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    """
    Schema for user login.
    """

    email: EmailStr
    password: str


class UserResponse(UserBase):
    """
    Schema for user response.
    """

    id: int
    avatar: Optional[str] = None
    role: str
    is_confirmed: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """
    JWT access token response.
    """

    access_token: str
    token_type: str = "bearer"


class TokenPair(BaseModel):
    """
    JWT access and refresh token response.
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """
    Schema for refresh token request.
    """

    refresh_token: str


class ContactBase(BaseModel):
    """
    Base schema for contact.
    """

    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: Optional[date] = None
    additional_data: Optional[str] = None


class ContactCreate(ContactBase):
    """
    Schema for creating contact.
    """
    pass


class ContactUpdate(BaseModel):
    """
    Schema for updating contact.
    """

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    additional_data: Optional[str] = None


class ContactResponse(ContactBase):
    """
    Schema for contact response.
    """

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RequestEmail(BaseModel):
    """
    Schema for email-based actions.
    """

    email: EmailStr


class ResetPasswordBody(BaseModel):
    """
    Schema for password reset submission.
    """

    new_password: str = Field(min_length=6, max_length=128)


class AvatarUpdateRequest(BaseModel):
    """
    Schema for default avatar update by admin.
    """

    avatar_url: str
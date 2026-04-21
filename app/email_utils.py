"""
Email helper functions.
"""

from app.database import settings


def send_password_reset_email(email: str, token: str) -> None:
    """
    Send a password reset email.
    In homework project, printing reset URL is acceptable for local/demo mode.
    """
    reset_link = f"{settings.APP_BASE_URL}/auth/reset_password/{token}"
    print(f"Send password reset link to {email}: {reset_link}")
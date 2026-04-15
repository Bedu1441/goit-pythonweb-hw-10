import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


def send_verification_email(email: str, username: str, token: str):
    base_url = os.getenv("APP_BASE_URL", "http://localhost:8001")
    verify_link = f"{base_url}/auth/confirmed_email/{token}"

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM")

    if not smtp_host or not smtp_user or not smtp_password or not smtp_from:
        print(f"Verification link for {email}: {verify_link}")
        return

    message = EmailMessage()
    message["Subject"] = "Verify your email"
    message["From"] = smtp_from
    message["To"] = email
    message.set_content(
        f"Hello, {username}!\n\nPlease verify your email by clicking this link:\n{verify_link}"
    )

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(message)
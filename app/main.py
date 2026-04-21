"""
Application entry point.
"""

import logging
from fastapi import FastAPI

from app.database import Base, engine
from app.routes_auth import router as auth_router
from app.routes_contacts import router as contacts_router
from app.routes_users import router as users_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Contacts API Homework 12",
    description=(
        "REST API for user authentication, contact management, password reset, "
        "role-based access control, Redis-based caching, and refresh token support."
    ),
    version="1.1.0",
)


@app.get(
    "/",
    summary="Health check",
    description="Simple endpoint to verify that the API is running.",
    tags=["system"],
)
def root():
    """
    Health-check root endpoint.
    """
    logger.info("Health check endpoint called")
    return {"message": "Contacts API is running"}


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(contacts_router)
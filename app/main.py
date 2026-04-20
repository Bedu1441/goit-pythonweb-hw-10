import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.database import Base, engine
from app.routes_auth import router as auth_router
from app.routes_contacts import router as contacts_router
from app.routes_users import router as users_router


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contacts API", version="1.0")

limiter = Limiter(key_func=get_remote_address, default_limits=[])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

cors_origins = os.getenv("CORS_ORIGINS", "")
origins = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for route in users_router.routes:
    if route.path == "/users/me":
        original_endpoint = route.endpoint
        route.endpoint = limiter.limit("5/minute")(original_endpoint)

app.include_router(auth_router)
app.include_router(contacts_router)
app.include_router(users_router)


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Contacts API is running"}
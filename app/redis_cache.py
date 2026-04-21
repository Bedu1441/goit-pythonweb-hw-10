"""
Redis cache utilities.
"""

import json
import redis
from redis.exceptions import RedisError
from app.database import settings


redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


def get_user_from_cache(email: str):
    """
    Return cached user data by email if available.
    If Redis is unavailable, return None.
    """
    try:
        value = redis_client.get(f"user:{email}")
        return json.loads(value) if value else None
    except RedisError:
        return None


def set_user_to_cache(email: str, user_data: dict, ttl: int = 300):
    """
    Store user data in cache with TTL.
    If Redis is unavailable, silently skip caching.
    """
    try:
        redis_client.setex(f"user:{email}", ttl, json.dumps(user_data))
    except RedisError:
        pass


def clear_user_cache(email: str):
    """
    Remove cached user data by email.
    If Redis is unavailable, silently skip cache cleanup.
    """
    try:
        redis_client.delete(f"user:{email}")
    except RedisError:
        pass
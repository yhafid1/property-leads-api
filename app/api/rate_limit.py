"""Rate limiting setup (slowapi), backed by Redis when available.

Reuses the same REDIS_URL already configured for Celery elsewhere in this
project. Falls back to slowapi's in-memory storage if Redis can't be
reached, so the API still works in environments without Redis running.
"""

import logging

from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from app.config import settings

logger = logging.getLogger(__name__)


def _key_func(request: Request) -> str:
    """Rate-limit per API key when present, otherwise per client IP."""
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return f"api-key:{api_key}"
    return get_remote_address(request)


def _build_storage_uri() -> str:
    """Use the project's existing Redis instance for rate-limit storage."""
    try:
        import redis as redis_lib

        client = redis_lib.from_url(settings.REDIS_URL, socket_connect_timeout=1)
        client.ping()
        return settings.REDIS_URL
    except Exception as exc:  # noqa: BLE001 - any connection failure -> fallback
        logger.warning(
            "Redis unavailable at %s (%s); falling back to in-memory rate limit storage",
            settings.REDIS_URL,
            exc,
        )
        return "memory://"


limiter = Limiter(
    key_func=_key_func,
    storage_uri=_build_storage_uri(),
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"],
)

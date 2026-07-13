"""Shared FastAPI dependencies (auth, etc.)."""

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.config import settings

API_KEY_NAME = "X-API-Key"

_api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def require_api_key(api_key: str = Security(_api_key_header)) -> str:
    """Validate the X-API-Key header against configured valid keys.

    Raises a 401 if the header is missing or does not match one of the
    keys configured via the API_KEYS environment variable.
    """
    valid_keys = settings.api_keys_list

    if not valid_keys:
        # Fail closed: if no keys are configured, auth cannot be satisfied.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API_KEYS is not configured on the server",
        )

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Include a valid 'X-API-Key' header.",
        )

    if api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )

    return api_key

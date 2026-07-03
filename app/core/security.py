import base64
import hashlib
import hmac
import json
from datetime import UTC, datetime, timedelta
from typing import Any

try:
    from jose import JWTError, jwt
except ModuleNotFoundError:
    JWTError = ValueError
    jwt = None

try:
    from passlib.context import CryptContext
except ModuleNotFoundError:
    CryptContext = None

from app.core.config import get_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") if CryptContext else None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if pwd_context:
        return pwd_context.verify(plain_password, hashed_password)
    return hmac.compare_digest(get_password_hash(plain_password), hashed_password)


def get_password_hash(password: str) -> str:
    if pwd_context:
        return pwd_context.hash(password)
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    settings = get_settings()
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload: dict[str, Any] = {"sub": subject, "exp": expire}
    if jwt:
        return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)
    return _encode_unsigned_payload(payload)


def decode_access_token(token: str) -> str | None:
    settings = get_settings()
    if jwt:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        except JWTError:
            return None
    else:
        payload = _decode_unsigned_payload(token)
    subject = payload.get("sub")
    return subject if isinstance(subject, str) else None


def _encode_unsigned_payload(payload: dict[str, Any]) -> str:
    serializable_payload = {
        key: value.isoformat() if isinstance(value, datetime) else value
        for key, value in payload.items()
    }
    raw = json.dumps(serializable_payload, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("utf-8")


def _decode_unsigned_payload(token: str) -> dict[str, Any]:
    try:
        raw = base64.urlsafe_b64decode(token.encode("utf-8"))
        payload = json.loads(raw)
    except (ValueError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}

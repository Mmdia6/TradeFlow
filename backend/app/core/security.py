from datetime import datetime, timedelta, timezone
import hashlib, secrets, jwt
from pwdlib import PasswordHash
from app.core.config import settings
_password_hash = PasswordHash.recommended()
def hash_password(password: str) -> str: return _password_hash.hash(password)
def verify_password(password: str, password_hash: str) -> bool: return _password_hash.verify(password, password_hash)
def create_access_token(subject: str) -> str:
    now=datetime.now(timezone.utc)
    return jwt.encode({"sub":subject,"type":"access","iat":now,"exp":now+timedelta(minutes=settings.access_token_minutes)},settings.secret_key,algorithm="HS256")
def decode_access_token(token: str) -> dict: return jwt.decode(token, settings.secret_key, algorithms=["HS256"])
def create_refresh_token() -> str: return secrets.token_urlsafe(48)
def hash_refresh_token(token: str) -> str: return hashlib.sha256(token.encode()).hexdigest()

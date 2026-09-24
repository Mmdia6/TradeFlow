from collections.abc import Generator
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
security=HTTPBearer(auto_error=False)
def db_session()->Generator[Session,None,None]: yield from get_db()
def get_current_user(credentials:HTTPAuthorizationCredentials|None=Depends(security),db:Session=Depends(db_session))->User:
    if credentials is None: raise HTTPException(401,"Authentication required.")
    try:
        payload=decode_access_token(credentials.credentials)
        if payload.get("type")!="access": raise ValueError
        user_id=int(payload["sub"])
    except Exception: raise HTTPException(401,"Invalid or expired access token.")
    user=db.get(User,user_id)
    if user is None or not user.is_active: raise HTTPException(401,"User is inactive or missing.")
    return user

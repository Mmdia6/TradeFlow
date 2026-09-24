from datetime import datetime
from fastapi import APIRouter,Depends,HTTPException,Request,status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import db_session
from app.core.rate_limit import allow
from app.core.security import hash_refresh_token
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas import Credentials,MessageResponse,RefreshRequest,TokenResponse
from app.services.auth import issue_tokens,login as login_user,register as register_user
router=APIRouter()
@router.post("/register",response_model=TokenResponse,status_code=status.HTTP_201_CREATED)
def register(payload:Credentials,request:Request,db:Session=Depends(db_session)):
    if not allow(f"register:{request.client.host if request.client else 'unknown'}"): raise HTTPException(429,"Too many authentication attempts.")
    try: _,a,r=register_user(db,payload.email.lower(),payload.password); return TokenResponse(access_token=a,refresh_token=r)
    except ValueError as e: db.rollback(); raise HTTPException(409,str(e))
@router.post("/login",response_model=TokenResponse)
def login(payload:Credentials,request:Request,db:Session=Depends(db_session)):
    if not allow(f"login:{payload.email.lower()}"): raise HTTPException(429,"Too many authentication attempts.")
    try: _,a,r=login_user(db,payload.email.lower(),payload.password); return TokenResponse(access_token=a,refresh_token=r)
    except ValueError: db.rollback(); raise HTTPException(401,"Invalid credentials.")
@router.post("/refresh",response_model=TokenResponse)
def refresh(payload:RefreshRequest,db:Session=Depends(db_session)):
    t=db.scalar(select(RefreshToken).where(RefreshToken.token_hash==hash_refresh_token(payload.refresh_token)))
    if t is None or t.revoked_at is not None or t.expires_at<datetime.utcnow(): raise HTTPException(401,"Invalid or expired refresh token.")
    u=db.get(User,t.user_id)
    if u is None or not u.is_active: raise HTTPException(401,"User is inactive or missing.")
    a,r=issue_tokens(db,u); nt=db.scalar(select(RefreshToken).where(RefreshToken.token_hash==hash_refresh_token(r))); t.revoked_at=datetime.utcnow(); t.replaced_by_id=nt.id; db.commit()
    return TokenResponse(access_token=a,refresh_token=r)
@router.post("/logout",response_model=MessageResponse)
def logout(payload:RefreshRequest,db:Session=Depends(db_session)):
    t=db.scalar(select(RefreshToken).where(RefreshToken.token_hash==hash_refresh_token(payload.refresh_token)))
    if t and t.revoked_at is None: t.revoked_at=datetime.utcnow(); db.commit()
    return MessageResponse(message="Logged out.")

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import db_session
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User

router = APIRouter()

class Credentials(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

def validate_password(password: str) -> None:
    if len(password) < 8:
        raise HTTPException(status_code=422, detail="Password must contain at least 8 characters.")

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: Credentials, db: Session = Depends(db_session)) -> TokenResponse:
    validate_password(payload.password)
    email = payload.email.lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="Email is already registered.")
    user = User(email=email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(access_token=create_access_token(str(user.id)))

@router.post("/login", response_model=TokenResponse)
def login(payload: Credentials, db: Session = Depends(db_session)) -> TokenResponse:
    validate_password(payload.password)
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if user is None or not verify_password(payload.password, user.password_hash) or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    return TokenResponse(access_token=create_access_token(str(user.id)))

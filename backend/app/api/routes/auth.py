from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.core.security import create_access_token

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
def register(payload: Credentials) -> TokenResponse:
    validate_password(payload.password)
    return TokenResponse(access_token=create_access_token(payload.email.lower()))

@router.post("/login", response_model=TokenResponse)
def login(payload: Credentials) -> TokenResponse:
    validate_password(payload.password)
    return TokenResponse(access_token=create_access_token(payload.email.lower()))

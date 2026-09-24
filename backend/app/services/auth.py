from datetime import datetime,timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import create_access_token,create_refresh_token,hash_password,hash_refresh_token,verify_password
from app.models.account import Account
from app.models.asset import Asset
from app.models.refresh_token import RefreshToken
from app.models.user import User
def issue_tokens(db:Session,user:User)->tuple[str,str]:
    access=create_access_token(str(user.id)); raw=create_refresh_token()
    db.add(RefreshToken(user_id=user.id,token_hash=hash_refresh_token(raw),expires_at=datetime.utcnow()+timedelta(days=settings.refresh_token_days)))
    return access,raw
def register(db:Session,email:str,password:str)->tuple[User,str,str]:
    if db.scalar(select(User).where(User.email==email)): raise ValueError("Email is already registered.")
    user=User(email=email,password_hash=hash_password(password)); db.add(user); db.flush()
    usdt=db.scalar(select(Asset).where(Asset.symbol=="USDT"))
    if usdt is None: raise RuntimeError("USDT seed asset is missing.")
    db.add(Account(user_id=user.id,asset_id=usdt.id,available_balance=10000)); access,refresh=issue_tokens(db,user); db.commit(); db.refresh(user)
    return user,access,refresh
def login(db:Session,email:str,password:str)->tuple[User,str,str]:
    user=db.scalar(select(User).where(User.email==email))
    if user is None or not user.is_active or not verify_password(password,user.password_hash): raise ValueError("Invalid credentials.")
    access,refresh=issue_tokens(db,user); db.commit(); return user,access,refresh

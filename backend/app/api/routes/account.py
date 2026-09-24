from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import db_session,get_current_user
from app.models.account import Account
from app.models.asset import Asset
from app.models.user import User
from app.schemas import AccountResponse
router=APIRouter()
@router.get("",response_model=list[AccountResponse])
def account(user:User=Depends(get_current_user),db:Session=Depends(db_session)):
    rows=db.scalars(select(Account).where(Account.user_id==user.id).order_by(Account.id)).all(); assets={a.id:a for a in db.scalars(select(Asset)).all()}
    return [AccountResponse(asset=assets[x.asset_id].symbol,available_balance=x.available_balance,locked_balance=x.locked_balance) for x in rows]

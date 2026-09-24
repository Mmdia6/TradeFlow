from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.api.dependencies import db_session,get_current_user
from app.models.user import User
from app.schemas import PortfolioResponse
from app.services.portfolio import build_portfolio
router=APIRouter()
@router.get("",response_model=PortfolioResponse)
def portfolio(user:User=Depends(get_current_user),db:Session=Depends(db_session)): return build_portfolio(db,user.id)

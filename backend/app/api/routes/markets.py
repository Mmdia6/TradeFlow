from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import db_session
from app.models.market import Market
from app.schemas import MarketResponse
from app.services.market import market_view
router=APIRouter()
@router.get("",response_model=list[MarketResponse])
def list_markets(db:Session=Depends(db_session)): return [market_view(db,m) for m in db.scalars(select(Market).where(Market.is_active.is_(True)).order_by(Market.symbol)).all()]
@router.get("/{symbol}",response_model=MarketResponse)
def get_market(symbol:str,db:Session=Depends(db_session)):
    m=db.scalar(select(Market).where(Market.symbol==symbol.upper(),Market.is_active.is_(True)))
    if m is None: raise HTTPException(404,"Market not found.")
    return market_view(db,m)

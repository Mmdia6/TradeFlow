from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import db_session,get_current_user
from app.models.market import Market
from app.models.order import Order
from app.models.trade import Trade
from app.models.user import User
from app.schemas import TradeResponse
router=APIRouter()
@router.get("",response_model=list[TradeResponse])
def trades(user:User=Depends(get_current_user),db:Session=Depends(db_session)):
    rows=db.execute(select(Trade,Market,Order).join(Market,Trade.market_id==Market.id).join(Order,Trade.order_id==Order.id).where(Order.user_id==user.id).order_by(Trade.executed_at.desc()).limit(100)).all()
    return [TradeResponse(id=t.id,market=m.symbol,side=o.side,quantity=t.quantity,price=t.price,quote_amount=t.quote_amount,fee=t.fee) for t,m,o in rows]

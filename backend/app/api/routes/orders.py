from fastapi import APIRouter,Depends,Header,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import db_session,get_current_user
from app.models.market import Market
from app.models.order import Order
from app.models.user import User
from app.schemas import OrderCreate,OrderResponse
from app.services.orders import cancel_order,create_order
router=APIRouter()
def view(db:Session,o:Order)->dict:
    m=db.get(Market,o.market_id)
    return {"id":o.id,"market":m.symbol,"side":o.side,"type":o.type,"status":o.status,"quantity":o.quantity,"filled_quantity":o.filled_quantity,"limit_price":o.limit_price,"average_fill_price":o.average_fill_price,"reserved_amount":o.reserved_amount}
@router.get("",response_model=list[OrderResponse])
def list_orders(user:User=Depends(get_current_user),db:Session=Depends(db_session)): return [view(db,o) for o in db.scalars(select(Order).where(Order.user_id==user.id).order_by(Order.created_at.desc()).limit(100)).all()]
@router.get("/{order_id}",response_model=OrderResponse)
def get_order(order_id:int,user:User=Depends(get_current_user),db:Session=Depends(db_session)):
    o=db.scalar(select(Order).where(Order.id==order_id,Order.user_id==user.id))
    if o is None: raise HTTPException(404,"Order not found.")
    return view(db,o)
@router.post("",response_model=OrderResponse,status_code=201)
def place_order(payload:OrderCreate,idempotency_key:str|None=Header(default=None,alias="Idempotency-Key"),user:User=Depends(get_current_user),db:Session=Depends(db_session)):
    if not idempotency_key: raise HTTPException(400,"Idempotency-Key header is required.")
    try: return view(db,create_order(db,user.id,payload.model_dump(),idempotency_key))
    except ValueError as e: db.rollback(); raise HTTPException(400,str(e))
@router.delete("/{order_id}",response_model=OrderResponse)
def cancel(order_id:int,user:User=Depends(get_current_user),db:Session=Depends(db_session)):
    try: return view(db,cancel_order(db,user.id,order_id))
    except ValueError as e: db.rollback(); raise HTTPException(400,str(e))

from datetime import datetime
from decimal import Decimal,ROUND_DOWN
import hashlib,json
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.account import Account
from app.models.asset import Asset
from app.models.idempotency_key import IdempotencyKey
from app.models.order import Order,OrderSide,OrderStatus,OrderType
from app.models.trade import Trade
from app.models.transaction import Transaction,TransactionType
from app.services.market import get_market,get_price
def _quantize(v:Decimal,p:int)->Decimal: return v.quantize(Decimal("1").scaleb(-p),rounding=ROUND_DOWN)
def _account(db:Session,user_id:int,asset_id:int)->Account:
    a=db.scalar(select(Account).where(Account.user_id==user_id,Account.asset_id==asset_id).with_for_update())
    if a is None: a=Account(user_id=user_id,asset_id=asset_id); db.add(a); db.flush()
    return a
def _ledger(db:Session,a:Account,amount:Decimal,kind:TransactionType,user_id:int,order_id:int):
    before=a.available_balance
    db.add(Transaction(account_id=a.id,user_id=user_id,asset_id=a.asset_id,type=kind,amount=amount,balance_before=before,balance_after=before+amount,reference_type="order",reference_id=str(order_id)))
def _execute(db:Session,o:Order,m:Market,base:Asset,quote:Asset,price:Decimal,user_id:int):
    qty=o.quantity; qa=_quantize(qty*price,m.price_precision); fee=_quantize(qa*Decimal(str(settings.trading_fee_rate)),m.price_precision)
    ba,qa_account=_account(db,user_id,base.id),_account(db,user_id,quote.id)
    if o.side==OrderSide.BUY:
        reserved,actual=o.reserved_amount,qa+fee; qa_account.locked_balance=max(Decimal("0"),qa_account.locked_balance-reserved); leftover=max(Decimal("0"),reserved-actual)
        qa_account.available_balance+=leftover; ba.available_balance+=qty
        if leftover: _ledger(db,qa_account,leftover,TransactionType.ORDER_RELEASE,user_id,o.id)
        _ledger(db,ba,qty,TransactionType.TRADE_CREDIT,user_id,o.id)
    else:
        ba.locked_balance=max(Decimal("0"),ba.locked_balance-qty); qa_account.available_balance+=qa-fee; _ledger(db,qa_account,qa-fee,TransactionType.TRADE_CREDIT,user_id,o.id)
    db.add(Trade(order_id=o.id,market_id=m.id,quantity=qty,price=price,quote_amount=qa,fee=fee)); o.filled_quantity=qty; o.average_fill_price=price; o.status=OrderStatus.FILLED; o.reserved_amount=Decimal("0")
def create_order(db:Session,user_id:int,payload:dict,key:str)->Order:
    rh=hashlib.sha256(json.dumps(payload,sort_keys=True,default=str).encode()).hexdigest()
    existing=db.scalar(select(IdempotencyKey).where(IdempotencyKey.user_id==user_id,IdempotencyKey.key==key))
    if existing:
        if existing.request_hash!=rh: raise ValueError("Idempotency key was already used with a different request.")
        o=db.get(Order,existing.order_id)
        if o is None: raise ValueError("Stored idempotency reference is invalid.")
        return o
    m=get_market(db,payload["market"]); price=get_price(m.symbol); qty=_quantize(Decimal(str(payload["quantity"])),m.quantity_precision)
    if qty<m.min_quantity: raise ValueError("Quantity is below the market minimum.")
    ot,side=OrderType(payload["type"]),OrderSide(payload["side"]); lp=Decimal(str(payload["limit_price"])) if payload.get("limit_price") is not None else None
    if ot==OrderType.LIMIT and lp is None: raise ValueError("Limit orders require limit_price.")
    ep=lp or price
    if qty*ep<m.min_notional: raise ValueError("Order notional is below the market minimum.")
    base,quote=db.get(Asset,m.base_asset_id),db.get(Asset,m.quote_asset_id)
    o=Order(user_id=user_id,market_id=m.id,side=side,type=ot,status=OrderStatus.PENDING,quantity=qty,limit_price=lp); db.add(o); db.flush()
    reserve=qty if side==OrderSide.SELL else ep*qty*(Decimal("1")+Decimal(str(settings.trading_fee_rate)))
    a=_account(db,user_id,base.id if side==OrderSide.SELL else quote.id)
    if a.available_balance<reserve: o.status=OrderStatus.REJECTED; db.commit(); raise ValueError("Insufficient balance.")
    a.available_balance-=reserve; a.locked_balance+=reserve; o.reserved_amount=reserve; _ledger(db,a,-reserve,TransactionType.ORDER_RESERVATION,user_id,o.id)
    fill=ot==OrderType.MARKET or (side==OrderSide.BUY and lp>=price) or (side==OrderSide.SELL and lp<=price)
    if fill: _execute(db,o,m,base,quote,price if ot==OrderType.MARKET else lp,user_id)
    else: o.status=OrderStatus.OPEN
    db.add(IdempotencyKey(user_id=user_id,key=key,request_hash=rh,order_id=o.id)); db.commit(); db.refresh(o); return o
def cancel_order(db:Session,user_id:int,order_id:int)->Order:
    o=db.scalar(select(Order).where(Order.id==order_id,Order.user_id==user_id).with_for_update())
    if o is None: raise ValueError("Order not found.")
    if o.status not in {OrderStatus.OPEN,OrderStatus.PARTIALLY_FILLED}: raise ValueError("Only open orders can be cancelled.")
    m=db.get(Market,o.market_id); base=db.get(Asset,m.base_asset_id); quote=db.get(Asset,m.quote_asset_id); a=_account(db,user_id,base.id if o.side==OrderSide.SELL else quote.id)
    a.locked_balance-=o.reserved_amount; a.available_balance+=o.reserved_amount; _ledger(db,a,o.reserved_amount,TransactionType.ORDER_RELEASE,user_id,o.id)
    o.reserved_amount=Decimal("0"); o.status=OrderStatus.CANCELLED; o.cancelled_at=datetime.utcnow(); db.commit(); db.refresh(o); return o

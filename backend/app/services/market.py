from decimal import Decimal
import redis
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.asset import Asset
from app.models.market import Market
_PRICES={"BTC/USDT":Decimal("65000"),"ETH/USDT":Decimal("3500"),"SOL/USDT":Decimal("150")}
def get_market(db:Session,symbol:str)->Market:
    m=db.scalar(select(Market).where(Market.symbol==symbol.upper(),Market.is_active.is_(True)))
    if m is None: raise ValueError("Market not found.")
    return m
def get_price(symbol:str)->Decimal: return _PRICES.get(symbol.upper(),Decimal("1"))
def cached_price(symbol:str)->Decimal:
    try:
        c=redis.Redis.from_url(settings.redis_url,decode_responses=True); k=f"tradeflow:market:{symbol.upper()}:price"; v=c.get(k)
        if v: return Decimal(v)
        p=get_price(symbol); c.setex(k,15,str(p)); return p
    except Exception: return get_price(symbol)
def market_view(db:Session,market:Market)->dict:
    b,q=db.get(Asset,market.base_asset_id),db.get(Asset,market.quote_asset_id)
    return {"id":market.id,"symbol":market.symbol,"base_asset":b.symbol,"quote_asset":q.symbol,"price":cached_price(market.symbol),
            "price_precision":market.price_precision,"quantity_precision":market.quantity_precision,"min_quantity":market.min_quantity,"min_notional":market.min_notional}

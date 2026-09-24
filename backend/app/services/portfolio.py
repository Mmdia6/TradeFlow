from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.account import Account
from app.models.asset import Asset
from app.models.market import Market
from app.models.order import Order,OrderSide
from app.models.trade import Trade
from app.services.market import cached_price
def build_portfolio(db:Session,user_id:int)->dict:
    accounts=db.scalars(select(Account).where(Account.user_id==user_id)).all()
    assets={a.id:a for a in db.scalars(select(Asset)).all()}; markets=db.scalars(select(Market).where(Market.is_active.is_(True))).all()
    by_base={m.base_asset_id:m for m in markets}; total=Decimal("0"); realized=Decimal("0"); result=[]
    for account in accounts:
        asset=assets[account.asset_id]; qty=account.available_balance+account.locked_balance
        if qty==0: continue
        if asset.symbol=="USDT": value,avg,unrealized=qty,Decimal("1"),Decimal("0")
        else:
            market=by_base.get(asset.id)
            if market is None: continue
            price=cached_price(market.symbol); value=qty*price
            buys=db.scalars(select(Trade).join(Order).where(Order.user_id==user_id,Trade.market_id==market.id,Order.side==OrderSide.BUY)).all()
            sells=db.scalars(select(Trade).join(Order).where(Order.user_id==user_id,Trade.market_id==market.id,Order.side==OrderSide.SELL)).all()
            bq=sum((t.quantity for t in buys),Decimal("0")); bc=sum((t.quote_amount+t.fee for t in buys),Decimal("0")); avg=bc/bq if bq else None
            sr=sum((t.quote_amount-t.fee for t in sells),Decimal("0")); sq=sum((t.quantity for t in sells),Decimal("0")); realized+=sr-(avg or Decimal("0"))*sq
            unrealized=(price-avg)*qty if avg is not None else Decimal("0")
        total+=value; result.append({"asset":asset.symbol,"quantity":qty,"current_value":value,"average_entry":avg,"unrealized_pnl":unrealized})
    return {"total_value":total,"realized_pnl":realized,"unrealized_pnl":sum((x["unrealized_pnl"] for x in result),Decimal("0")),"assets":result}

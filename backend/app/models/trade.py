from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Trade(Base):
    __tablename__ = "trades"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    market_id: Mapped[int] = mapped_column(ForeignKey("markets.id"), index=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(36, 18))
    price: Mapped[Decimal] = mapped_column(Numeric(36, 18))
    quote_amount: Mapped[Decimal] = mapped_column(Numeric(36, 18))
    fee: Mapped[Decimal] = mapped_column(Numeric(36, 18), default=Decimal("0"))
    executed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

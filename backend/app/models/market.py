from datetime import datetime
from decimal import Decimal
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class Market(Base):
    __tablename__ = "markets"
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    base_asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    quote_asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    price_precision: Mapped[int] = mapped_column(Integer, default=8)
    quantity_precision: Mapped[int] = mapped_column(Integer, default=8)
    min_quantity: Mapped[Decimal] = mapped_column(Numeric(36, 18), default=Decimal("0"))
    min_notional: Mapped[Decimal] = mapped_column(Numeric(36, 18), default=Decimal("0"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

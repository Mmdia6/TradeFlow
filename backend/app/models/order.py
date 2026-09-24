from datetime import datetime
from decimal import Decimal
from enum import Enum
from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    OPEN = "OPEN"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    market_id: Mapped[int] = mapped_column(ForeignKey("markets.id"), index=True)
    side: Mapped[OrderSide] = mapped_column(SAEnum(OrderSide))
    type: Mapped[OrderType] = mapped_column(SAEnum(OrderType))
    status: Mapped[OrderStatus] = mapped_column(SAEnum(OrderStatus), default=OrderStatus.PENDING)
    quantity: Mapped[Decimal] = mapped_column(Numeric(36, 18))
    filled_quantity: Mapped[Decimal] = mapped_column(Numeric(36, 18), default=Decimal("0"))
    limit_price: Mapped[Decimal | None] = mapped_column(Numeric(36, 18), nullable=True)
    average_fill_price: Mapped[Decimal | None] = mapped_column(Numeric(36, 18), nullable=True)
    reserved_amount: Mapped[Decimal] = mapped_column(Numeric(36, 18), default=Decimal("0"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

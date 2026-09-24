from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class PortfolioSnapshot(Base):
    __tablename__ = "portfolio_snapshots"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    total_value: Mapped[Decimal] = mapped_column(Numeric(36, 18))
    realized_pnl: Mapped[Decimal] = mapped_column(Numeric(36, 18))
    unrealized_pnl: Mapped[Decimal] = mapped_column(Numeric(36, 18))
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

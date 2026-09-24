from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
class IdempotencyKey(Base):
    __tablename__="idempotency_keys"
    __table_args__=(UniqueConstraint("user_id","key",name="uq_idempotency_user_key"),)
    id:Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True)
    key:Mapped[str]=mapped_column(String(128))
    request_hash:Mapped[str]=mapped_column(String(64))
    order_id:Mapped[int|None]=mapped_column(ForeignKey("orders.id"),nullable=True)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)

from datetime import date
from sqlalchemy import Date, func
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.database import Base


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[date] = mapped_column(Date, default=func.now())
    status: Mapped[str] = mapped_column(nullable=False)

    order_items: Mapped[list["OrderItems"]] = relationship("OrderItems", back_populates="order")


from app.order_items.models import OrderItems  # noqa E402

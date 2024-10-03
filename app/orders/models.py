from datetime import date
from sqlalchemy import Date
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.database import Base


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)

    order_items: Mapped[list["Orders"]] = relationship(back_populates="orders")

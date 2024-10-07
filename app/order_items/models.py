from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.database import Base


class OrderItems(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)

    order: Mapped["Orders"] = relationship("Orders", back_populates="order_items")
    product: Mapped["Products"] = relationship("Products", back_populates="order_items")


from app.orders.models import Orders  # noqa E402
from app.products.models import Products  # noqa E402

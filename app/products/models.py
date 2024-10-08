from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    price: Mapped[float] = mapped_column(nullable=False)
    available_stock: Mapped[int] = mapped_column(nullable=False)

    order_items: Mapped[list["OrderItems"]] = relationship(
        "OrderItems",
        back_populates="product",
        cascade="all, delete, delete-orphan",
    )


from app.order_items.models import OrderItems  # noqa E402

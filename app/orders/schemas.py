from enum import Enum

from pydantic import BaseModel

from app.order_items.schemas import OrderItemsSchema


class OrderStatus(str, Enum):
    in_progress = "В обработке"
    shipped = "Отправлен"
    delivered = "Доставлен"
    canceled = "Отменен"


class OrderSchema(BaseModel):
    status: OrderStatus
    order_items: list[OrderItemsSchema]

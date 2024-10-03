from datetime import date
from pydantic import BaseModel
from enum import Enum
from app.order_items.schemas import OrderItemsSchema


class OrderStatus(str, Enum):
    in_progress = "В обработке"
    shipped = "Отправлен"
    delivered = "Доставлен"
    canceled = "Отменен"


class OrderSchema(BaseModel):
    created_at: date
    status: OrderStatus
    order_items: list[OrderItemsSchema]

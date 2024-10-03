from pydantic import BaseModel, Field


class OrderItemsSchema(BaseModel):
    product_id: int = Field(title="Идентификатор продукта")
    quantity: int = Field(title="Количество товара в заказе", gt=0)

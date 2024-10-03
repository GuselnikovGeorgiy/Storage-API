from pydantic import BaseModel, Field
from fastapi import Query


class ProductSchema(BaseModel):
    name: str = Field(title="Наименование товара")
    description: str = Field(title="Описание товара")
    price: float = Field(title="Цена", gt=0)
    available_stock: int = Field(title="Количество товара на складе", gt=0)

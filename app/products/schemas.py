from pydantic import BaseModel, Field
from fastapi import Query


class ProductSchema(BaseModel):
    name: str = Field(title="Product name")
    description: str = Field(title="Product description")
    price: float = Field(title="Product price", gt=0)
    available_stock: int = Field(title="Product available in stock", gt=0)

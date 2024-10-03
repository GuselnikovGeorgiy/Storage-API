from fastapi import APIRouter

from app.products.dao import ProductsDAO
from app.products.schemas import ProductSchema


router = APIRouter(
    tags=["Products"],
)


@router.post("/products")
async def create_product(product_data: ProductSchema):
    return await ProductsDAO.add(**product_data.dict())


@router.get("/products")
async def get_products():
    return await ProductsDAO.select_all()


@router.get("/products/{product_id}")
async def get_product(product_id: int):
    return await ProductsDAO.find_one_or_none(id=product_id)


@router.put("/products/{product_id}")
async def update_product(product_id: int, product_data: ProductSchema):
    return await ProductsDAO.update(id=product_id, **product_data.dict())


@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    return await ProductsDAO.delete(id=product_id)
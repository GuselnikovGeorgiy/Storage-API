from fastapi import APIRouter
from app.database import get_db_session
from app.products.dao import ProductsDAO
from app.products.schemas import ProductSchema

router = APIRouter(
    tags=["Products"],
)


@router.post("/products")
async def create_product(product_data: ProductSchema):
    async with get_db_session() as session:
        return await ProductsDAO.add(
            session=session,
            **product_data.dict(),
        )


@router.get("/products")
async def get_products():
    async with get_db_session() as session:
        return await ProductsDAO.select_all(session=session)


@router.get("/products/{product_id}")
async def get_product(product_id: int):
    async with get_db_session() as session:
        return await ProductsDAO.find_one_or_none(
            session=session,
            id=product_id
        )


@router.put("/products/{product_id}")
async def update_product(product_id: int, product_data: ProductSchema):
    async with get_db_session() as session:
        return await ProductsDAO.update(
            session=session,
            id=product_id,
            **product_data.dict(),
        )


@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    async with get_db_session() as session:
        return await ProductsDAO.delete(session=session, id=product_id)

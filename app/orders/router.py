from fastapi import APIRouter

from app.database import get_db_session
from app.orders.dao import OrdersDAO
from app.orders.schemas import OrderSchema, OrderStatus
from app.orders.services import add_order

router = APIRouter(
    tags=["Orders"],
)


@router.get("/orders")
async def get_orders():
    async with get_db_session() as session:
        return await OrdersDAO.select_all(session=session)


@router.get("/orders/items")
async def get_orders_joined():
    async with get_db_session() as session:
        return await OrdersDAO.select_joined(session=session)


@router.get("/orders/{order_id}")
async def get_order(order_id: int):
    async with get_db_session() as session:
        return await OrdersDAO.find_one_or_none(session=session, id=order_id)


@router.get("/orders/{order_id}/items")
async def get_order_with_items(order_id: int):
    async with get_db_session() as session:
        return await OrdersDAO.select_joined(
            session=session,
            id=order_id,
        )


@router.post("/orders")
async def create_order(order_data: OrderSchema):
    async with get_db_session() as session:
        return await add_order(session=session, order_data=order_data)


@router.patch("/orders/{order_id}/status")
async def update_order(order_id: int, status: OrderStatus):
    async with get_db_session() as session:
        return await OrdersDAO.update(session=session, id=order_id, status=status)

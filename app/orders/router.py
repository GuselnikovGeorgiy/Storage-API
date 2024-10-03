from fastapi import APIRouter
from app.orders.dao import OrdersDAO
from app.orders.schemas import OrderStatus, OrderSchema


router = APIRouter(
    tags=["Orders"],
)


@router.post("/orders")
async def create_order(order_data: OrderSchema):
    pass


@router.get("/orders")
async def get_orders():
    return await OrdersDAO.select_all()


@router.get("/orders/items")
async def get_orders_joined():
    return await OrdersDAO.select_joined()


@router.get("/orders/{order_id}")
async def get_order(order_id: int):
    return await OrdersDAO.find_one_or_none(id=order_id)


@router.get("/orders/{order_id}/items")
async def get_order_with_items(order_id: int):
    return await OrdersDAO.select_joined(id=order_id)


@router.patch("/orders/{order_id}/{status}")
async def update_order(order_id: int, status: OrderStatus):
    return await OrdersDAO.update(id=order_id, status=status)


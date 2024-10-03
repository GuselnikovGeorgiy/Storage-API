from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.orders.models import Orders
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi.encoders import jsonable_encoder


class OrdersDAO(BaseDAO):
    model = Orders

    @classmethod
    async def select_joined(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(Orders).filter_by(**filter_by).options(selectinload(Orders.order_items))
            res = await session.execute(query)
            res = res.scalars().all()
            res = jsonable_encoder(res)
            return res

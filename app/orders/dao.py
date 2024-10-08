from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.exceptions import APIException, SQLAlchemyException
from app.orders.models import Orders


class OrdersDAO(BaseDAO):
    model = Orders

    @classmethod
    async def select_joined(cls, session: AsyncSession, **order_details):
        res = None
        try:
            query = (
                select(Orders)
                .filter_by(**order_details)
                .options(selectinload(Orders.order_items))
            )
            res = await session.execute(query)
            res = res.scalars().all()
            res = jsonable_encoder(res)
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                raise SQLAlchemyException
            elif isinstance(e, Exception):
                raise APIException
        return res

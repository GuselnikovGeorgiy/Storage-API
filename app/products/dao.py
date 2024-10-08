from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.exceptions import APIException, IDNotFoundException, SQLAlchemyException
from app.order_items.models import OrderItems
from app.products.models import Products


class ProductsDAO(BaseDAO):
    model = Products

    @classmethod
    async def delete(cls, session: AsyncSession, id: int):
        item = await cls.find_one_or_none(session=session, id=id)
        if not item:
            raise IDNotFoundException

        try:
            query = delete(OrderItems).where(OrderItems.product_id == id)
            await session.execute(query)

            query = delete(cls.model).where(cls.model.__table__.columns.id == id)
            await session.execute(query)
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                raise SQLAlchemyException
            elif isinstance(e, Exception):
                raise APIException

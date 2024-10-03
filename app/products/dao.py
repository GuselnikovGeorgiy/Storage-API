from app.dao.base import BaseDAO
from app.products.models import Products
from app.database import async_session_maker
from sqlalchemy import select,update, delete
from app.exceptions import IDNotFoundException


class ProductsDAO(BaseDAO):
    model = Products

    @classmethod
    async def update(cls, id: int, **data):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=id)
            result = await session.execute(query)
            if result.mappings().one_or_none() is None:
                raise IDNotFoundException

            query = update(cls.model).where(cls.model.__table__.columns.id == id).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=id)
            result = await session.execute(query)
            if result.mappings().one_or_none() is None:
                raise IDNotFoundException

            query = delete(cls.model).where(cls.model.__table__.columns.id == id)
            await session.execute(query)
            await session.commit()

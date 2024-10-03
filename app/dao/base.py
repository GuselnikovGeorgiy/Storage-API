from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker
from app.exceptions import SQLAlchemyException, APIException, IDNotFoundException


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def select_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        try:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                raise SQLAlchemyException
            elif isinstance(e, Exception):
                raise APIException

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

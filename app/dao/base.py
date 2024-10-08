from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import APIException, IDNotFoundException, SQLAlchemyException


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().one_or_none()

    @classmethod
    async def select_all(cls, session: AsyncSession):
        query = select(cls.model.__table__.columns)
        result = await session.execute(query)
        return result.mappings().all()

    @classmethod
    async def add(cls, session: AsyncSession, **data):
        try:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(query)
            await session.flush()
            return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                raise SQLAlchemyException
            elif isinstance(e, Exception):
                raise APIException

    @classmethod
    async def update(cls, session: AsyncSession, id: int, **data):
        item = await cls.find_one_or_none(session=session, id=id)
        if not item:
            raise IDNotFoundException

        try:
            query = (
                update(cls.model)
                .where(cls.model.__table__.columns.id == id)
                .values(**data)
            )
            await session.execute(query)
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                raise SQLAlchemyException
            elif isinstance(e, Exception):
                raise APIException

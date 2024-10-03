from app.dao.base import BaseDAO
from app.products.models import Products
from app.database import async_session_maker
from sqlalchemy import select,update, delete
from app.exceptions import IDNotFoundException


class ProductsDAO(BaseDAO):
    model = Products


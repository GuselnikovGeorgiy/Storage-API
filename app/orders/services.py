from app.exceptions import (
    IDNotFoundException,
    OutOfStockException,
    NotEnoughStockException,
    SQLAlchemyException,
)
from sqlalchemy.exc import SQLAlchemyError
from app.orders.schemas import OrderSchema
from app.orders.dao import OrdersDAO
from app.products.dao import ProductsDAO
from app.order_items.dao import OrderItemsDAO
from app.database import get_db_session


async def add_order(order_data: OrderSchema):
    lst_products = []
    try:
        async with get_db_session() as session:
            for order_item in order_data.order_items:
                product = await ProductsDAO.find_one_or_none(
                    session=session,
                    id=order_item.product_id,
                )
                if not product:
                    raise IDNotFoundException
                if product.available_stock == 0:
                    raise OutOfStockException
                if product.available_stock < order_item.quantity:
                    raise NotEnoughStockException

                lst_products.append(product)

            for product, order_item in zip(lst_products, order_data.order_items):
                await ProductsDAO.update(
                    session=session,
                    id=product.id,
                    available_stock=product.available_stock - order_item.quantity
                )

            order_id_json = await OrdersDAO.add(
                session=session,
                status=order_data.status
            )

            order_id = order_id_json['id']

            for order_item in order_data.order_items:
                await OrderItemsDAO.add(
                    session=session,
                    order_id=order_id,
                    product_id=order_item.product_id,
                    quantity=order_item.quantity
                )
    except (SQLAlchemyError, Exception) as e:
        if isinstance(e, SQLAlchemyError):
            raise SQLAlchemyException
        raise
    else:
        return order_id_json

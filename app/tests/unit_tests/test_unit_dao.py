import pytest

from app.database import get_db_session
from app.exceptions import SQLAlchemyException, IDNotFoundException
from app.orders.dao import OrdersDAO
from app.products.dao import ProductsDAO


# Тестирование find_one_or_none
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "order_id, is_exist",
    [
        (1, True), (2, True), (100, False),
    ]
)
async def test_get_order_by_id(order_id: int, is_exist: bool):
    async with get_db_session() as session:
        order = await OrdersDAO.find_one_or_none(session=session, id=order_id)

        if is_exist:
            assert order
            assert order.id == order_id
        else:
            assert not order


# Тестирование select_all
@pytest.mark.asyncio
async def test_get_orders():
    async with get_db_session() as session:
        orders = await OrdersDAO.select_all(session=session)
        assert isinstance(orders, list)
        assert len(orders) > 0


# Тестирование add
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_data, expected_id, expected_exception",
    [
        ({"name": "test", "description": "test", "price": 100, "available_stock": 10}, 7, None),
        ({"name": "test2", "description": "test2", "price": 110, "available_stock": 10}, 8, None),
        ({"name": "test3", "description": "test2", "price": 110}, None, SQLAlchemyException),
        ({"name2": "test2", "description": "test2", "price": 110, "available_stock": 10}, None, SQLAlchemyException),
        ({"name": "test2", "description": "test2", "price": "110", "available_stock": 10}, None, SQLAlchemyException),
    ]
)
async def test_add_product(
        product_data: dict,
        expected_id: int,
        expected_exception: Exception | None
):
    async with get_db_session() as session:
        if expected_exception:
            with pytest.raises(expected_exception):
                await ProductsDAO.add(session=session, **product_data)
        else:
            product_id = await ProductsDAO.add(session=session, **product_data)
            assert product_id["id"] == expected_id


# Тестирование update
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_id, product_data, expected_exception",
    [
        (1, {"name": "test", "description": "test", "price": 100, "available_stock": 10}, None),
        (1, {"name": "test", "description": "test", "price": 100, "available_stock": 10}, None),
        (2, {"name": "test2", "description": "test2"}, None),
        (999, {"name": "test2", "description": "test2"}, IDNotFoundException),
        (1, {"name3": "test", "description": "test", "price": 100, "available_stock": 10}, SQLAlchemyException),
        (1, {"name": "test", "description": "test", "price": "100", "available_stock": 10}, SQLAlchemyException),
    ]
)
async def test_update_product(product_id: int, product_data: dict, expected_exception: Exception | None):
    async with get_db_session() as session:
        if expected_exception:
            with pytest.raises(expected_exception):
                await ProductsDAO.update(session=session, id=product_id, **product_data)
        else:
            await ProductsDAO.update(session=session, id=product_id, **product_data)

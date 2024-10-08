import pytest

from app.database import get_db_session
from app.exceptions import (
    IDNotFoundException,
    NotEnoughStockException,
    OutOfStockException,
    SQLAlchemyException,
    UnprocessableEntityException,
)
from app.orders.dao import OrdersDAO
from app.orders.schemas import OrderSchema
from app.orders.services import add_order


# Тестирование select_joined
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter_by, expected_result_count, expected_exception",
    [
        ({"id": 1}, 1, None),
        ({"status": "Отправлен"}, 1, None),
        ({"id": 999}, 0, None),
        ({"status": "Несуществующий статус"}, 0, None),
        ({"non_existent_field": "invalid_value"}, 0, SQLAlchemyException),
    ],
)
async def test_select_joined(
    filter_by: dict,
    expected_result_count: int,
    expected_exception: Exception | None,
):
    async with get_db_session() as session:
        if expected_exception:
            with pytest.raises(expected_exception):
                await OrdersDAO.select_joined(session=session, **filter_by)
        else:
            result = await OrdersDAO.select_joined(session=session, **filter_by)
            assert len(result) == expected_result_count


# Тестирование add_order
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "order_data, expected_id, expected_exception",
    [
        (
            {
                "status": "Отправлен",
                "order_items": [
                    {"product_id": 1, "quantity": 1},
                    {"product_id": 2, "quantity": 2},
                ],
            },
            4,
            None,
        ),
        (
            {
                "order_items": [
                    {"product_id": 5, "quantity": 1},
                    {"product_id": 2, "quantity": 2},
                ],
                "status": "Отправлен",
            },
            5,
            None,
        ),
        (
            {
                "order_items": [
                    {"product_id": 100, "quantity": 1},
                    {"product_id": 2, "quantity": 2},
                ],
                "status": "В обработке",
            },
            None,
            IDNotFoundException,
        ),
        (
            {"order_items": [], "status": "В обработке"},
            None,
            UnprocessableEntityException,
        ),
        (
            {
                "order_items": [
                    {"product_id": 3, "quantity": 100},
                    {"product_id": 2, "quantity": 2},
                ],
                "status": "В обработке",
            },
            None,
            NotEnoughStockException,
        ),
        (
            {
                "order_items": [
                    {"product_id": 2, "quantity": 3},
                    {"product_id": 6, "quantity": 2},
                ],
                "status": "В обработке",
            },
            None,
            OutOfStockException,
        ),
        (
            {
                "order_items": [
                    {"product_id": 1, "quantity": 9},
                    {"product_id": 1, "quantity": 2},
                ],
                "status": "В обработке",
            },
            None,
            UnprocessableEntityException,
        ),
    ],
)
async def test_add_product(
    order_data: dict, expected_id: int, expected_exception: Exception | None
):
    order_data_parsed = OrderSchema.model_validate(order_data)
    async with get_db_session() as session:
        if expected_exception:
            with pytest.raises(expected_exception):
                _ = await add_order(
                    session=session, order_data=order_data_parsed
                )
        else:
            order_id = await add_order(session=session, order_data=order_data_parsed)
            assert order_id["id"] == expected_id

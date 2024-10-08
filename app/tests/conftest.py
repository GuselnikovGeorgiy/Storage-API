import asyncio
import json
from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from app.config import settings
from app.database import Base, engine, get_db_session
from app.main import create_app
from app.order_items.models import OrderItems
from app.orders.models import Orders
from app.products.models import Products


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_test_json(model: str):
        with open(f"app/tests/test_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    products = open_test_json("products")
    orders = open_test_json("orders")
    order_items = open_test_json("order_items")

    for order in orders:
        order["created_at"] = datetime.strptime(order["created_at"], "%Y-%m-%d")

    async with get_db_session() as session:
        add_products = insert(Products).values(products)
        add_orders = insert(Orders).values(orders)
        add_order_items = insert(OrderItems).values(order_items)

        await session.execute(add_products)
        await session.execute(add_orders)
        await session.execute(add_order_items)


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


fastapi_app = create_app()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        yield ac

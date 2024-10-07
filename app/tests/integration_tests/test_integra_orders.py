from httpx import AsyncClient


async def test_get_orders(ac: AsyncClient):
    response = await ac.get("/orders")

    assert response.status_code == 200
    assert len(response.json()) == 3

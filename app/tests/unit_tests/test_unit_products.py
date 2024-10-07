import pytest
from app.exceptions import IDNotFoundException
from app.products.dao import ProductsDAO
from app.database import get_db_session


# Тестирование delete
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_id, expected_exception",
    [
        (1, None),
        (2, None),
        (999, IDNotFoundException),
    ]
)
async def test_delete_product(product_id: int, expected_exception: Exception | None):
    async with get_db_session() as session:
        if expected_exception:
            with pytest.raises(expected_exception):
                await ProductsDAO.delete(session=session, id=product_id)
        else:
            await ProductsDAO.delete(session=session, id=product_id)

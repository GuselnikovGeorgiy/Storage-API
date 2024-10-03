from fastapi import FastAPI
from app.orders.router import router as orders_router
from app.products.router import router as products_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Storage API",
        root_path="/api",

    )

    app.include_router(orders_router)
    app.include_router(products_router)

    return app


from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="Storage API",
        root_path="/api/",

    )
    return app


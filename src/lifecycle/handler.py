from fastapi import FastAPI

from src.lifecycle import middleware, routing, static


def bootstrap(app: FastAPI) -> None:
    routing.include_routers(app)
    middleware.add_middleware(app)
    static.mount_static(app)

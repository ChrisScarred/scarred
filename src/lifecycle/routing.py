from fastapi import FastAPI
from src.controllers import demos, essentials, exceptions

def include_routers(app: FastAPI) -> None:
    app.include_router(essentials.router)
    app.include_router(demos.router)
    app.include_router(exceptions.router)

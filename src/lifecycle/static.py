from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.services.dependencies import config, routes


def mount_static(app: FastAPI) -> None:
        """Mount static files.
        """
        static_route = routes.get("static")
        app.mount(
            f"/{static_route}",
            StaticFiles(directory=config.get("app.resources.static")),
            name=static_route
        )
"""Startup manager module.
"""

import logging
from typing import Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.staticfiles import StaticFiles

from src.services.config import Config
from src.services.context import Context


class StartupManager:
    def __init__(self, app: FastAPI, config: Callable) -> None:
        self.app = app
        self.config = config
    
    def startup(self) -> None:
        self._add_middleware()
        self._mount_static()

    def _add_middleware(self) -> None:
        """Adds the following middleware: CORSMiddleware, TrustedHostMiddleware, and HTTPSRedirectMiddleware.
        """
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.get("security.origins"),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logging.debug(f"CORSMiddleware allowed origins are `{self.config.get('security.origins')}`.")
        
        self.app.add_middleware(TrustedHostMiddleware, allowed_hosts=self.config.get("security.hosts"))
        logging.debug(f"TrustedHostMiddleware allowed hosts are `{self.config.get('security.hosts')}`.")

        self.app.add_middleware(HTTPSRedirectMiddleware)

    def _mount_static(self) -> None:
        """Mount static files.
        """
        self.app.mount(
            "/static",
            StaticFiles(directory=self.config.get("app.resources.static")),
            name="static"
        )

def startup_event(app: FastAPI, config: Config) -> None:
    sm = StartupManager(app, config)
    sm.startup()
    logging.info("Application start-up complete.")


def shutdown_event(context: Context) -> None:
    """Perform the shut-down events.
    """
    context.get("Cockroach").close()
    logging.info("Application shut-down complete.")

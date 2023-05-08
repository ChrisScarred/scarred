import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from src.services.dependencies import config

def add_middleware(app: FastAPI) -> None:
    """Adds the following middleware: CORSMiddleware, TrustedHostMiddleware, and HTTPSRedirectMiddleware.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.get("security.origins"),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logging.debug(f"CORSMiddleware allowed origins are `{config.get('security.origins')}`.")
    
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.get("security.hosts"))
    logging.debug(f"TrustedHostMiddleware allowed hosts are `{config.get('security.hosts')}`.")

    app.add_middleware(HTTPSRedirectMiddleware)
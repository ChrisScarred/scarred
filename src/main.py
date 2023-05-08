import os

import uvicorn
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.requests import Request

from src.services.exception_handlers import client_exception_handler, server_exception_handler
from src.lifecycle.handler import bootstrap
from src.services.dependencies import config

app = FastAPI(title=config.get("app.name"), debug=config.get("app.debug"), version=config.get("app.version"))
bootstrap(app)


@app.exception_handler(HTTPException)
def client_exception_catcher(request: Request, exception: Exception):
    return client_exception_handler(request, exception)


@app.exception_handler(Exception)
def server_exception_catcher(request: Request, exception: Exception):
    return server_exception_handler(request, exception)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=5000,
        log_level="debug",
        ssl_keyfile=os.path.join(config.get("base_dir"), "certs/local/key.pem"),
        ssl_certfile=os.path.join(config.get("base_dir"), "certs/local/cert.pem"),
        reload=True,
    )

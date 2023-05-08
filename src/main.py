import os

import uvicorn
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.requests import Request

from src.controllers import demos, essentials, exceptions
from src.services.dependencies import config, routes, context
from src.services.cycle import shutdown_event, startup_event

app = FastAPI(title=config.get("app.name"), debug=config.get("app.debug"), version=config.get("app.version"))
app.include_router(essentials.router)
app.include_router(demos.router)
app.include_router(exceptions.router)


@app.on_event("startup")
def start_up():
    startup_event(app, config)


@app.on_event("shutdown")
def shutdown():
    shutdown_event(context)


@app.exception_handler(HTTPException)
def client_exception_handler_main(request: Request, exception: Exception):
    return exceptions.client_exception_handler(request, exception)


@app.exception_handler(Exception)
def server_exception_handler_main(request: Request, exception: Exception):
    return exceptions.server_exception_handler(request, exception)


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

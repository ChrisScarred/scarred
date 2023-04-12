import os

import uvicorn
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.requests import Request

from src.controllers import essentials, exceptions, demos
from src.services.context import context

app = FastAPI(title=context.get("app.name"), debug=context.get("app.debug"), version=context.get("app.version"))
context.add("FastAPI", app)


@app.on_event("startup")
async def start_up():
    await essentials.start_up(context)


@app.on_event("shutdown")
async def shutdown_event():
    await essentials.shutdown_event()


@app.exception_handler(HTTPException)
def client_exception_handler(request: Request, exception: Exception):
    return exceptions.client_exception_handler(request, exception, context)


@app.exception_handler(Exception)
def server_exception_handler(request: Request, exception: Exception):
    return exceptions.server_exception_handler(request, exception, context)


@app.get("/")
def home(request: Request):
    return essentials.home(request, context)


@app.get("/demos/")
def home(request: Request):
    return demos.router(request, context)


@app.get(f"/{context.get('routes.error')}/")
def error_generic(request: Request):
    return essentials.error_generic(request, context)


@app.get(f"/{context.get('routes.not_found')}/")
def error_404(request: Request):
    return essentials.error_404(request, context)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=5000,
        log_level="debug",
        ssl_keyfile=os.path.join(context.get("base_dir"), "certs/local/key.pem"),
        ssl_certfile=os.path.join(context.get("base_dir"), "certs/local/cert.pem"),
        reload=True,
    )

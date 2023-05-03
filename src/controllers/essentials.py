"""Handle basic requests.
"""
import logging

from starlette.requests import Request

from src.services.context import ContextHandler
from src.services.startup import StartupManager


async def shutdown_event(context: ContextHandler) -> None:
    context.get("Cockroach").close()
    logging.info("Application shut-down complete.")

async def start_up(context: ContextHandler) -> ContextHandler:
    sm = StartupManager(context)
    sm.start_up()
    logging.info("Application start-up complete.")


def home(request: Request, context: ContextHandler):
    return context.get("templates").TemplateResponse(context.get("views.intro"), {"request": request})


def error_404(request: Request, context: ContextHandler):
    params = request.query_params
    path = context.get("param_names.path")
    domain = str(request.url).split(context.get("routes.not_found"))[0].strip("/")

    return context.get("templates").TemplateResponse(
        context.get("views.content"),
        context={
            "request": request,
            "header": "Page not found",
            "content": (
                f"Page {domain}/{params.get(path, '/')} not found."
            ),
        },
    )

def error_generic(request: Request, context: ContextHandler):
    params = request.query_params
    code = context.get("param_names.code")
    path = context.get("param_names.path")
    templates = context.get("templates")
    content_template = context.get("views.content")
    
    domain = str(request.url).split(context.get("routes.not_found"))[0].strip("/")

    if code in params.keys():
        return templates.TemplateResponse(
            content_template,
            context={
                "request": request,
                "header": "An error has occurred",
                "content": f"Scar(R)ed apologises, an error {params[code]} has occurred when attempting to access page {domain}/{params.get(path, '')}.",
            },
        )
            
    return templates.TemplateResponse(
        content_template,
        context={
            "request": request,
            "header": "An error has occurred",
            "content": f"Scar(R)ed apologises, an unknown error has occurred when attempting to access page {domain}/{params.get(path, '')}.",
        },
    )

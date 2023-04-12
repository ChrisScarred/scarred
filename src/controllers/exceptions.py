from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.services.context import ContextHandler

import logging


def client_exception_handler(request: Request, exception: Exception, context: ContextHandler):
    path = request.url.path.strip("/")
    
    if exception.status_code == 404:
        return RedirectResponse(f"/{context.get('routes.not_found')}?{context.get('param_names.path')}={path}")
    try:
        return RedirectResponse(f"/{context.get('routes.error')}?{context.get('param_names.code')}={exception.status_code}&{context.get('param_names.path')}={path}")
    except Exception as e:
        logging.exception(e)
        return RedirectResponse(f"/{context.get('routes.error')}?{context.get('param_names.path')}={path}")


def server_exception_handler(request: Request, exception: Exception, context: ContextHandler):
    try:
        path = request.url.path.strip("/")
        return RedirectResponse(f"/{context.get('routes.error')}?{context.get('param_names.code')}={exception.status_code}&{context.get('param_names.path')}={path}")
    except Exception as e:
        logging.exception(e)
        return RedirectResponse(f"/{context.get('routes.error')}?{context.get('param_names.path')}={path}")

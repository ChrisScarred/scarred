import logging
from urllib import parse

from starlette.responses import RedirectResponse
from starlette.requests import Request

from src.services.dependencies import routes

PATH_PARAM = routes.get("param_names.path")

def client_exception_handler(request: Request, exception: Exception):
    path = parse.quote(request.url.path.strip("/"), safe='')
    if exception.status_code == 404:        
        return RedirectResponse(url = f"{routes.get('not_found')}?{PATH_PARAM}={path}")
    try:
        return RedirectResponse(url = f"/{routes.get('error')}?{routes.get('param_names.code')}={exception.status_code}&{PATH_PARAM}={path}")
    except Exception as e:
        logging.exception(e)
        return RedirectResponse(url = f"/{routes.get('error')}?{PATH_PARAM}={path}")


def server_exception_handler(request: Request, exception: Exception):
    try:
        path = parse.quote(request.url.path.strip("/"), safe='')
        return RedirectResponse(f"/{routes.get('error')}?{routes.get('param_names.code')}={exception.status_code}&{PATH_PARAM}={path}")
    except Exception as e:
        logging.exception(e)
        return RedirectResponse(f"/{routes.get('error')}?{PATH_PARAM}={path}")

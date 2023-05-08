import logging

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from urllib import parse
from src.services.dependencies import routes, context

router = APIRouter(tags=["exceptions"])

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


@router.get(f"/{routes.get('not_found')}")
def error_404(request: Request):
    params = request.query_params
    path = routes.get("param_names.path")
    domain = str(request.url).split(routes.get("not_found"))[0].strip("/")

    return context.get("templates").TemplateResponse(
        routes.get("views.content"),
        context={
            "request": request,
            "header": "Page not found",
            "content": (
                f"Page {domain}/{params.get(path, '/')} not found."
            ),
        },
    )


@router.get(f"/{routes.get('error')}")
def error_generic(request: Request):
    params = request.query_params
    code = routes.get("param_names.code")
    templates = context.get("templates")
    content_template = routes.get("views.content")
    
    domain = str(request.url).split(routes.get("not_found"))[0].strip("/")

    if code in params.keys():
        return templates.TemplateResponse(
            content_template,
            context={
                "request": request,
                "header": "An error has occurred",
                "content": f"Scar(R)ed apologises, an error {params[code]} has occurred when attempting to access page {domain}/{params.get(PATH_PARAM, '')}.",
            },
        )
            
    return templates.TemplateResponse(
        content_template,
        context={
            "request": request,
            "header": "An error has occurred",
            "content": f"Scar(R)ed apologises, an unknown error has occurred when attempting to access page {domain}/{params.get(PATH_PARAM, '')}.",
        },
    )

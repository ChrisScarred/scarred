from fastapi import APIRouter
from starlette.requests import Request

from src.services.dependencies import context, routes

router = APIRouter(tags=["exceptions"])
PATH_PARAM = routes.get("param_names.path")


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

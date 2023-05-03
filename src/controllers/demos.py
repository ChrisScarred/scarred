from starlette.requests import Request
from fastapi import Form

from src.services.context import ContextHandler
from src.assets.dragon_age import respond

async def router(request: Request, context: ContextHandler):
    params = request.query_params
    if len(params.keys()) == 0:
        return overview(request, context)
    name = params.get("name")
    if name:
        demo(name, request, context)

async def demo(name: str, request: Request, context: ContextHandler, species: str = Form(...), age: int = Form(...)):
    if name == "draci-vek":
        method = request.method
        if method == "GET":
            return context.get("templates").TemplateResponse(
                "dragon_age.html", context={"request": request, "title": "Dračí vek"}
            )
        elif method == "POST":
            result = respond(species, age)
            return context.get("templates").TemplateResponse(
                "dragon_age.html", context={"request": request, "title": "Dračí vek", "result": result}
            )

def overview(request: Request, context: ContextHandler):
    return context.get("Cockroach").test()

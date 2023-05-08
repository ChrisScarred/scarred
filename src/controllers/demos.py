from typing import Annotated

from fastapi import APIRouter, Form
from starlette.requests import Request

from src.assets.dragon_age import respond
from src.services.dependencies import context, routes

router = APIRouter()

@router.get(routes.get("demos.dragon_age"))
@router.post(routes.get("demos.dragon_age"))
async def dragon_age_demo(request: Request, species: Annotated[str, Form()], age: Annotated[int, Form()]):
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

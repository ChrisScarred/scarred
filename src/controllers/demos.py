from typing import Annotated

from fastapi import APIRouter, Form
from starlette.requests import Request

from src.assets.dragon_age import dragon_age_response
from src.services.dependencies import context, routes

router = APIRouter()

@router.get(f"/{routes.get('demos.dragon_age')}")
async def dragon_age_demo(request: Request):
    return context.get("templates").TemplateResponse(
        routes.get("views.dragon_age"), context={"request": request, "title": "Dračí vek"}
    )


@router.post(f"/{routes.get('demos.dragon_age')}")
async def dragon_age_demo(request: Request, species: Annotated[str, Form()], age: Annotated[int, Form()]):
    result = await dragon_age_response(species, age)
    return context.get("templates").TemplateResponse(
        routes.get("views.dragon_age"), context={"request": request, "title": "Dračí vek", "result": result}
    )

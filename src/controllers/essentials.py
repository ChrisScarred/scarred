"""Handle basic requests.
"""
from starlette.requests import Request
from src.services.dependencies import context, routes
from fastapi import APIRouter

router = APIRouter(tags=["essentials"])

@router.get("/")
def home(request: Request):
    return context.get("templates").TemplateResponse(routes.get("views.intro"), {"request": request})

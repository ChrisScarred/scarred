from starlette.requests import Request
from fastapi import Form, APIRouter

from src.assets.dragon_age import respond

router = APIRouter(prefix="/demos")



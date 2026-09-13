from fastapi import APIRouter

from src.api.route import utils


api_router = APIRouter()
api_router.include_router(utils.router)


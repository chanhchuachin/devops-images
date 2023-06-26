from fastapi import APIRouter
from src.api.background_removal.router import br_router
from src.api.engine.router import engine_router

api_router = APIRouter()
api_router.include_router(br_router)
api_router.include_router(engine_router)

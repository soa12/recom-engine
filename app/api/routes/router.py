from fastapi import APIRouter

from app.api.routes import event, recommendation

api_router = APIRouter()
api_router.include_router(event.router, tags=["event"], prefix="/event")
api_router.include_router(recommendation.router, tags=["recommendation"], prefix="/query")

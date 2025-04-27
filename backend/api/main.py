from fastapi import APIRouter

from backend.api.routes import (
    users,
    profiles,
    articles
)

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(profiles.router)
api_router.include_router(articles.router)
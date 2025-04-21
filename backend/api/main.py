from fastapi import APIRouter

from backend.api.routes import (
    users,
    profiles
)

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(profiles.router)

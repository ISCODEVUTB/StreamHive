from fastapi import APIRouter

from backend.api.routes import (
    login,
    users,
    profiles,
    articles,
    article_tags,
    movie_lists,
    ratings,
    follows,
    reactions,
    comments
)

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(profiles.router)
api_router.include_router(movie_lists.router)
api_router.include_router(ratings.router)
api_router.include_router(follows.router)
api_router.include_router(reactions.router)
api_router.include_router(comments.router)
api_router.include_router(articles.router)
api_router.include_router(article_tags.router)
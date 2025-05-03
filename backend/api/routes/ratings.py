import uuid
from typing import Any, Annotated

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from backend.logic.models import Rating, Profile
from backend.logic.schemas.ratings import (
    ProfileRating, 
    ProfileRatingsPublic, 
    MovieRating, 
    MovieRatingsPublic
)
from backend.logic.controllers import ratings
from backend.api.deps import SessionDep


router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.get(
    "/profile/{username}",
    response_model=ProfileRatingsPublic,
)
def read_ratings_by_username(
    *,
    session: SessionDep, 
    username: str
) -> ProfileRatingsPublic:
    """
    Retrieve all ratings made by a user (by username).
    """
    return ratings.get_ratings_by_username(session=session, username=username)


@router.get(
    "/movie/{movie_id}",
    response_model=MovieRatingsPublic,
)
def read_ratings_by_movie_id(
    *,
    session: SessionDep, 
    movie_id: str
) -> MovieRatingsPublic:
    """
    Retrieve all ratings for a specific movie (including usernames and ratings).
    """
    return ratings.get_ratings_by_movie_id(session=session, movie_id=movie_id)


@router.get("/movie/{movie_id}/average", response_model=float)
def get_average_rating_for_movie(
    *,
    session: SessionDep,
    movie_id: str
) -> float:
    """
    Retrieve the average rating for a specific movie.
    """
    avg = session.exec(
        select(func.avg(Rating.rate)).where(Rating.movie_id == movie_id)
    ).first()
    
    average = avg if avg is not None else 0.0
    return round(average, 2)

@router.post(
    "/", 
    response_model=Rating
)
def create_or_update_rating(
    *, 
    session: SessionDep,
    profile_id: uuid.UUID,
    movie_id: str,
    rate: float
) -> Rating:
    """
    Create or update a rating for a movie by a profile.
    """
    if not (0 <= rate <= 5):
        raise HTTPException(
            status_code=400,
            detail="Rating value must be between 0 and 5.",
        )
    
    rating = ratings.create_or_update_rating(
        session=session, 
        profile_id=profile_id,
        movie_id=movie_id,
        rate=rate
    )
    return rating


@router.delete("/profile/{profile_id}/movie/{movie_id}")
def delete_rating(
    *,
    session: SessionDep,
    profile_id: uuid.UUID,
    movie_id: str
) -> dict:
    """
    Delete a rating by profile_id and movie_id.
    """
    rating = session.exec(
        select(Rating).where(
            Rating.profile_id == profile_id,
            Rating.movie_id == movie_id
        )
    ).first()

    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found.")

    session.delete(rating)
    session.commit()
    return {"message": "Rating deleted successfully."}

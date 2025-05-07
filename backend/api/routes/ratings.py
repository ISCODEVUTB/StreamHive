import uuid
from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from backend.logic.models import Rating, Profile
from backend.logic.schemas.ratings import (
    CreateRating,
    ProfileRating, 
    ProfileRatingsPublic, 
    MovieRating, 
    MovieRatingsPublic
)
from backend.logic.controllers import ratings
from backend.api.deps import CurrentUser, SessionDep, get_current_user
from backend.api.schemas import Message


router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.post(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=Rating
)
def create_or_update_rating(
    *, 
    session: SessionDep,
    current_user: CurrentUser,
    movie_id: str,
    rate_in: CreateRating
) -> Rating:
    """
    Create or update a rating for a movie by a profile.
    """
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    profile_in: Profile = session.exec(statement).first()
    profile_id = profile_in.profile_id

    rating = CreateRating(
        rate=rate_in.rate,
    )

    rating = ratings.create_or_update_rating(
        session=session, 
        profile_id=profile_id,
        movie_id=movie_id,
        rating_in=rating
    )
    return rating


@router.get(
    "/profile",
    dependencies=[Depends(get_current_user)],
    response_model=ProfileRatingsPublic,
)
def read_my_ratings(
    *,
    session: SessionDep,
    current_user: CurrentUser   
) -> ProfileRatingsPublic:
    """
    Retrieve all ratings made by a user (by profile).
    """
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    profile_in: Profile = session.exec(statement).first()
    profile_id = profile_in.profile_id

    return ratings.get_ratings_by_profile(session=session, profile_id=profile_id)


@router.get(
    "/profile/{profile_id}",
    dependencies=[Depends(get_current_user)],
    response_model=ProfileRatingsPublic,
)
def read_ratings_by_profile(
    *,
    session: SessionDep,
    profile_id: uuid.UUID   
) -> ProfileRatingsPublic:
    """
    Retrieve all ratings made by a user (by profile).
    """
    profile_id: Profile = session.get(Profile, profile_id)
    profile_id = profile_id.profile_id

    return ratings.get_ratings_by_profile(session=session, profile_id=profile_id)


@router.get(
    "/movie/{movie_id}",
    dependencies=[Depends(get_current_user)],
    response_model=MovieRatingsPublic
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


@router.delete(
    "/movie/{movie_id}/profile/{profile_id}",
    response_model=Message
)
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
    return Message(message="Rating deleted successfully.")

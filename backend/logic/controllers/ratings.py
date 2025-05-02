import uuid
from typing import Any

from sqlmodel import Session, select

from backend.logic.models import Rating, Profile
from backend.logic.schemas.ratings import (
    ProfileRating, 
    ProfileRatingsPublic, 
    MovieRating, 
    MovieRatingsPublic
)


def create_or_update_rating(
    *, session: Session, profile_id: uuid.UUID, movie_id: str, rate: float
) -> Rating:
    """
    Create or update a rating by profile_id for a movie

    Args:
        session (Session): Active SQLModel database session.
        profile_id (uuid.UUID): The profile ID that is rating the movie.
        movie_id (str): The ID of the movie being rated.
        rate (float): The rating value, typically between 0 and 5.

    Returns:
        Rating: The created or updated rating object.
    """
    db_obj = session.exec(
        select(Rating).where(
            Rating.profile_id == profile_id, Rating.movie_id == movie_id
        )
    ).first()

    if db_obj:
        db_obj.rate = rate
    else:
        db_obj = Rating(profile_id=profile_id, movie_id=movie_id, rate=rate)
    
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_ratings_by_username(
    *, session: Session, username: str
) -> ProfileRatingsPublic:
    """
    Retrieve all movie ratings made by a profile, identified by its username.

    Args:
        session (Session): Active SQLModel database session.
        username (str): The username of the profile to fetch ratings for.

    Returns:
        ProfileRatingsPublic: A collection of ratings associated with the given profile username.
    """
    profile = session.exec(select(Profile).where(Profile.username == username)).first()

    if not profile:
        return ProfileRatingsPublic(username=username, ratings=[])
    
    session_ratings = session.exec(select(Rating).where(Rating.profile_id == profile.profile_id)).all()
    ratings_list = [ProfileRating(movie_id=r.movie_id, rate=r.rate) for r in session_ratings]

    return ProfileRatingsPublic(username=username, ratings=ratings_list)


def get_ratings_by_movie_id(
    *, session: Session,  movie_id: str
) -> MovieRatingsPublic:
    """
    Retrieve all profiles that have rated a specific movie.

    Args:
        session (Session): Active SQLModel database session.
        movie_id (str): The movie ID to search for.

    Returns:
        MovieRatingsPublic: A collection of profiles with ratings for the specified movie.
    """
    rating = session.exec(select(Rating).where(Rating.movie_id == movie_id))
    if not rating:
        return MovieRatingsPublic(movie_id=movie_id, ratings=[])
    
    result_list = []
    for r in rating:
        profile = session.exec(select(Profile).where(Profile.profile_id == r.profile_id)).first()
        if profile:
            result_list.append(MovieRating(username=profile.username, rate=r.rate))

    return MovieRatingsPublic(movie_id=movie_id, ratings=result_list)

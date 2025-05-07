import uuid
from typing import Any

from sqlmodel import Session, select

from backend.logic.models import Rating, Profile
from backend.logic.schemas.ratings import (
    CreateRating,
    ProfileRating, 
    ProfileRatingsPublic, 
    MovieRating, 
    MovieRatingsPublic
)


def create_or_update_rating(
    *, session: Session, profile_id: uuid.UUID, movie_id: str, rating_in: CreateRating,
) -> Rating:
    """
    Create or update a rating using a validated CreateRating schema.

    Args:
        session (Session): Active SQLModel database session.
        rating_in (CreateRating): Input schema containing profile_id, movie_id, and rate.

    Returns:
        Rating: The created or updated rating object.
    """
    db_obj = session.exec(
        select(Rating).where(
            Rating.profile_id == profile_id,
            Rating.movie_id == movie_id
        )
    ).first()

    if db_obj:
        db_obj.rate = rating_in.rate
    else:
        db_obj = Rating(
            profile_id=profile_id,
            movie_id=movie_id,
            rate=rating_in.rate
        )

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_ratings_by_profile(
    *, session: Session, profile_id: uuid.UUID
) -> ProfileRatingsPublic | None:
    """
    Retrieve all movie ratings made by a profile, identified by its username.

    Args:
        session (Session): Active SQLModel database session.
        profile_id (uuid.UUID): The ID of the profile to fetch ratings for.

    Returns:
        ProfileRatingsPublic: A collection of ratings associated with the given profile ID.
    """
    profile = session.get(Profile, profile_id)
    if not profile:
        return None
    
    username = profile.username
    session_ratings = session.exec(select(Rating).where(Rating.profile_id == profile.profile_id)).all()
    ratings_list = [ProfileRating(movie_id=r.movie_id, rate=r.rate) for r in session_ratings]

    return ProfileRatingsPublic(profile_id=profile_id, username=username, ratings=ratings_list)


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
    rating = (
        select(Rating, Profile.profile_id, Profile.username)
        .join(Profile, Profile.profile_id == Rating.profile_id)
        .where(Rating.movie_id == movie_id)
    )

    ratings = list(session.exec(rating))
    ratings_list = [
        MovieRating(profile_id=profile_id, username=username, rate=rating.rate)
        for rating, profile_id, username in ratings
    ]

    return MovieRatingsPublic(movie_id=movie_id, ratings=ratings_list)

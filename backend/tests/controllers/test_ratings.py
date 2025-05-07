import uuid
import pytest
from sqlmodel import Session
from sqlmodel import func, select

from backend.logic.models import Rating
from backend.logic.enum import ProfileRoles, UserTypes, UserGender
from backend.logic.controllers import users, profiles, ratings
from backend.logic.schemas.ratings import (
    CreateRating,
    ProfileRatingsPublic, 
    MovieRatingsPublic
)
from backend.logic.schemas.users import CreateUser
from backend.logic.schemas.profiles import CreateProfile
from backend.tests.utils.utils import random_email, random_lower_string, random_birth_date

full_name='User Example'
gender=UserGender.OTHER
user_type=UserTypes.EXTERNAL


def user_and_profile_in(db: Session):  
    user_in = CreateUser(
        full_name=full_name,
        email=random_email(), 
        password =random_lower_string(),
        birth_date=random_birth_date(),
        user_gender=gender,
        user_type=user_type
    )
    
    user = users.create_user(session=db, user_create=user_in)

    profile_in = CreateProfile(
        username=random_lower_string(),
        profile_role=ProfileRoles.SUBSCRIBER
    )
    profile = profiles.create_profile(session=db, profile_create=profile_in, user_id=user.user_id)

    return user, profile


def test_create_or_update_rating(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    movie_id = "movie-rom-123"
    rate = CreateRating(
        rate=4.5
    )
    
    rating = ratings.create_or_update_rating(
        session=db, profile_id=profile.profile_id, movie_id=movie_id, rating_in=rate
    )

    assert rating.profile_id == profile.profile_id
    assert rating.movie_id == movie_id
    assert rating.rate == rate.rate


def test_get_rating_by_profile(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    movie_id = "movie-com-456"
    rate = CreateRating(
        rate=3.5
    )
    
    rating = ratings.create_or_update_rating(
        session=db, profile_id=profile.profile_id, movie_id=movie_id, rating_in=rate
    )
    rating = ratings.get_ratings_by_profile(session=db, profile_id=profile.profile_id)

    assert isinstance(rating, ProfileRatingsPublic)
    assert rating.username == profile.username
    assert len(rating.ratings) == 1
    assert rating.ratings[0].movie_id == movie_id


def test_get_rating_by_nonexistent_profile(db: Session) -> None:
    non_existent = uuid.uuid4()

    rating = ratings.get_ratings_by_profile(session=db, profile_id=non_existent)

    assert rating is None


def test_get_rating_by_movie_id(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    movie_id = "movie-horr-789"
    rate = CreateRating(
        rate=3.0
    )
    
    rating = ratings.create_or_update_rating(
        session=db, profile_id=profile.profile_id, movie_id=movie_id, rating_in=rate
    )
    rating = ratings.get_ratings_by_movie_id(session=db, movie_id=movie_id)

    assert isinstance(rating, MovieRatingsPublic)
    assert rating.movie_id == movie_id
    assert len(rating.ratings) == 1
    assert rating.ratings[0].username == profile.username
    assert rating.ratings[0].rate == rate.rate


def test_get_rating_by_movie_id_no_ratings(db: Session) -> None:
    movie_id = "movie-0-ratings"

    rating = ratings.get_ratings_by_movie_id(session=db, movie_id=movie_id)

    assert isinstance(rating, MovieRatingsPublic)
    assert rating.movie_id == movie_id
    assert len(rating.ratings) == 0


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_update_ratings(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    movie_id = "movie-rom-456"
    rate = CreateRating(
        rate=3.5
    )
    rate2 = CreateRating(
        rate=4.5
    )
    
    ratings.create_or_update_rating(
        session=db, profile_id=profile.profile_id, movie_id=movie_id, rating_in=rate
    )

    updated_rating = ratings.create_or_update_rating(
        session=db, profile_id=profile.profile_id, movie_id=movie_id, rating_in=rate2
    )
    
    assert updated_rating
    assert updated_rating.rate == rate2.rate


def test_average_rating(db: Session):
    _, profile1 = user_and_profile_in(db)
    _, profile2 = user_and_profile_in(db)
    movie_id = "movie-hor-789"
    ratings.create_or_update_rating(
        session=db, profile_id=profile1.profile_id, movie_id=movie_id, rating_in=CreateRating(rate=2.0)
    )
    ratings.create_or_update_rating(
        session=db, profile_id=profile2.profile_id, movie_id=movie_id, rating_in=CreateRating(rate=4.0)
    )

    avg = db.exec(
        select(func.avg(Rating.rate)).where(Rating.movie_id == movie_id)
    ).first()

    assert round(avg, 2) == 3.0 
    

def test_delete_rating(db: Session):
    _, profile = user_and_profile_in(db)
    movie_id = "movie-rom-456"
    ratings.create_or_update_rating(
        session=db, profile_id=profile.profile_id, movie_id=movie_id, rating_in=CreateRating(rate=2.5)
    )

    rating = db.exec(
        select(Rating).where(
            Rating.profile_id == profile.profile_id,
            Rating.movie_id == movie_id
        )
    ).first()

    assert rating is not None

    db.delete(rating)
    db.commit()

    deleted = db.exec(
        select(Rating).where(
            Rating.profile_id == profile.profile_id,
            Rating.movie_id == movie_id
        )
    ).first()

    assert deleted is None

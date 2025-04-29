from fastapi.encoders import jsonable_encoder
import pytest
from sqlmodel import Session

from backend.logic.models import User, Profile, MovieList
from backend.logic.controllers import users, profiles, movie_lists
from backend.logic.schemas.users import CreateUser
from backend.logic.schemas.profiles import CreateProfile
from backend.logic.schemas.movie_lists import CreateMovieList, UpdateMovieList
from backend.tests.utils.utils import random_email, random_lower_string, random_birth_date


def user_in() -> User:
    return CreateUser(
        email=random_email(), 
        password =random_lower_string(),
        birth_date=random_birth_date(),
        full_name='User Example',
        gender="Other",
        user_type="external"
    )


def profile_in() -> Profile:
    profile_in = CreateProfile(
        username=random_lower_string(),
    )


def test_create_profile(db: Session) -> None:
    user = users.create_user(session=db, user_create=user_in())
    profile = profiles.create_profile(session=db, profile_create=profile_in(), user_id=user.user_id)
    list_in = CreateMovieList(
        name=random_lower_string()
    )
    movie_list = movie_lists.create_movie_list(session=db, movielist_create=list_in, profile_id=profile.profile_id)

    assert movie_list
    assert movie_list.profile_id == profile.profile_id
    assert movie_list.name == list_in.name


def test_get_profile(db: Session) -> None:
    user = users.create_user(session=db, user_create=user_in())
    profile = profiles.create_profile(session=db, profile_create=profile_in(), user_id=user.user_id)
    list_in = CreateMovieList(
        name=random_lower_string()
    )
    movie_list = movie_lists.create_movie_list(session=db, movielist_create=list_in, profile_id=profile.profile_id)
    movie_list_2 = db.get(MovieList, movie_list.list_id)
    
    assert movie_list_2
    assert movie_list.name == movie_list_2.name
    assert jsonable_encoder(movie_list) == jsonable_encoder(movie_list_2)


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_update_user(db: Session) -> None:
    user = users.create_user(session=db, user_create=user_in())
    profile = profiles.create_profile(session=db, profile_create=profile_in(), user_id=user.user_id)
    list_in = CreateMovieList(
        name=random_lower_string()
    )
    movie_list = movie_lists.create_movie_list(session=db, movielist_create=list_in, profile_id=profile.profile_id)
    
    new_name = random_lower_string()
    list_in_update = UpdateMovieList(
        name=new_name
    )
    
    if movie_list.list_id is not None:
        movie_lists.update_movie_list(session=db, db_movielist=movie_list, movielist_in=list_in_update)
    movie_list_2 = db.get(MovieList, movie_list.list_id)
    
    assert movie_list_2
    assert movie_list_2.name == new_name
    
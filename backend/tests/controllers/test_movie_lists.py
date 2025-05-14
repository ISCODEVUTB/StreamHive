from fastapi.encoders import jsonable_encoder
import pytest
from sqlmodel import Session

from backend.logic.models import MovieList
from backend.logic.controllers import movie_lists
from backend.logic.schemas.movie_lists import CreateMovieList, UpdateMovieList
from backend.tests.utils.utils import random_lower_string
from backend.tests.utils.user import user_and_profile_in


def test_create_movie_list(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    list_in = CreateMovieList(
        name=random_lower_string()
    )
    movie_list = movie_lists.create_movie_list(session=db, movielist_create=list_in, profile_id=profile.profile_id)

    assert movie_list
    assert movie_list.profile_id == profile.profile_id
    assert movie_list.name == list_in.name


def test_get_movie_list(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    list_in = CreateMovieList(
        name=random_lower_string()
    )
    movie_list = movie_lists.create_movie_list(session=db, movielist_create=list_in, profile_id=profile.profile_id)
    movie_list_2 = db.get(MovieList, movie_list.list_id)
    
    assert movie_list_2
    assert movie_list.name == movie_list_2.name
    assert jsonable_encoder(movie_list) == jsonable_encoder(movie_list_2)


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_update_movie_list(db: Session) -> None:
    _, profile = user_and_profile_in(db)
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
    
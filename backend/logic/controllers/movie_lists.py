import uuid
from typing import Any

from sqlmodel import Session, select

from backend.logic.models import MovieList
from backend.logic.schemas.movie_lists import CreateMovieList, UpdateMovieList


def create_movie_list(*, session: Session, movielist_create: CreateMovieList, profile_id: uuid.UUID) -> MovieList:
    db_obj = MovieList.model_validate(
        movielist_create, update={"profile_id": profile_id}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_movie_list(*, session: Session, db_movielist: MovieList, movielist_in: UpdateMovieList) -> Any:
    movielist_data = movielist_in.model_dump(exclude_unset=True)
    extra_data = {}
    db_movielist.sqlmodel_update(movielist_data, update=extra_data)
    session.add(db_movielist)
    session.commit()
    session.refresh(db_movielist)
    return db_movielist
    
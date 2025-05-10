import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from backend.logic.models import (
    MovieList,
    Profile
)
from backend.logic.entities.movie_list import MovieList as EntityMovieList
from backend.logic.schemas.movie_lists import (
    CreateMovieList,
    UpdateMovieList,
    MovieListPublic,
    MovieListsPublic
)
from backend.logic.controllers import movie_lists, movie_list_controller
from backend.api.deps import CurrentUser, SessionDep, get_current_user
from backend.api.schemas import Message


router = APIRouter(prefix="/lists", tags=["movie-lists"])
msg = "The movie lists with this id does not exist in the system"


@router.get(
    "/all",
    dependencies=[Depends(get_current_user)],
    response_model=MovieListsPublic
)
def read_public_lists(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count_statement = select(func.count()).select_from(MovieList).filter(MovieList.privacy == False)
    count = session.exec(count_statement).one()

    statement = select(MovieList).offset(skip).limit(limit).filter(MovieList.privacy == False)
    movielists = session.exec(statement).all()
    
    if movielists:
        json_file = movie_list_controller.MovieListController().get_all()
        json_list = {
            (item["id"], item["profile_id"]): item
            for item in json_file
        }
        
        final_movie_lists = []
        for ml in movielists:
            key = (str(ml.list_id), str(ml.profile_id))
            movies = json_list.get(key, {}).get("movies", [])
            
            movie_list_data = {attr: getattr(ml, attr) for attr in dir(ml) if not attr.startswith('_')}
            movie_list_data["movies"] = movies

            final_movie_lists.append(movie_list_data)
        movielists = final_movie_lists

    return MovieListsPublic(movie_lists=movielists, count=count)


@router.get(
    "/my-lists",
    dependencies=[Depends(get_current_user)],
    response_model=MovieListsPublic,
)
def read_lists(session: SessionDep, current_user: CurrentUser) -> Any:
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    profile_in: Profile = session.exec(statement).first()
    profile_id = profile_in.profile_id

    count_statement = select(func.count()).select_from(MovieList).filter(MovieList.profile_id == profile_id)
    count = session.exec(count_statement).one()

    statement = select(MovieList).filter(MovieList.profile_id == profile_id)
    movielists = session.exec(statement).all()

    return MovieListsPublic(movie_lists=movielists, count=count)


@router.post(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=MovieListPublic
)
def create_list(session: SessionDep, list_in: CreateMovieList, current_user: CurrentUser) -> MovieList:
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    profile_in: Profile = session.exec(statement).first()
    profile_id = profile_in.profile_id

    movielist = movie_lists.create_movie_list(session=session, movielist_create=list_in, profile_id=profile_id)
    try:
        movie_list_controller.MovieListController().add(EntityMovieList(
            id=str(movielist.list_id),
            profile_id=str(movielist.profile_id)
        ))
    except Exception:
        session.delete(session.get(MovieList, movielist.list_id))
        session.commit()
        raise HTTPException(
            status_code=500,
            detail="Could not create movie list"
        )
    return movielist


@router.get(
    "/{list_id}",
    dependencies=[Depends(get_current_user)],
    response_model=MovieListPublic
)
def read_movie_list_by_id(
    list_id: uuid.UUID, 
    session: SessionDep,
    current_user: CurrentUser
) -> Any:
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    profile_in: Profile = session.exec(statement).first()
    profile_id = profile_in.profile_id

    movielist: MovieList = session.get(MovieList, list_id)
    if not movielist.privacy or movielist.profile_id == profile_id:
        json_file = movie_list_controller.MovieListController().get_by_id(str(list_id))
        
        movielist = {attr: getattr(movielist, attr) for attr in dir(movielist) if not attr.startswith('_')}
        movielist["movies"] = json_file["movies"]
    
    return movielist


@router.get(
    "/profile/{profile_id}",
    dependencies=[Depends(get_current_user)],
    response_model=MovieListsPublic,
)
def read_lists_by_profile(session: SessionDep, profile_id: uuid.UUID) -> Any:
    count_statement = select(func.count()).select_from(MovieList).where(
        (MovieList.profile_id == profile_id) & (MovieList.privacy == False)
    )
    count = session.exec(count_statement).one()

    statement = select(MovieList).where(
        (MovieList.profile_id == profile_id) & (MovieList.privacy == False)
    )
    movielists = session.exec(statement).all()

    return MovieListsPublic(movie_lists=movielists, count=count)


@router.patch(
    "/{list_id}",
    dependencies=[Depends(get_current_user)],
    response_model=MovieListPublic
)
def update_list(
    session: SessionDep, 
    list_id: uuid.UUID, 
    list_in: UpdateMovieList,
    current_user: CurrentUser
) -> Any:
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    profile_in: Profile = session.exec(statement).first()
    profile_id = profile_in.profile_id

    db_list: MovieList = session.get(MovieList, list_id)
    if not db_list:
        raise HTTPException(
            status_code=404,
            detail=msg,
        )
    if not db_list.profile_id == profile_id:
        raise HTTPException(
            status_code=401,
            detail='Not authorize to update list'
        )
    
    db_list = movie_lists.update_movie_list(session=session, db_movielist=db_list, movielist_in=list_in)
    return db_list


@router.patch(
    "/{list_id}/a/movie/{movie_id}",
    dependencies=[Depends(get_current_user)],
    response_model=Message
)
def add_movie_to_list(
    session: SessionDep,
    list_id: uuid.UUID, 
    movie_id: str,
    current_user: CurrentUser
) -> Any:
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    profile_in: Profile = session.exec(statement).first()
    profile_id = profile_in.profile_id

    db_list: MovieList = session.get(MovieList, list_id)
    if not db_list:
        raise HTTPException(
            status_code=404,
            detail=msg,
        )
    if not db_list.profile_id == profile_id:
        raise HTTPException(
            status_code=401,
            detail='Not authorize to update list'
        )
    
    add = movie_list_controller.MovieListController().add_movie(str(list_id), movie_id)
    alter = "not " if not add else " "
    return Message(message=f"{movie_id} {alter}added")


@router.patch(
    "/{list_id}/r/movie/{movie_id}",
    dependencies=[Depends(get_current_user)],
    response_model=Message
)
def remove_movie_to_list(
    session: SessionDep,
    list_id: uuid.UUID, 
    movie_id: str,
    current_user: CurrentUser
) -> Any:
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    profile_in: Profile = session.exec(statement).first()
    profile_id = profile_in.profile_id

    db_list: MovieList = session.get(MovieList, list_id)
    if not db_list:
        raise HTTPException(
            status_code=404,
            detail=msg,
        )
    if not db_list.profile_id == profile_id:
        raise HTTPException(
            status_code=401,
            detail='Not authorize to update list'
        )

    rmv = movie_list_controller.MovieListController().remove_movie(str(list_id), movie_id)
    alter = "not " if not rmv else " "
    return Message(message=f"{movie_id} {alter}removed")


@router.delete(
    "/{list_id}",
    dependencies=[Depends(get_current_user)],
    response_model=Message
)
def delete_movie_list(session: SessionDep, list_id: uuid.UUID, current_user: CurrentUser) -> Any:
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    profile_in: Profile = session.exec(statement).first()
    profile_id = profile_in.profile_id

    db_list: MovieList = session.get(MovieList, list_id)
    if not db_list:
        raise HTTPException(
            status_code=404,
            detail=msg,
        )
    if not db_list.profile_id == profile_id:
        raise HTTPException(
            status_code=401,
            detail='Not authorize to delete list'
        )
    
    rmv = movie_list_controller.MovieListController().remove(str(list_id))
    if not rmv:
        raise HTTPException(
            status_code=500,
            detail="Could not delete movie list"
        )

    session.delete(db_list)
    session.commit()
    return Message(message=f"{list_id} removed successfully")

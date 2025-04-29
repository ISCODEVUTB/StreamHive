import uuid
from typing import Any, Annotated

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from backend.logic.models import (
    MovieList
)
from backend.logic.schemas.movie_list import (
    CreateMovieList,
    UpdateMovieList,
    MovieListPublic,
    MovieListsPublic
)
from backend.logic.controllers import movie_lists
from backend.api.deps import SessionDep


router = APIRouter(prefix="/movie-lists", tags=["movie-lists"])
msg = "The movie lists with this id does not exist in the system"

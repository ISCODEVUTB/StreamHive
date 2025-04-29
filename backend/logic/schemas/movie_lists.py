import uuid
from sqlmodel import SQLModel

from backend.logic.schemas.profiles import ProfilePublic


class MovieListBase(SQLModel):
    name: str
    description: str | None = None


class CreateMovieList(MovieListBase):
    pass


class UpdateMovieList(MovieListBase):
    name: str | None = None


class MovieListPublic(MovieListBase):
    list_id: uuid.UUID


class MovieListsPublic(SQLModel):
    movie_lists: list[MovieListPublic]
    count: int


class ProfileMovieLists(ProfilePublic, MovieListsPublic):
    pass
    
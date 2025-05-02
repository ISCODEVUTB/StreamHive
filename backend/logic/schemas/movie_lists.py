import uuid
from sqlmodel import SQLModel

from backend.logic.schemas.profiles import ProfilePublic


class MovieListBase(SQLModel):
    name: str
    description: str | None = None
    privacy: bool = False


class CreateMovieList(MovieListBase):
    pass


class UpdateMovieList(MovieListBase):
    name: str | None = None
    privacy: bool | None = None


class MovieListPublic(MovieListBase):
    list_id: uuid.UUID
    profile_id: uuid.UUID
    movies: list | None = None


class MovieListsPublic(SQLModel):
    movie_lists: list[MovieListPublic]
    count: int


class ProfileMovieLists(ProfilePublic, MovieListsPublic):
    pass
    
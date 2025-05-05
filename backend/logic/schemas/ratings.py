import uuid
from sqlmodel import SQLModel


class ProfileRating(SQLModel):
    movie_id: str
    rate: float


class ProfileRatingsPublic(SQLModel):
    profile_id: uuid.UUID
    username: str
    ratings: list[ProfileRating]


class MovieRating(SQLModel):
    profile_id: uuid.UUID
    username: str
    rate: float


class MovieRatingsPublic(SQLModel):
    movie_id: str
    ratings: list[MovieRating]
    
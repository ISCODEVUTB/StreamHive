import uuid
from sqlmodel import Field, SQLModel


class ProfileRating(SQLModel):
    movie_id: str
    rate: float


class CreateRating(SQLModel):
    rate: float = Field(ge=1.5, le=5)


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
    
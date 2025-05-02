from sqlmodel import SQLModel


class ProfileRating(SQLModel):
    movie_id: str
    rate: float


class ProfileRatingsPublic(SQLModel):
    username: str
    ratings: list[ProfileRating]


class MovieRating(SQLModel):
    username: str
    rate: float


class MovieRatingsPublic(SQLModel):
    movie_id: str
    ratings: list[MovieRating]
    
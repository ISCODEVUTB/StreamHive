import uuid
from sqlmodel import SQLModel

from backend.logic.schemas.profiles import ProfilePublic
from backend.logic.schemas.articles import ArticlePublic


class CreateAuthor(SQLModel):
    profile_id: uuid.UUID
    article_id: uuid.UUID


class UpdateAuthor(SQLModel):
    profile_id: uuid.UUID | None
    article_id: uuid.UUID | None


class AuthorsPublic(SQLModel):
    article_id: uuid.UUID
    authors: list[ProfilePublic]
    count: int


class AuthorsArticles(SQLModel):
    profile_id: uuid.UUID
    articles: list[ArticlePublic]
    count: int
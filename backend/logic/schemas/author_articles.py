import uuid
from sqlmodel import SQLModel

from backend.logic.schemas.profiles import ProfilePublic
from backend.logic.schemas.articles import ArticlePublic


class CreateAuthor(SQLModel):
    profile_id: uuid.UUID
    article_id: uuid.UUID
    main_author: bool = False


class UpdateAuthor(SQLModel):
    profile_id: uuid.UUID | None = None
    article_id: uuid.UUID | None = None
    main_author: bool | None = None


class AuthorsPublic(SQLModel):
    article_id: uuid.UUID
    authors: list[ProfilePublic]
    count: int


class AuthorsArticles(SQLModel):
    profile_id: uuid.UUID
    articles: list[ArticlePublic]
    count: int
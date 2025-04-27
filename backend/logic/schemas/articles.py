import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel


class ArticleBase(SQLModel):
    article_title: str = Field(max_length=100)
    movie_ref_id: str | None = None


class CreateArticle(ArticleBase):
    section_id: int
    newsletter_id: int


class UpdateArticle(SQLModel):
    article_title: str | None = Field(default=None, max_length=100)
    section_id: int | None = None
    newsletter_id: int | None = None


class ArticlePublicEXT(ArticleBase):
    article_id: uuid.UUID
    created_at: datetime
    section: str
    newsletter: str


class ArticlePublic(ArticleBase):
    article_id: uuid.UUID
    created_at: datetime


class ArticlesPublic(SQLModel):
    articles: list[ArticlePublic]
    count: int

class ArticlesPublicEXT(SQLModel):
    articles: list[ArticlePublicEXT]
    count: int

class SectionArticles(SQLModel):
    section: str
    articles: list[ArticlePublic]
    count: int


class NewsletterArticles(SQLModel):
    newsletter: str
    data: list[SectionArticles]
    total_articles: int
    total_sections: int
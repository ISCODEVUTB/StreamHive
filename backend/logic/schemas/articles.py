import uuid
from datetime import date
from sqlmodel import Field, SQLModel


class ArticleBase(SQLModel):
    article_title: str = Field(max_length=100)


class CreateArticle(ArticleBase):
    section_id: int
    newsletter_id: int


class UpdateArticle(SQLModel):
    article_title: str | None = Field(max_length=100)
    section_id: int | None
    newsletter_id: int | None


class ArticlePublicEXT(ArticleBase):
    article_id: uuid.UUID
    date: date
    section: str
    newsletter: str


class ArticlePublic(ArticleBase):
    article_id: uuid.UUID
    date: date


class ArticlesPublic(SQLModel):
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
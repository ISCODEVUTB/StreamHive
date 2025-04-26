import uuid
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship


class Article(SQLModel, table=True):
    article_title: str = Field(max_length=100)
    movie_ref_id: str | None = Field(index=True, max_length=20)
    article_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = datetime.now(timezone.utc)
    section_id: int = Field(foreign_key='section.section_id')
    newsletter_id: int | None = Field(foreign_key='newsletter.newsletter_id')

    section: "Section" = Relationship(back_populates="article")
    newsletter: Optional["Newsletter"] = Relationship(back_populates="article")
    author_article: list["AuthorArticle"] = Relationship(back_populates="article")
    
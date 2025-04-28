import uuid
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship


class Article(SQLModel, table=True):
    """
    Database model representing an article.

    Attributes:
        article_title (str): Title of the article (max 100 characters).
        movie_ref_id (Optional[str]): Optional reference to a movie, indexed for faster searches (max 20 characters).
        article_id (UUID): Primary key identifier, auto-generated UUID.
        created_at (datetime): Timestamp when the article was created (UTC time).
        section_id (int): Foreign key linking to the Section this article belongs to.
        newsletter_id (Optional[int]): Foreign key linking to the Newsletter this article belongs to (can be None).

    Relationships:
        section (Section): Many-to-one relationship to the Section the article belongs to.
        newsletter (Optional[Newsletter]): Many-to-one relationship to the Newsletter the article is part of (optional).
        author_article (List[AuthorArticle]): One-to-many relationship with authors linked to this article.
    """
    article_title: str = Field(max_length=100)
    movie_ref_id: str | None = Field(index=True, max_length=20)
    article_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = datetime.now(timezone.utc)
    section_id: int = Field(foreign_key='section.section_id')
    newsletter_id: int | None = Field(foreign_key='newsletter.newsletter_id')

    section: "Section" = Relationship(back_populates="article")
    newsletter: Optional["Newsletter"] = Relationship(back_populates="article")
    author_article: list["AuthorArticle"] = Relationship(back_populates="article")
    
import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel


class ArticleBase(SQLModel):
    """
    Base model for article data containing common fields.

    Attributes:
        article_title (str): Title of the article (max 100 characters).
        movie_ref_id (Optional[str]): Reference ID of an associated movie, if any.
    """
    article_title: str = Field(max_length=100)
    movie_ref_id: str | None = None


class CreateArticle(ArticleBase):
    """
    Model for creating a new article.

    Attributes:
        section_id (int): ID of the section where the article belongs.
        newsletter_id (Optional[int]): ID of the related newsletter, if any.
    """
    section_id: int
    newsletter_id: int | None = None


class BodyArticle(SQLModel):
    """
    Model representing the Article entity.

    Attributes:
        content: The textual content of the article.
        image_rel_url: Location of the image used for the article 
    """
    content: str
    image_rel_url: str


class UpdateBodyArticle(SQLModel):
    """
    Model representing the Article entity.

    Attributes:
        content: The textual content of the article.
        image_rel_url: Location of the image used for the article 
    """
    content: str | None = None
    image_rel_url: str | None = None


class UpdateArticle(SQLModel):
    """
    Model for updating an existing article.

    Attributes:
        article_title (Optional[str]): New title for the article.
        section_id (Optional[int]): Updated section ID.
        newsletter_id (Optional[int]): Updated newsletter ID.
    """
    article_title: str | None = Field(default=None, max_length=100)
    section_id: int | None = None
    newsletter_id: int | None = None


class ArticlePublicEXT(ArticleBase):
    """
    Extended public-facing model for article details.

    Attributes:
        article_id (uuid.UUID): Unique identifier for the article.
        created_at (datetime): Timestamp of article creation.
        section (str): Name of the section the article belongs to.
        newsletter (str): Name of the associated newsletter.
    """
    article_id: uuid.UUID
    author: str
    created_at: datetime
    section: str
    newsletter: str | None = None
    body: list = []


class ArticlePublic(ArticleBase):
    """
    Public-facing model for basic article details.

    Attributes:
        article_id (uuid.UUID): Unique identifier for the article.
        created_at (datetime): Timestamp of article creation.
    """
    article_id: uuid.UUID
    created_at: datetime


class ArticlesPublic(SQLModel):
    """
    Model representing a list of public articles.

    Attributes:
        articles (List[ArticlePublic]): List of articles with basic public info.
        count (int): Total number of articles.
    """
    articles: list[ArticlePublic]
    count: int

class ArticlesPublicEXT(SQLModel):
    """
    Model representing a list of extended public articles.

    Attributes:
        articles (List[ArticlePublic]): List of articles with extended public info.
        count (int): Total number of articles.
    """
    articles: list[ArticlePublicEXT]
    count: int

class SectionArticles(SQLModel):
    """
    Model grouping articles by section.

    Attributes:
        section (str): Name of the section.
        articles (List[ArticlePublic]): List of articles under the section.
        count (int): Number of articles in the section.
    """
    section: str
    articles: list[ArticlePublic]
    count: int


class NewsletterArticles(SQLModel):
    """
    Model grouping sections and articles under a newsletter.

    Attributes:
        newsletter (str): Name of the newsletter.
        data (List[SectionArticles]): List of sections with their articles.
        total_articles (int): Total number of articles across all sections.
        total_sections (int): Total number of sections in the newsletter.
    """
    newsletter: str
    data: list[SectionArticles]
    total_articles: int
    total_sections: int
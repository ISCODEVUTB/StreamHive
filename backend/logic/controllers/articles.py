import uuid
from typing import Any, Optional
from datetime import datetime, date
from sqlmodel import Session, select

from backend.core.security import get_password_hash, verify_password
from backend.logic.models import Article
from backend.logic.schemas.articles import CreateArticle, UpdateArticle


def create_article(*, session: Session, article_create: CreateArticle) -> Article:
    """
    Create a new Article in the database.

    Args:
        session (Session): Active SQLModel database session.
        article_create (CreateArticle): Pydantic model containing the data for the new article.

    Returns:
        Article: The newly created Article object.
    """
    db_obj = Article.model_validate(article_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_article(*, session: Session, db_article: Article, article_in: UpdateArticle) -> Any:
    """
    Update an existing Article in the database.

    Args:
        session (Session): Active SQLModel database session.
        db_article (Article): The current Article object to update.
        article_in (UpdateArticle): Pydantic model containing the updated data.

    Returns:
        Article: The updated Article object.
    """
    article_data = article_in.model_dump(exclude_unset=True)
    extra_data = {}
    db_article.sqlmodel_update(article_data, update=extra_data)
    session.add(db_article)
    session.commit()
    session.refresh(db_article)
    return db_article


def get_article_by_section(*, session: Session, section_id: int) -> Optional[Article]:
    """
    Retrieve an Article by its section ID.

    Args:
        session (Session): Active SQLModel database session.
        section_id (int): The section ID to search for.

    Returns:
        Article | None: The found Article object if it exists, otherwise None.
    """
    statement = select(Article).where(Article.section_id == section_id)
    session_article = session.exec(statement).first()
    return session_article


def get_article_by_date(*, session: Session, newsletter_date: date) -> Optional[list[Article]]:
    """
    Retrieves all articles created on a specific date, ignoring the time part of the created_at.

    Args:
        session (Session): Active SQLModel database session.
        newsletter_date (date): The date to search for articles.

    Returns:
        list[Article] | None: List of Article objects created on the given date, or None if no articles were found.
    """
    start_of_day = datetime.combine(newsletter_date, datetime.min.time())  # 00:00:00
    end_of_day = datetime.combine(newsletter_date, datetime.max.time())    # 23:59:59

    # Query for articles created within the time range of the given date
    statement = select(Article).where(Article.created_at >= start_of_day, Article.created_at <= end_of_day)
    session_article = session.exec(statement).first()

    # Verify if articles exist for the given date
    if not session_article:
        raise ValueError(f"No hay artículos disponibles para la fecha {newsletter_date}.")
    
    return session_article

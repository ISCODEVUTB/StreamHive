import uuid
from typing import Any
from sqlmodel import Session, select

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
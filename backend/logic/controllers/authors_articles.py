from sqlmodel import Session, select
from backend.logic.models import AuthorArticle
from backend.logic.schemas.author_articles import CreateAuthor, UpdateAuthor
import uuid
from typing import Any


def create_author_article(*, session: Session, author_create: CreateAuthor) -> AuthorArticle:
    """
    Create a new AuthorArticle association in the database.

    Args:
        session (Session): Active SQLModel database session.
        author_create (CreateAuthor): Pydantic model containing the data for the association.

    Returns:
        AuthorArticle: The newly created AuthorArticle object.
    """
    db_obj = AuthorArticle.model_validate(author_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_author_article(
    *,
    session: Session,
    db_author_article: AuthorArticle,
    author_in: UpdateAuthor
) -> Any:
    """
    Update an existing AuthorArticle association in the database.

    Args:
        session (Session): Active SQLModel database session.
        db_author_article (AuthorArticle): The current AuthorArticle object to update.
        author_in (UpdateAuthor): Pydantic model containing the updated data.

    Returns:
        AuthorArticle: The updated AuthorArticle object.
    """
    author_data = author_in.model_dump(exclude_unset=True)
    extra_data = {}
    db_author_article.sqlmodel_update(author_data, update=extra_data)
    session.add(db_author_article)
    session.commit()
    session.refresh(db_author_article)
    return db_author_article


def get_author_articles_by_profile_id(
    *,
    session: Session,
    profile_id: uuid.UUID
) -> list[AuthorArticle]:
    """
    Retrieve all AuthorArticle associations for a given profile_id.

    Args:
        session (Session): Active SQLModel database session.
        profile_id (UUID): ID of the profile.

    Returns:
        list[AuthorArticle]: List of AuthorArticle objects linked to the profile.
    """
    statement = select(AuthorArticle).where(
        AuthorArticle.profile_id == profile_id
    )
    return list(session.exec(statement))


def get_author_articles_by_article_id(
    *,
    session: Session,
    article_id: uuid.UUID
) -> list[AuthorArticle]:
    """
    Retrieve all AuthorArticle associations for a given article_id.

    Args:
        session (Session): Active SQLModel database session.
        article_id (UUID): ID of the article.

    Returns:
        list[AuthorArticle]: List of AuthorArticle objects linked to the article.
    """
    statement = select(AuthorArticle).where(
        AuthorArticle.article_id == article_id
    )
    return list(session.exec(statement))


def delete_author_article(
    *,
    session: Session,
    db_author_article: AuthorArticle
) -> None:
    """
    Delete an AuthorArticle association from the database.

    Args:
        session (Session): Active SQLModel database session.
        db_author_article (AuthorArticle): The object to delete.
    """
    session.delete(db_author_article)
    session.commit()

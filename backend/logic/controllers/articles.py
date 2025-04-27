import uuid
from typing import Any, Optional
from datetime import datetime, date
from sqlmodel import Session, select

from backend.core.security import get_password_hash, verify_password
from backend.logic.models import Article
from backend.logic.schemas.articles import CreateArticle, UpdateArticle


def create_article(*, session: Session, article_create: CreateArticle) -> Article:
    db_obj = Article.model_validate(article_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_article(*, session: Session, db_article: Article, article_in: UpdateArticle) -> Any:
    article_data = article_in.model_dump(exclude_unset=True)
    extra_data = {}
    db_article.sqlmodel_update(article_data, update=extra_data)
    session.add(db_article)
    session.commit()
    session.refresh(db_article)
    return db_article


def get_article_by_section(*, session: Session, section_id: int) -> Optional[Article]:
    statement = select(Article).where(Article.section_id == section_id)
    session_article = session.exec(statement).first()
    return session_article


def get_article_by_date(*, session: Session, newsletter_date: date) -> Optional[list[Article]]:
    """
    Retrieves all articles that were created on a specific date, ignoring the time part of created_at.
    """
    # Crear el rango de tiempo para el día
    start_of_day = datetime.combine(newsletter_date, datetime.min.time())  # 00:00:00
    end_of_day = datetime.combine(newsletter_date, datetime.max.time())    # 23:59:59

    statement = select(Article).where(Article.created_at.cast(date) == newsletter_date)
    # Query para obtener artículos en ese rango de tiempo
    statement = select(Article).where(Article.created_at >= start_of_day, Article.created_at <= end_of_day)
    session_article = session.exec(statement).first()

    # Verificar si hay artículos disponibles
    if not session_article:
        raise ValueError(f"No hay artículos disponibles para la fecha {newsletter_date}.")
    
    return session_article

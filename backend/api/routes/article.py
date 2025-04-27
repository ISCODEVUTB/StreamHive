import uuid
from typing import Any, Annotated

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from backend.logic.models import (
    Article
)
from backend.logic.schemas.articles import (
    CreateArticle,
    ArticlePublic,
    ArticlesPublic
)
from backend.logic.controllers import articles
from backend.api.deps import SessionDep
from backend.logic.entities.article import Article

router = APIRouter(prefix="/articles", tags=["article"])

@router.get(
    "/",
    response_model=ArticlesPublic,
)
def read_profiles(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count_statement = select(func.count()).select_from(Article)
    count = session.exec(count_statement).one()

    statement = select(Article).offset(skip).limit(limit)
    articles= session.exec(statement).all()

    return ArticlesPublic(articles=articles, count=count)


@router.get("/{article_id}", response_model=ArticlePublic)
def read_article_by_id(
    article_id: uuid.UUID, 
    session: SessionDep
) -> Any:
    article = session.get(Article, article_id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return ArticlePublic(
        article_id=article.article_id,
        datetime=article.created_at,
        article_title=article.article_title
    )


@router.post(
    "/", 
    response_model=ArticlePublic
)
def create_article(*, session: SessionDep, article_in: CreateArticle, user_in: uuid.UUID) -> Any:
    article = articles.get_article_by_title(session=session, article_title=article_in.article_title)
    if article:
        raise HTTPException(
            status_code=400,
            detail="An article with this title already exists in the system.",
        )
    
    article = articles.create_article(session=session, article_create=article_in, user_id=user_in)
    return ArticlePublic(
        article_id=article.article_id,
        datetime=article.created_at,
        article_title=article.article_title
    )

import uuid
from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from backend.logic.models import (
    Article,
)
from backend.logic.schemas.articles import (
    CreateArticle,
    BodyArticle,
    UpdateArticle,
    SectionArticles,
    NewsletterArticles,
    ArticlePublic,
    ArticlesPublic
)
from backend.logic.entities import article as EntityArticle
from backend.logic.controllers import articles, article_controller
from backend.api.deps import SessionDep, get_current_active_internal_or_admin


router = APIRouter(prefix="/articles", tags=["article"])
msg = "The article with this id does not exist in the system"


@router.get(
    "/",
    response_model=ArticlesPublic,
)
def read_articles(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
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
    
    return article


@router.post(
    "/",
    dependencies=[Depends(get_current_active_internal_or_admin)],
    response_model=ArticlePublic
)
def create_article(
    *, 
    session: SessionDep, 
    article_in: CreateArticle, 
    body_article:BodyArticle
) -> Any:
    """
    Create a new article
    """
    article = articles.create_article(session=session, article_create=article_in)
    try:
        article_controller.ArticleController().add(EntityArticle(
            article_id=str(article.article_id),
            content=BodyArticle.content,
            image_rel_url=BodyArticle.image_rel_url
        ))
    except Exception:
        session.delete(session.get(Article, article.article_id))
        raise HTTPException(
            status_code=400,
            detail="Could not create movie list"
        )
    return article


@router.patch(
    "/{article_id}",
    response_model=ArticlePublic,
)
def update_article(
    *,
    session: SessionDep,
    article_id: uuid.UUID,
    article_in: UpdateArticle,
    body_article: BodyArticle,
) -> Any:
    db_article = session.get(Article, article_id)
    if not db_article:
        raise HTTPException(
            status_code=404,
            detail=msg,
        )
    
    try:
        updates = {}
        if body_article.content:
            updates['content'] = body_article.content
        if body_article.image_rel_url:
            updates['image_rel_url'] = body_article.image_rel_url

        article_controller.ArticleController().update_article(str(article_id), updates)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail='Could not update the file'
        )

    db_article = articles.update_article(session=session, db_article=db_article, article_in=article_in)
    return db_article


@router.delete(
    "/{article_id}", 
#    dependencies=[Depends(get_current_active_superuser)]
)
def delete_article(
    session: SessionDep, 
#    current_user: CurrentUser, 
    article_id: uuid.UUID
) -> None:
    db_article = session.get(Article, article_id)
    if not db_article:
        raise HTTPException(
            status_code=404,
            detail=msg,
        )
    
    session.delete(db_article)
    session.commit()
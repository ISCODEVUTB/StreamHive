import uuid
from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from backend.logic.models import (
    Article,
    Profile,
    AuthorArticle
)
from backend.logic.schemas.articles import (
    CreateArticle,
    BodyArticle,
    UpdateArticle,
    SectionArticles,
    NewsletterArticles,
    ArticlePublic,
    ArticlesPublic,
    UpdateBodyArticle
)
from backend.logic.entities.article import Article as EntityArticle
from backend.logic.controllers import articles, article_controller, authors_articles
from backend.logic.schemas.author_articles import CreateAuthor
from backend.api.deps import CurrentUser, SessionDep, get_current_active_internal_or_admin


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


@router.post(
    "/",
    dependencies=[Depends(get_current_active_internal_or_admin)],
    response_model=ArticlePublic
)
def create_article(
    *, 
    session: SessionDep, 
    article_in: CreateArticle, 
    body_article:BodyArticle,
    current_user: CurrentUser
) -> Any:
    """
    Create a new article
    """
    profile_id = session.exec(
        select(Profile.profile_id)
        .where(Profile.user_id == current_user.user_id)
    ).first()
    article = articles.create_article(session=session, article_create=article_in)
    try:
        article_controller.ArticleController().add(EntityArticle(
            article_id=article.article_id,
            content=body_article.content,
            image_rel_url=body_article.image_rel_url
        ))
        authors_articles.create_author_article(
            session=session,
            author_create=CreateAuthor(
                profile_id=profile_id, 
                article_id=article.article_id, 
                main_author=True
            )
        )
    except Exception as e:
        session.delete(session.get(Article, article.article_id))
        session.commit()
        raise HTTPException(
            status_code=400,
            detail=f"Could not create movie list: {e}"
        )
    return article


@router.get("/{article_id}", response_model=ArticlePublic)
def read_article_by_id(
    article_id: uuid.UUID, 
    session: SessionDep
) -> Any:
    article = session.get(Article, article_id)

    if not article:
        raise HTTPException(
            status_code=404, 
            detail="Article not found"
        )
    
    return article


@router.patch(
    "/{article_id}",
    dependencies=[Depends(get_current_active_internal_or_admin)],
    response_model=ArticlePublic
)
def update_article(
    *,
    session: SessionDep,
    article_id: uuid.UUID,
    article_in: UpdateArticle,
    body_article: UpdateBodyArticle,
    current_user: CurrentUser
) -> Any:
    profile_id = session.exec(
        select(Profile.profile_id)
        .where(Profile.user_id == current_user.user_id)
    ).first()

    db_article = session.get(Article, article_id)
    if not db_article:
        raise HTTPException(
            status_code=404,
            detail=msg,
        )
    db_article_author = session.exec(
        select(AuthorArticle)
        .where(
            (AuthorArticle.article_id == db_article.article_id) &
            (AuthorArticle.profile_id == profile_id)
        )
    )
    if not db_article_author:
        raise HTTPException(
            status_code=401,
            detail='Not authorized',
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
    dependencies=[Depends(get_current_active_internal_or_admin)]
)
def delete_article(
    session: SessionDep, 
    current_user: CurrentUser, 
    article_id: uuid.UUID
) -> None:
    profile_id = session.exec(
        select(Profile.profile_id)
        .where(Profile.user_id == current_user.user_id)
    ).first()

    db_article = session.get(Article, article_id)
    if not db_article:
        raise HTTPException(
            status_code=404,
            detail=msg,
        )
    db_article_author = session.exec(
        select(AuthorArticle)
        .where(
            (AuthorArticle.article_id == db_article.article_id) &
            (AuthorArticle.profile_id == profile_id)
        )
    ).first()
    if not db_article_author:
        raise HTTPException(
            status_code=401,
            detail='Not authorized',
        )
    
    try:
        article_controller.ArticleController().delete_article(str(article_id))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not delete movie list: {e}"
        )

    session.delete(db_article_author)
    session.delete(db_article)
    session.commit()
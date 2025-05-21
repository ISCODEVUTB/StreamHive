import uuid
from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from backend.logic.models import (
    Article,
    Profile,
    AuthorArticle,
    Section,
    Newsletter
)
from backend.logic.models.users import User
from backend.logic.schemas.articles import (
    ArticlePublicEXT,
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
from backend.api.schemas import Message


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

@router.get(
    "/newsletter/latest",
    response_model=NewsletterArticles
)
def get_latest_newsletter_articles(session: SessionDep) -> Any:
    # Buscar el newsletter más reciente
    latest_newsletter = session.exec(
        select(Newsletter).order_by(Newsletter.created_at.desc()).limit(1)
    ).first()

    if not latest_newsletter:
        raise HTTPException(status_code=404, detail="No newsletters found")

    # Buscar secciones con artículos de ese newsletter
    sections = session.exec(
        select(Section)
        .join(Article)
        .where(Article.newsletter_id == latest_newsletter.newsletter_id)
        .distinct()
    ).all()

    section_articles_list = []
    total_articles = 0

    for section in sections:
        articles_in_section = session.exec(
            select(Article).where(
                (Article.newsletter_id == latest_newsletter.newsletter_id) &
                (Article.section_id == section.section_id)
            )
        ).all()
        section_articles_list.append(
            SectionArticles(
                section=section.name,
                articles=articles_in_section,
                count=len(articles_in_section)
            )
        )
        total_articles += len(articles_in_section)

    return NewsletterArticles(
        newsletter=latest_newsletter.name,
        data=section_articles_list,
        total_articles=total_articles,
        total_sections=len(section_articles_list)
    )

@router.get("/{article_id}", response_model=ArticlePublicEXT)
def read_article_by_id(
    article_id: uuid.UUID, 
    session: SessionDep
) -> Any:
    article: Article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    section = session.get(Section, article.section_id)
    section_name = section.name if section else None
    if not section:
        raise HTTPException(status_code=500, detail="Section not found")

    newsletter_name = None
    if article.newsletter_id:
        newsletter = session.get(Newsletter, article.newsletter_id)
        newsletter_name = newsletter.name if newsletter else None
        if not newsletter:
            raise HTTPException(status_code=500, detail="Newsletter not found")

    author = session.exec(
        select(User.full_name)
        .join(Profile, User.user_id == Profile.profile_id)
        .join(AuthorArticle, Profile.profile_id == AuthorArticle.profile_id)
        .where(AuthorArticle.article_id == article_id)
    ).first()

    author_name = author or "Unknown"

    body_article = article_controller.ArticleController().get_by_id(str(article_id))
    body_content = body_article.get("body", []) if body_article else []

    return ArticlePublicEXT(
        article_id=article.article_id,
        article_title=article.article_title,
        movie_ref_id=article.movie_ref_id,
        created_at=article.created_at,
        section=section_name,
        newsletter=newsletter_name,
        author=author_name,
        body=body_content
    )


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
    dependencies=[Depends(get_current_active_internal_or_admin)],
    response_model=Message
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
            detail=f"Could not delete article: {e}"
        )

    session.delete(db_article_author)
    session.delete(db_article)
    session.commit()
    return Message(message='Article deleted successfully')

@router.get(
    "/section/{section_id}",
    response_model=SectionArticles
)
def get_articles_by_section(section_id: uuid.UUID, session: SessionDep) -> Any:
    section = session.get(Section, section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    articles_in_section = session.exec(
        select(Article).where(Article.section_id == section_id)
    ).all()

    return SectionArticles(
        section=section.name,
        articles=articles_in_section,
        count=len(articles_in_section)
    )


@router.get(
    "/newsletter/{newsletter_id}",
    response_model=NewsletterArticles
)
def get_articles_by_newsletter(newsletter_id: uuid.UUID, session: SessionDep) -> Any:
    newsletter = session.get(Newsletter, newsletter_id)
    if not newsletter:
        raise HTTPException(status_code=404, detail="Newsletter not found")

    # Obtener secciones asociadas a artículos dentro del newsletter
    statement = select(Section).join(Article).where(Article.newsletter_id == newsletter_id).distinct()
    sections = session.exec(statement).all()

    section_articles_list = []
    total_articles = 0

    for section in sections:
        articles_in_section = session.exec(
            select(Article).where(
                (Article.newsletter_id == newsletter_id) &
                (Article.section_id == section.section_id)
            )
        ).all()
        section_articles_list.append(
            SectionArticles(
                section=section.name,
                articles=articles_in_section,
                count=len(articles_in_section)
            )
        )
        total_articles += len(articles_in_section)

    return NewsletterArticles(
        newsletter=newsletter.name,
        data=section_articles_list,
        total_articles=total_articles,
        total_sections=len(section_articles_list)
    )

from fastapi.encoders import jsonable_encoder
import pytest
from sqlmodel import Session

from backend.logic.models import Article
from backend.logic.controllers import articles, article_tags
from backend.logic.schemas.articles import CreateArticle, UpdateArticle
from backend.logic.schemas.articles_tags import CreateTag
from backend.tests.utils.utils import random_lower_string, random_birth_date


def section_in():
    return CreateTag(
        name=random_lower_string(),
        description=random_lower_string()
    )


def newsletter_in():
    return CreateTag(
        name=str(random_birth_date()),
        description=random_lower_string()
    )


def test_create_article(db: Session) -> None:
    section = article_tags.create_section(session=db, section_create=section_in())
    article_in = CreateArticle(
        article_title=random_lower_string(),
        section_id=section.section_id
    )
    article = articles.create_article(session=db, article_create=article_in)
    
    assert article
    assert article.section_id == section.section_id


def test_create_news_article(db: Session) -> None:
    section = article_tags.create_section(session=db, section_create=section_in())
    newsletter = article_tags.create_newsletter(session=db, newsletter_create=newsletter_in())
    article_in = CreateArticle(
        article_title=random_lower_string(),
        section_id=section.section_id,
        newsletter_id=newsletter.newsletter_id
    )
    article = articles.create_article(session=db, article_create=article_in)
    
    assert article
    assert article.section_id == section.section_id
    assert article.newsletter_id == newsletter.newsletter_id


def test_get_article(db: Session) -> None:
    section = article_tags.create_section(session=db, section_create=section_in())
    article_in = CreateArticle(
        article_title=random_lower_string(),
        section_id=section.section_id
    )
    article = articles.create_article(session=db, article_create=article_in)
    article_2 = db.get(Article, article.article_id)

    assert article_2
    assert jsonable_encoder(article) == jsonable_encoder(article_2)


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_update_article(db: Session) -> None:
    section = article_tags.create_section(session=db, section_create=section_in())
    article_in = CreateArticle(
        article_title=random_lower_string(),
        section_id=section.section_id
    )
    article = articles.create_article(session=db, article_create=article_in)
   
    newsletter = article_tags.create_newsletter(session=db, newsletter_create=newsletter_in())
    article_in_update = UpdateArticle(
        newsletter_id=newsletter.newsletter_id
    )

    if article.article_id is not None:
        articles.update_article(session=db, db_article=article, article_in=article_in_update)
    article_2 = db.get(Article, article.article_id)
    
    assert article_2
    assert article_2.newsletter_id is not None
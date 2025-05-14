import uuid
import pytest
from sqlmodel import Session

from backend.logic.models import AuthorArticle
from backend.logic.controllers import article_tags, articles, authors_articles
from backend.logic.schemas.articles import CreateArticle
from backend.logic.schemas.articles_tags import CreateTag
from backend.logic.schemas.author_articles import CreateAuthor, UpdateAuthor
from backend.tests.utils.user import user_and_profile_in
from backend.tests.utils.utils import random_lower_string


def create_test_article(db: Session):
    section_in = CreateTag(
        name=random_lower_string(),
        description=random_lower_string()
    )
    section = article_tags.create_section(session=db, section_create=section_in)
    
    article_in = CreateArticle(
        article_title="Sample Article",
        section_id=section.section_id
    )
    return articles.create_article(session=db, article_create=article_in)


def test_get_author_articles_by_profile_id(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    article = create_test_article(db)

    author_in = CreateAuthor(profile_id=profile.profile_id, article_id=article.article_id, main_author=True)
    authors_articles.create_author_article(session=db, author_create=author_in)

    result = authors_articles.get_author_articles_by_profile_id(session=db, profile_id=profile.profile_id)

    assert len(result) == 1
    assert result[0].profile_id == profile.profile_id
    assert result[0].article_id == article.article_id


def test_get_author_articles_by_article_id(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    article = create_test_article(db)

    author_in = CreateAuthor(profile_id=profile.profile_id, article_id=article.article_id, main_author=True)
    authors_articles.create_author_article(session=db, author_create=author_in)

    result = authors_articles.get_author_articles_by_article_id(session=db, article_id=article.article_id)

    assert len(result) == 1
    assert result[0].article_id == article.article_id
    assert result[0].profile_id == profile.profile_id


def test_get_author_articles_empty(db: Session) -> None:
    profile_id = uuid.uuid4()
    article_id = uuid.uuid4()

    result_by_profile = authors_articles.get_author_articles_by_profile_id(session=db, profile_id=profile_id)
    result_by_article = authors_articles.get_author_articles_by_article_id(session=db, article_id=article_id)

    assert result_by_profile == []
    assert result_by_article == []


def test_create_author_article(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    article = create_test_article(db)

    author_in = CreateAuthor(profile_id=profile.profile_id, article_id=article.article_id, main_author=True)
    author = authors_articles.create_author_article(session=db, author_create=author_in)

    assert author.profile_id == profile.profile_id
    assert author.article_id == article.article_id


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_update_author_article_main_author(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    article = create_test_article(db)

    author_in = CreateAuthor(profile_id=profile.profile_id, article_id=article.article_id)
    author = authors_articles.create_author_article(session=db, author_create=author_in)

    # Simulamos una actualización para convertirlo en autor principal
    update_data = UpdateAuthor(
        main_author=True
    )
    updated: AuthorArticle = authors_articles.update_author_article(
        session=db,
        db_author_article=author,
        author_in=update_data
    )

    assert updated.profile_id == profile.profile_id
    assert updated.article_id == article.article_id
    assert updated.main_author is True


def test_delete_author_article(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    article = create_test_article(db)

    author_in = CreateAuthor(profile_id=profile.profile_id, article_id=article.article_id)
    author = authors_articles.create_author_article(session=db, author_create=author_in)

    # Eliminar
    authors_articles.delete_author_article(session=db, db_author_article=author)

    # Verificar que ya no existe
    result = authors_articles.get_author_articles_by_profile_id(
        session=db, profile_id=profile.profile_id
    )

    assert result == []
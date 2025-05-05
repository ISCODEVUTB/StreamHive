import uuid
import pytest
from sqlmodel import Session

from backend.logic.models import AuthorArticle
from backend.logic.controllers import article_tags, users, articles, profiles, authors_articles
from backend.logic.schemas.articles import CreateArticle
from backend.logic.schemas.articles_tags import CreateTag
from backend.logic.schemas.author_articles import CreateAuthor, UpdateAuthor
from backend.logic.schemas.profiles import CreateProfile
from backend.logic.schemas.users import CreateUser
from backend.logic.enum import UserTypes, UserGender, ProfileRoles
from backend.tests.utils.utils import random_email, random_lower_string, random_birth_date


full_name = "Test User"
gender = UserGender.OTHER
user_type = UserTypes.EXTERNAL


def create_test_profile(db: Session):
    user_in = CreateUser(
        full_name=full_name,
        email=random_email(),
        password=random_lower_string(),
        birth_date=random_birth_date(),
        user_gender=gender,
        user_type=user_type
    )
    user = users.create_user(session=db, user_create=user_in)

    profile_create = CreateProfile(
        username=random_lower_string(),
        profile_role=ProfileRoles.SUBSCRIBER
    )
    return profiles.create_profile(session=db, profile_create=profile_create, user_id=user.user_id)


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
    profile = create_test_profile(db)
    article = create_test_article(db)

    author_in = CreateAuthor(profile_id=profile.profile_id, article_id=article.article_id, main_author=True)
    authors_articles.create_author_article(session=db, author_create=author_in)

    result = authors_articles.get_author_articles_by_profile_id(session=db, profile_id=profile.profile_id)

    assert len(result) == 1
    assert result[0].profile_id == profile.profile_id
    assert result[0].article_id == article.article_id


def test_get_author_articles_by_article_id(db: Session) -> None:
    profile = create_test_profile(db)
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
    profile = create_test_profile(db)
    article = create_test_article(db)

    author_in = CreateAuthor(profile_id=profile.profile_id, article_id=article.article_id, main_author=True)
    author = authors_articles.create_author_article(session=db, author_create=author_in)

    assert author.profile_id == profile.profile_id
    assert author.article_id == article.article_id


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_update_author_article_main_author(db: Session) -> None:
    profile = create_test_profile(db)
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
    profile = create_test_profile(db)
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
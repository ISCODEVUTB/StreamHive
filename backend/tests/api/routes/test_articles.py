import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from backend.core.config import settings
from backend.logic.controllers import article_controller, profiles
from backend.logic.models import Article, Profile, AuthorArticle
from backend.tests.utils.utils import random_lower_string


def test_create_my_profile(
    db: Session, client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
        "username": random_lower_string(),
        "description": random_lower_string(),
        "profile_role": "subscriber"
    }

    r = client.post(
        f"{settings.API_V1_STR}/profiles",
        headers=superuser_token_headers,
        json=data
    )

    assert 200 <= r.status_code < 300
    created_profile = r.json()
    profile = profiles.get_profile_by_username(session=db, username=created_profile['username'])
    assert profile
    assert profile.username == created_profile['username']


def test_create_sections(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    data = {
        "name": "Test Section",
        "description": "Just a section to test the endpoint."
    }

    r = client.post(
        f"{settings.API_V1_STR}/articles/t/sections",
        headers=superuser_token_headers,
        json=data
    )

    assert 200 <= r.status_code < 300
    section = r.json()
    assert section['name'] == data['name']


def test_create_article(
    db: Session, client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
        "article_in": {
            "article_title": "Test Article",
            "section_id": 1
        },
        "body_article": {
            "content": "<p>This is a Test Article.</p>",
            "image_rel_url": "img/test.png"
        }
    }

    r = client.post(
        f"{settings.API_V1_STR}/articles/",
        headers=superuser_token_headers,
        json=data
    )

    assert 200 <= r.status_code < 300
    assert 'article_id' in r.json()


def test_create_article_normal_user(
    db: Session, client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    data = {
        "article_in": {
            "article_title": "Test Article",
            "section_id": 1
        },
        "body_article": {
            "content": "<p>This is a Test Article.</p>",
            "image_rel_url": "img/test.png"
        }
    }

    r = client.post(
        f"{settings.API_V1_STR}/articles/",
        headers=normal_user_token_headers,
        json=data
    )

    assert r.status_code == 403
    assert r.json()['detail'] == "The user doesn't have enough privileges"


def test_retrieve_articles(
    db: Session, client: TestClient
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/articles",
    )

    assert 200 <= r.status_code < 300
    articles = r.json()
    assert 'articles' in articles
    for article in articles['articles']:
        assert 'article_id' in article


def test_get_article(
    client: TestClient, db: Session
) -> None:
    article_id = db.exec(
        select(Article.article_id)
        .select_from(Article)
    ).first()
    r = client.get(
        f"{settings.API_V1_STR}/articles/{article_id}",
    )

    assert 200 <= r.status_code < 300
    article = r.json()
    assert 'article_id' in article


def test_get_article_not_found(
    client: TestClient, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/articles/{uuid.uuid4()}",
    )

    assert r.status_code == 404
    assert r.json()['detail'] == 'Article not found'


def test_update_article(
    db: Session, client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
        "article_in": {
            "article_title": "This is another Article Title.",
        },
        "body_article": {
            "image_rel_url": "img/article.png"
        }
    }

    article_id = db.exec(
        select(Article.article_id)
        .select_from(Article)
    ).first()

    r = client.patch(
        f"{settings.API_V1_STR}/articles/{article_id}",
        headers=superuser_token_headers,
        json=data
    )

    assert 200 <= r.status_code < 300
    assert 'article_id' in r.json()


def test_delete_article(
    db: Session, client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    article_id = db.exec(
        select(Article.article_id)
        .select_from(Article)
    ).first()

    r = client.delete(
        f"{settings.API_V1_STR}/articles/{article_id}",
        headers=superuser_token_headers,
    )
    article_controller.ArticleController().flush_list()

    assert 200 <= r.status_code < 300
    assert r.json()['message'] == 'Article deleted successfully'
    
    result = db.exec(select(Article).where(Article.article_id == article_id)).first()
    assert result is None
    result = db.exec(select(AuthorArticle).where(AuthorArticle.article_id == article_id)).first()
    assert result is None

def test_delete_profile(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    r_get = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers,
    )

    r_rmv = client.delete(
        f"{settings.API_V1_STR}/profiles/",
        headers=superuser_token_headers,
    )

    assert r_rmv.status_code == 200
    deleted_profile = r_rmv.json()
    assert deleted_profile["message"] == "Profile deleted successfully"

    result = db.exec(select(Profile).where(Profile.profile_id == uuid.UUID(r_get.json()['profile_id']))).first()
    assert result is None
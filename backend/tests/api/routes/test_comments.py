import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, delete, select

from backend.core.config import settings
from backend.logic.controllers import article_controller, profiles, comments
from backend.logic.models import Article, AuthorArticle, Profile, Comment
from backend.logic.schemas.comments import CreateComment
from backend.tests.utils.user import user_and_profile_in
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


def test_create_comment_article(
    db: Session, client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    article_id = db.exec(
        select(Article.article_id)
        .select_from(Article)
    ).first()

    data = {
        "content": "That was such an awsome article!",
        "has_spoilers": "false"
    }

    r = client.post(
        f"{settings.API_V1_STR}/comments/t/{'article'}/{article_id}",
        headers=superuser_token_headers,
        json=data
    )

    assert 200 <= r.status_code < 300
    assert 'comment_id' in r.json()
    comment = r.json()
    assert comment['has_spoilers'] == False


def test_create_comment_movie(
    client: TestClient, superuser_token_headers: dict[str, str]
):  
    movie_id = '12345'
    data = {
        "content": "That was such an awsome movie!",
        "has_spoilers": "false"
    }

    r = client.post(
        f"{settings.API_V1_STR}/comments/t/{'movie'}/{movie_id}",
        headers=superuser_token_headers,
        json=data
    )

    assert 200 <= r.status_code < 300
    assert 'comment_id' in r.json()
    comment = r.json()
    assert comment['has_spoilers'] == False


def test_create_comment_movie_w_spoilers(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    movie_id = '12345'
    data = {
        "content": "That was such an awsome movie!",
        "has_spoilers": "true"
    }

    r = client.post(
        f"{settings.API_V1_STR}/comments/t/{'movie'}/{movie_id}",
        headers=superuser_token_headers,
        json=data
    )

    assert 200 <= r.status_code < 300
    assert 'comment_id' in r.json()
    comment = r.json()
    assert comment['has_spoilers'] == True


def test_get_comment(
    db: Session, client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    comment_id = db.exec(
        select(Comment.comment_id)
        .select_from(Comment)
    ).first()

    r = client.get(
        f"{settings.API_V1_STR}/comments/{comment_id}",
        headers=superuser_token_headers
    )

    assert 200 <= r.status_code < 300
    comment = r.json()
    assert 'profile_id' in comment
    assert 'content' in comment


def test_retrieve_my_comments(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/comments/my-comments",
        headers=superuser_token_headers
    )

    assert 200 <= r.status_code < 300
    assert 'profile_id' in r.json()
    comments = r.json()['comments']
    assert len(comments) >= 1
    for obj in comments:
        assert obj['target_id'] is not None
        assert obj['target_type'] is not None


def test_retrieve_movie_comments(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    target_type = 'movie'
    target_id = '12345'
    r = client.get(
        f"{settings.API_V1_STR}/comments/t/{target_type}/{target_id}",
        headers=superuser_token_headers
    )

    assert 200 <= r.status_code < 300
    comments = r.json()
    assert comments['target_id'] == target_id
    assert comments['target_type'] == target_type
    assert len(comments['comments']) >= 1
    for obj in comments['comments']:
        assert obj['profile_id'] is not None
        assert obj['has_spoilers'] is not None


def test_retrieve_article_comments(
    db: Session, client: TestClient, superuser_token_headers: dict[str, str]
):
    target_type = 'article'
    target_id = db.exec(
        select(Article.article_id)
        .select_from(Article)
    ).first()
    r = client.get(
        f"{settings.API_V1_STR}/comments/t/{target_type}/{target_id}",
        headers=superuser_token_headers
    )

    assert 200 <= r.status_code < 300
    comments = r.json()
    assert comments['target_id'] == str(target_id)
    assert comments['target_type'] == target_type
    assert len(comments['comments']) >= 1
    for obj in comments['comments']:
        assert obj['profile_id'] is not None
        assert obj['has_spoilers'] is not None


def test_retrieve_comment_answers(
    db: Session, client: TestClient, superuser_token_headers: dict[str, str]
):
    target_type = 'comment'
    target_id = db.exec(
        select(Comment.comment_id)
        .select_from(Comment)
    ).first()

    _, profile = user_and_profile_in(db)
    comments.create_comment(
        session=db, 
        comment_in=CreateComment(content='Reply'), 
        profile_id=profile.profile_id,
        target_type=target_type,
        target_id=str(target_id)
    )

    r = client.get(
        f"{settings.API_V1_STR}/comments/t/{target_type}/{target_id}",
        headers=superuser_token_headers
    )

    assert 200 <= r.status_code < 300
    comment = r.json()
    assert comment['target_id'] == str(target_id)
    assert comment['target_type'] == target_type
    assert len(comment['comments']) >= 1
    for obj in comment['comments']:
        assert obj['profile_id'] is not None
        assert obj['has_spoilers'] is not None


def test_delete_comments(
    db: Session, client: TestClient, superuser_token_headers: dict[str, str]
):
    r_get = client.get(
        f"{settings.API_V1_STR}/comments/my-comments",
        headers=superuser_token_headers
    )

    for comment in r_get.json()['comments']:
        comment_id = uuid.UUID(comment['comment_id'])
        r_rmv = client.delete(
            f"{settings.API_V1_STR}/comments/{comment_id}",
            headers=superuser_token_headers
        )

        assert r_rmv.status_code == 200
        assert r_rmv.json()["message"] == "Comment deleted successfully"

        result = db.exec(select(Comment).where(Comment.comment_id == comment_id)).first()
        assert result is None


def test_delete_profile(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    db.exec(delete(Comment))
    db.exec(delete(Article))
    db.exec(delete(AuthorArticle))
    article_controller.ArticleController().flush_list()
    db.commit()

    r_get = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers,
    )

    r_rmv = client.delete(
        f"{settings.API_V1_STR}/profiles",
        headers=superuser_token_headers,
    )

    assert r_rmv.status_code == 200
    deleted_profile = r_rmv.json()
    assert deleted_profile["message"] == "Profile deleted successfully"

    result = db.exec(select(Profile).where(Profile.profile_id == uuid.UUID(r_get.json()['profile_id']))).first()
    assert result is None
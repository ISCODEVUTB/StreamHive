import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, delete, select

from backend.core.config import settings
from backend.logic.controllers import article_controller, profiles
from backend.logic.models import (
    Article, 
    AuthorArticle, 
    Profile, 
    Comment, 
    Reaction
)
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


def test_create_comment(
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


def test_create_reaction_article(
    db: Session, client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    target_type = 'article'
    target_id = db.exec(
        select(Article.article_id)
        .select_from(Article)
    ).first()

    r = client.post(
        f"{settings.API_V1_STR}/reactions/t/{target_type}/{target_id}",
        headers=superuser_token_headers,
    )

    assert 200 <= r.status_code < 300
    reaction = r.json()
    assert reaction['target_id'] == str(target_id)
    assert reaction['target_type'] == target_type


def test_create_reaction_movie(
    client: TestClient, superuser_token_headers: dict[str, str]
):  
    target_type = 'movie'
    target_id = '12345'

    r = client.post(
        f"{settings.API_V1_STR}/reactions/t/{target_type}/{target_id}",
        headers=superuser_token_headers,
    )

    assert 200 <= r.status_code < 300
    reaction = r.json()
    assert reaction['target_id'] == (target_id)
    assert reaction['target_type'] == target_type


def test_create_reaction_comment(
    db: Session, client: TestClient, superuser_token_headers: dict[str, str]
):  
    target_type = 'comment'
    target_id = db.exec(
        select(Comment.comment_id)
        .select_from(Comment)
    ).first()

    r = client.post(
        f"{settings.API_V1_STR}/reactions/t/{target_type}/{target_id}",
        headers=superuser_token_headers,
    )

    assert 200 <= r.status_code < 300
    reaction = r.json()
    assert reaction['target_id'] == str(target_id)
    assert reaction['target_type'] == target_type


def test_retrieve_movies_profiles_reactions(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    target_type = 'movie'
    profile_id = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers,
    ).json()['profile_id']
    r = client.get(
        f"{settings.API_V1_STR}/reactions/t/{target_type}/profile/{uuid.UUID(profile_id)}",
        headers=superuser_token_headers
    )

    assert 200 <= r.status_code < 300
    likes = r.json()
    assert likes['profile_id'] == profile_id
    assert len(likes['liked']) >= 1
    for obj in likes['liked']:
        assert obj['target_id'] is not None
        assert obj['target_type'] == target_type


def test_retrieve_article_profiles_reactions(
    db: Session, client: TestClient, superuser_token_headers: dict[str, str]
):
    target_type = 'article'
    profile_id = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers,
    ).json()['profile_id']
    r = client.get(
        f"{settings.API_V1_STR}/reactions/t/{target_type}/profile/{uuid.UUID(profile_id)}",
        headers=superuser_token_headers
    )

    assert 200 <= r.status_code < 300
    likes = r.json()
    assert likes['profile_id'] == profile_id
    assert len(likes['liked']) >= 1
    for obj in likes['liked']:
        assert obj['target_id'] is not None
        assert obj['target_type'] == target_type


def test_retrieve_comment_profiles_reactions(
    db: Session, client: TestClient, superuser_token_headers: dict[str, str]
):
    target_type = 'comment'
    profile_id = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers,
    ).json()['profile_id']
    r = client.get(
        f"{settings.API_V1_STR}/reactions/t/{target_type}/profile/{uuid.UUID(profile_id)}",
        headers=superuser_token_headers
    )

    assert 200 <= r.status_code < 300
    likes = r.json()
    assert likes['profile_id'] == profile_id
    assert len(likes['liked']) >= 1
    for obj in likes['liked']:
        assert obj['target_id'] is not None
        assert obj['target_type'] == target_type


def test_retrieve_movies_reactions(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    target_type = 'movie'
    target_id = '12345'
    r = client.get(
        f"{settings.API_V1_STR}/reactions/t/{target_type}/{target_id}",
        headers=superuser_token_headers
    )

    assert 200 <= r.status_code < 300
    likes = r.json()
    assert likes['target_id'] == target_id
    assert likes['target_type'] == target_type
    assert len(likes['liked_by']) == 1
    for obj in likes['liked_by']:
        assert obj['profile_id'] is not None


def test_delete_reactions(
    db: Session, client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    target_type = 'movie'
    profile_id = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers,
    ).json()['profile_id']
    
    r_get = client.get(
        f"{settings.API_V1_STR}/reactions/t/{target_type}/my-reactions",
        headers=superuser_token_headers
    )

    for reaction in r_get.json()['liked']:
        target_id = reaction['target_id']
        r_rmv = client.delete(
            f"{settings.API_V1_STR}/reactions/t/{target_type}/{target_id}",
            headers=superuser_token_headers
        )

        assert r_rmv.status_code == 200
        assert r_rmv.json()["message"] == "Reaction deleted successfully"

        result = db.exec(
            select(Reaction)
            .where(
                (Reaction.target_type == target_type) &
                (Reaction.target_id == target_id) &
                (Reaction.profile_id == uuid.UUID(profile_id))
            )
        ).first()
        assert result is None


def test_delete_profile(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    db.exec(delete(Reaction))
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
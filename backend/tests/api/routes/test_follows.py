import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, delete, select

from backend.core.config import settings
from backend.logic.controllers import follows, profiles
from backend.logic.models import Profile, Follow
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


def test_create_follow(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    _, profile = user_and_profile_in(db)

    r = client.post(
        f"{settings.API_V1_STR}/follows/{profile.profile_id}",
        headers=superuser_token_headers
    )

    assert 200 <= r.status_code < 300
    following = r.json()
    assert following['following_id'] == str(profile.profile_id)


def test_create_follow_myself(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    profile_id = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers
    ).json()['profile_id']

    r = client.post(
        f"{settings.API_V1_STR}/follows/{uuid.UUID(profile_id)}",
        headers=superuser_token_headers
    )

    assert 400
    assert r.json()['detail'] == "A user cannot follow themselves."


def test_retrieve_followers(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    _, profile = user_and_profile_in(db)
    my_profile = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers
    ).json()['profile_id']

    follows.create_follow(
        session=db, 
        follower_id=profile.profile_id, 
        following_id=uuid.UUID(my_profile)
    )
    r = client.get(
        f"{settings.API_V1_STR}/follows/my-followers",
        headers=superuser_token_headers
    )
    assert 'followers' in r.json()
    followers = r.json()['followers']
    assert len(followers) >= 1


def test_retrieve_following(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    _, profile = user_and_profile_in(db)
    my_profile = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers
    ).json()['profile_id']

    follows.create_follow(
        session=db, 
        following_id=profile.profile_id, 
        follower_id=uuid.UUID(my_profile)
    )
    r = client.get(
        f"{settings.API_V1_STR}/follows/my-following",
        headers=superuser_token_headers
    )
    assert 'following' in r.json()
    following = r.json()['following']
    assert len(following) >= 1
    for follow in following:
        assert 'profile_id' in follow


def test_retrieve_followers_others(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    my_profile = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers
    ).json()

    profile = db.exec(
        select(Follow.follower_id)
        .where(Follow.follower_id == uuid.UUID(my_profile['profile_id']))
    ).first()

    r = client.get(
        f"{settings.API_V1_STR}/follows/profile/{profile}/followers",
        headers=superuser_token_headers
    )
    assert r.json()['username'] == my_profile['username']
    assert 'followers' in r.json()
    assert len(r.json()['followers']) >= 1


def test_retrieve_following_others(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    my_profile = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers
    ).json()

    profile = db.exec(
        select(Follow.follower_id)
        .where(Follow.following_id == uuid.UUID(my_profile['profile_id']))
    ).first()

    r = client.get(
        f"{settings.API_V1_STR}/follows/profile/{profile}/following",
        headers=superuser_token_headers
    )
    assert 200 <= r.status_code < 300
    assert 'following' in r.json()
    assert len(r.json()['following']) >= 1


def test_delete_follow(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    profile_id = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers
    ).json()['profile_id']

    following =db.exec(
        select(Follow.following_id)
        .where(Follow.follower_id == uuid.UUID(profile_id))
    ).all()
    print("AQUI", uuid.UUID(profile_id), following)

    for id in following:
        r = client.delete(
            f"{settings.API_V1_STR}/follows/{id}",
            headers=superuser_token_headers
        )
        assert 200 <= r.status_code < 300
        assert r.json()['message'] == "Follow deleted successfully."


def test_delete_profile(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    db.exec(delete(Follow))
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
import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from backend.core.config import settings
from backend.logic.controllers import profiles, ratings
from backend.logic.models import Profile
from backend.logic.models.ratings import Rating
from backend.logic.schemas.ratings import CreateRating
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


def test_create_rating(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    movie_id = '12345'
    data = {
        "rate": 5
    }

    r = client.post(
        f"{settings.API_V1_STR}/ratings/movie/{movie_id}",
        headers=superuser_token_headers,
        json=data
    )
    assert 200 <= r.status_code < 300
    rating = r.json()
    assert 'movie_id' in rating
    assert rating['movie_id'] == movie_id


def test_update_rating(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    movie_id = '12345'
    data = {
        "rate": 2.5
    }

    r = client.post(
        f"{settings.API_V1_STR}/ratings/movie/{movie_id}",
        headers=superuser_token_headers,
        json=data
    )
    assert 200 <= r.status_code < 300
    rating = r.json()
    assert 'movie_id' in rating
    assert rating['movie_id'] == movie_id
    assert rating['rate'] == data['rate']


def test_retrieve_profile_ratings(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    profile_id = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers
    ).json()['profile_id']

    r = client.get(
        f"{settings.API_V1_STR}/ratings/profile/{uuid.UUID(profile_id)}",
        headers=superuser_token_headers
    )
    assert 200 <= r.status_code < 300
    assert r.json()['profile_id'] == profile_id
    assert 'ratings' in r.json()
    assert len(r.json()['ratings']) >= 1


def test_retrieve_movie_ratings(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    movie_id = '12345'

    r = client.get(
        f"{settings.API_V1_STR}/ratings/movie/{movie_id}",
        headers=superuser_token_headers
    )
    assert 200 <= r.status_code < 300
    assert r.json()['movie_id'] == movie_id
    assert 'ratings' in r.json()
    for rating in r.json()['ratings']:
        assert 'username' in rating


def test_get_avg_rating(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
):
    movie_id = '12345'
    avg = 2.5
    for i in range(3):
        _, profile = user_and_profile_in(db)
        ratings.create_or_update_rating(
            session=db, 
            profile_id=profile.profile_id, 
            movie_id=movie_id,
            rating_in=CreateRating(rate=5-i)
        )
        avg += 5-i
    avg = round(avg/4, 2)

    r = client.get(
        f"{settings.API_V1_STR}/ratings/movie/{movie_id}/average"
    )

    assert 200 <= r.status_code < 300
    assert r.json()['avg_rate'] == avg


def test_delete_rating(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    profile_id = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers
    ).json()['profile_id']
    db_ratings = db.exec(
        select(Rating.profile_id, Rating.movie_id)
        .where(Rating.profile_id == uuid.UUID(profile_id))
    ).all()

    for profile, movie in db_ratings:
        r = client.delete(
            f"{settings.API_V1_STR}/ratings/movie/{movie}/profile/{profile}",
            headers=superuser_token_headers,
        )
        assert 200 <= r.status_code < 300
        assert 'message' in r.json()
        assert r.json()['message'] == "Rating deleted successfully."


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
import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from backend.core.config import settings
from backend.logic.controllers import profiles
from backend.logic.models import Profile
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


def test_get_my_profile(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:    
    r = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers
    )
    my_profile = r.json()
    assert 200 <= r.status_code < 300
    profile = db.get(Profile, uuid.UUID(my_profile['profile_id']))
    assert my_profile['username'] == profile.username
    assert my_profile['profile_role'] == profile.profile_role
    assert my_profile['profile_id'] == str(profile.profile_id)


def test_retrieve_profiles(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    _, profile1 = user_and_profile_in(db)
    _, profile2 = user_and_profile_in(db)
    assert profile1 and profile2

    r = client.get(f"{settings.API_V1_STR}/profiles/", headers=superuser_token_headers)
    all_profiles = r.json()

    assert len(all_profiles["profiles"]) > 1
    assert "count" in all_profiles
    for item in all_profiles["profiles"]:
        assert "username" in item


def test_get_existing_profile(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    _, profile = user_and_profile_in(db)
    assert profile
    
    r = client.get(
        f"{settings.API_V1_STR}/profiles/{profile.profile_id}",
        headers=superuser_token_headers
    )
    existing_profile = r.json()
    assert 200 <= r.status_code < 300
    assert existing_profile['profile_id'] == str(profile.profile_id)
    assert existing_profile['username'] == profile.username


def test_get_retrieving_profiles_permissions_error(
    client: TestClient
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/profiles/"
    )
    assert r.status_code == 401
    assert r.json()['detail'] == 'Not authenticated'


def test_create_profile_existing_username(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    _, profile = user_and_profile_in(db)

    data = {
        "username": profile.username,
        "description": random_lower_string(),
        "profile_role": "subscriber"
    }

    r = client.post(
        f"{settings.API_V1_STR}/profiles",
        headers=superuser_token_headers,
        json=data
    )

    created_profile = r.json()
    assert r.status_code == 400
    assert "_profile_id" not in created_profile


def test_update_profile(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    new_username = random_lower_string()
    data = {
        "username": new_username,
    }

    r = client.patch(
        f"{settings.API_V1_STR}/profiles/update",
        headers=superuser_token_headers,
        json=data
    )
    updated_profile = r.json()

    assert 200 <= r.status_code < 300
    assert updated_profile['username'] == new_username


def test_update_user_username_exists(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    _, profile2 = user_and_profile_in(db)

    data = {
        "username": profile2.username,
    }

    r = client.patch(
        f"{settings.API_V1_STR}/profiles/update",
        headers=superuser_token_headers,
        json=data
    )
    
    assert r.status_code == 409
    assert r.json()["detail"] == "Profile with this username already exists" 


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
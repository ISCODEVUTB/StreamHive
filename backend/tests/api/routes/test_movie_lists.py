import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from backend.core.config import settings
from backend.logic.controllers import profiles, users, movie_lists
from backend.logic.models import MovieList
from backend.logic.schemas.profiles import CreateProfile
from backend.logic.schemas.users import CreateUser
from backend.tests.utils.utils import random_birth_date, random_email, random_lower_string


def user_and_profile_in(db: Session):  
    user_create = CreateUser(
        email=random_email(), 
        password =random_lower_string(),
        birth_date=random_birth_date(),
        full_name='User Example',
        user_gender="other",
        user_type="external"
    )

    user = users.create_user(session=db, user_create=user_create)

    profile_create = CreateProfile(
        username=random_lower_string()
    )

    profile = profiles.create_profile(session=db, profile_create=profile_create, user_id=user.user_id)

    return user, profile

'''
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


def test_create_movie_list_public(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    data = {
        "name": "TestList",
        "description": random_lower_string(),
        "privacy": "false"
    }

    r = client.post(
        f"{settings.API_V1_STR}/lists",
        headers=superuser_token_headers,
        json=data
    )

    assert 200 <= r.status_code < 300
    movielist = db.get(MovieList, uuid.UUID(r.json()['list_id']))
    assert movielist
    assert movielist.name == data['name']
    assert str(movielist.privacy).lower == data['privacy']


def test_create_movie_list_private(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    data = {
        "name": "TestList",
        "description": random_lower_string(),
        "privacy": "true"
    }

    r = client.post(
        f"{settings.API_V1_STR}/lists",
        headers=superuser_token_headers,
        json=data
    )

    assert 200 <= r.status_code < 300
    movielist = db.get(MovieList, uuid.UUID(r.json()['list_id']))
    assert movielist
    assert movielist.name == data['name']
    assert movielist.privacy == data['privacy']


def test_add_movie(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    movies = ['Shrek', 'Madagascar', 'Luck', 'Piyu', 'Avatar']
    list_ids = db.exec(select(MovieList.list_id).select_from(MovieList)).all()

    for id in list_ids:
        for movie in movies:
            r = client.patch(
                f"{settings.API_V1_STR}/lists/{id}/a/movie/{movie}",
                headers=superuser_token_headers
            )
            assert 200 <= r.status_code < 300
            assert r.json()['message'] == f'{movie}  added'
        
        r = client.get(
            f"{settings.API_V1_STR}/lists/{id}",
            headers=superuser_token_headers
        )
        assert 200 <= r.status_code < 300
        movielist = r.json()['movies']
        assert len(movielist) == len(movies)

        for i, movie in enumerate(movielist):
            assert movie['movie_id'] == movies[i]
            assert 'created_at' in movie
        

def test_remove_movie(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    movies = ['Luck', 'Piyu']
    list_ids = db.exec(select(MovieList.list_id).select_from(MovieList)).all()

    for id in list_ids:
        for movie in movies:
            r = client.patch(
                f"{settings.API_V1_STR}/lists/{id}/d/movie/{movie}",
                headers=superuser_token_headers
            )
            assert 200 <= r.status_code < 300
            assert r.json()['message'] == f'{movie}  removed'
        
        r = client.get(
            f"{settings.API_V1_STR}/lists/{id}",
            headers=superuser_token_headers
        )
        assert 200 <= r.status_code < 300
        movielist = r.json()['movies']

        for i, movie in enumerate(movielist):
            assert not movie['movie_id'] == movies[i]


def test_get_movie_lists_public(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/lists/{id}",
        headers=superuser_token_headers
    )
'''

def test_get_movie_list_private_owner():
    pass


def test_get_movie_list_private_other():
    pass


def test_update_movie_list():
    pass


"""def test_retrive_movie_lists(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/lists/all",
        headers=superuser_token_headers,
    )

    all_lists = r.json()
    assert len(all_lists['movie_lists']) > 1
    for inter in all_lists['movie_list']:
        if inter['privacy'] == 'true':
            assert inter['movies'] == []
"""

def delete_movie_list():
    pass
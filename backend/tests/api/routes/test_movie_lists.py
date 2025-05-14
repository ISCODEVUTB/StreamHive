import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from backend.core.config import settings
from backend.logic.controllers import movie_list_controller, profiles, movie_lists
from backend.logic.models import MovieList, Profile
from backend.logic.schemas.movie_lists import CreateMovieList
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
    assert str(movielist.privacy).lower() == data['privacy']


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
    assert str(movielist.privacy).lower() == data['privacy']


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
            assert 'added_at' in movie
        

def test_remove_movie(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    movies = ['Luck', 'Piyu']
    list_ids = db.exec(select(MovieList.list_id).select_from(MovieList)).all()

    for id in list_ids:
        for movie in movies:
            r = client.patch(
                f"{settings.API_V1_STR}/lists/{id}/r/movie/{movie}",
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
            assert movie['movie_id'] not in movies


def test_get_movie_lists_public(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    list_id = db.exec(
        select(MovieList.list_id)
        .select_from(MovieList)
        .where(MovieList.privacy == False)
    ).first()

    r = client.get(
        f"{settings.API_V1_STR}/lists/{list_id}",
        headers=superuser_token_headers
    )
    the_list = r.json()

    assert 'privacy' in the_list
    assert not the_list['privacy']
    #assert the_list['movies'] != []


def test_get_movie_list_private_owner(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    list_id = db.exec(
        select(MovieList.list_id)
        .select_from(MovieList)
        .where(MovieList.privacy == True)
    ).first()

    r = client.get(
        f"{settings.API_V1_STR}/lists/{list_id}",
        headers=superuser_token_headers
    )
    the_list = r.json()

    assert 'privacy' in the_list
    assert the_list['privacy']
    #assert the_list['movies'] != []


def test_get_movie_list_private_other(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    _, profile = user_and_profile_in(db)
    other_list = movie_lists.create_movie_list(
        session=db,
        movielist_create=CreateMovieList(name='Test List', privacy=True),
        profile_id=profile.profile_id
    )

    r = client.get(
        f"{settings.API_V1_STR}/lists/{other_list.list_id}",
        headers=superuser_token_headers
    )
    the_list = r.json()

    assert 'privacy' in the_list
    assert the_list['privacy']
    assert the_list['movies'] is None


def test_update_movie_list(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    list_id = db.exec(
        select(MovieList.list_id)
        .select_from(MovieList)
        .where(MovieList.privacy == True)
    ).first()

    new_name = 'New Test Name'
    data = {
        "name": new_name,
        "description":random_lower_string(),
        "privacy": "false" 
    }

    r = client.patch(
        f"{settings.API_V1_STR}/lists/{list_id}",
        headers=superuser_token_headers,
        json=data
    )

    assert 200 <= r.status_code < 300
    updated_list = r.json()
    assert updated_list['name'] == new_name
    assert not updated_list['privacy']


def test_retrive_movie_lists(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/lists/all",
        headers=superuser_token_headers,
    )

    all_lists = r.json()
    assert len(all_lists['movie_lists']) >= 1
    for inter in all_lists['movie_lists']:
        assert 'privacy' in inter
        assert not inter['privacy']


def test_retrive_my_movie_lists(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    profile_id = r.json()['profile_id']

    r = client.get(
        f"{settings.API_V1_STR}/lists/my-lists",
        headers=superuser_token_headers,
    )

    all_lists = r.json()
    assert len(all_lists['movie_lists']) >= 1
    for inter in all_lists['movie_lists']:
        assert 'profile_id' in inter
        assert inter['profile_id'] == profile_id


def test_retrive_movie_lists_by_profile(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    _, profile = user_and_profile_in(db)
    movie_lists.create_movie_list(
        session=db,
        movielist_create=CreateMovieList(name='Test List'),
        profile_id=profile.profile_id
    )
    movie_lists.create_movie_list(
        session=db,
        movielist_create=CreateMovieList(name='Test List', privacy=True),
        profile_id=profile.profile_id
    )
    
    r = client.get(
        f"{settings.API_V1_STR}/lists/profile/{profile.profile_id}",
        headers=superuser_token_headers,
    )

    profile_lists = r.json()
    assert len(profile_lists['movie_lists']) == 1
    for inter in profile_lists['movie_lists']:
        assert 'privacy' in inter
        assert not inter['privacy']


def test_delete_movie_list(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    profile_id = client.get(
        f"{settings.API_V1_STR}/profiles/my-profile",
        headers=superuser_token_headers,
    ).json()['profile_id']

    list_ids = db.exec(
        select(MovieList.list_id)
        .select_from(MovieList)
        .where(MovieList.profile_id == uuid.UUID(profile_id))
    ).all()

    for id in list_ids:
        r = client.delete(
            f"{settings.API_V1_STR}/lists/{id}",
            headers=superuser_token_headers
        )
        assert 200 <= r.status_code < 300
        assert r.json()['message'] == f"{id} removed successfully"
    
    movie_list_controller.MovieListController().flush_list()


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
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from backend.core.config import settings
from backend.logic.models import Section


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


def test_create_sections_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    data = {
        "name": "Test Section",
        "description": "Just a section to test the endpoint."
    }

    r = client.post(
        f"{settings.API_V1_STR}/articles/t/sections",
        headers=normal_user_token_headers,
        json=data
    )

    assert r.status_code == 403
    assert r.json()['detail'] == "The user doesn't have enough privileges"


def test_create_newsletter(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
        "name": "Test Newsletter",
        "description": "Just a newsletter to test the endpoint."
    }

    r = client.post(
        f"{settings.API_V1_STR}/articles/t/newsletters",
        headers=superuser_token_headers,
        json=data
    )

    assert 200 <= r.status_code < 300
    newsletter = r.json()
    assert newsletter['name'] == data['name']


def test_create_newsletters_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    data = {
        "name": "Test Newsletter",
        "description": "Just a newsletter to test the endpoint."
    }

    r = client.post(
        f"{settings.API_V1_STR}/articles/t/newsletters",
        headers=normal_user_token_headers,
        json=data
    )

    assert r.status_code == 403
    assert r.json()['detail'] == "The user doesn't have enough privileges"


def test_get_section(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/articles/t/sections",
        headers=superuser_token_headers
    )

    assert 200 <= r.status_code < 300
    assert 'sections' in r.json()
    section = r.json()['sections']
    assert section[0]['name'] == "Test Section"


def test_get_newsletter(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/articles/t/newsletters",
        headers=superuser_token_headers
    )

    assert 200 <= r.status_code < 300
    assert 'newsletters' in r.json()
    section = r.json()['newsletters']
    assert section[0]['name'] == "Test Newsletter"


def test_update_section(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    print(db.exec(select(Section)).all())

    data = {
        "name": "New Section"
    }

    r = client.patch(
        f"{settings.API_V1_STR}/articles/t/sections/{1}",
        headers=superuser_token_headers,
        json=data
    )

    assert 200 <= r.status_code < 300
    section = r.json()
    assert section['name'] == data['name']


def test_update_newsletter(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    data = {
        "name": "New Test Newsletter"
    }

    r = client.patch(
        f"{settings.API_V1_STR}/articles/t/newsletters/{1}",
        headers=superuser_token_headers,
        json=data
    )

    assert 200 <= r.status_code < 300
    section = r.json()
    assert section['name'] == data['name']


def test_delete_section(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    r = client.delete(
        f"{settings.API_V1_STR}/articles/t/sections/{1}",
        headers=superuser_token_headers,
    )

    assert 200 <= r.status_code < 300
    assert r.json()['message'] == 'Section deleted successfully'


def test_delete_newsletter(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    r = client.delete(
        f"{settings.API_V1_STR}/articles/t/newsletters/{1}",
        headers=superuser_token_headers,
    )

    assert 200 <= r.status_code < 300
    assert r.json()['message'] == 'Newsletter deleted successfully'
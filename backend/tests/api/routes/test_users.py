import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from backend.core.config import settings
from backend.core.security import verify_password
from backend.logic.controllers import users
from backend.logic.enum import UserGender, UserTypes
from backend.logic.models import User
from backend.logic.schemas.users import CreateUser
from backend.tests.utils.utils import random_birth_date, random_email, random_lower_string


def user_in(
    *,
    email: str,
    password: str
):
    return CreateUser(
        email=email, 
        password =password,
        birth_date=random_birth_date(),
        full_name = "Test User",
        user_gender = UserGender.OTHER,
        user_type = UserTypes.EXTERNAL
    )


def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/account", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["user_status"] == 'active'
    assert current_user["user_type"] == 'admin'
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/account", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["user_status"] == 'active'
    assert current_user["user_type"] == 'external'
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_create_user_new_email(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    email=random_email()
    password =random_lower_string()
    birth_date=random_birth_date().isoformat()
    gender = UserGender.OTHER.value
    user_type = UserTypes.EXTERNAL.value
    
    data = {
        "full_name": "Test User",
        "email": email,
        "password": password,
        "birth_date": birth_date,
        "user_gender": gender,
        "user_type": user_type
    }
    r = client.post(
        f"{settings.API_V1_STR}/users",
        headers=superuser_token_headers,
        json=data,
    )
    
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = users.get_user_by_email(session=db, email=email)
    assert user
    assert user.email == created_user["email"]


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user = users.create_user(session=db, user_create=user_in(email=username, password=password))
    user_id = user.user_id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = users.get_user_by_email(session=db, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_get_existing_user_current_user(
    client: TestClient, 
    superuser_token_headers: dict[str, str], 
    db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user = users.create_user(session=db, user_create=user_in(email=username, password=password))
    user_id = user.user_id

    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )

    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = users.get_user_by_email(session=db, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_get_existing_user_permissions_error(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/{uuid.uuid4()}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403
    assert r.json() == {"detail": "The user doesn't have enough privileges"}


def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password =random_lower_string()
    birth_date=random_birth_date().isoformat()
    gender = UserGender.OTHER.value
    user_type = UserTypes.EXTERNAL.value
    users.create_user(session=db, user_create=user_in(email=username, password=password))
    data = {
        "full_name": "Test User",
        "email": username,
        "password": password,
        "birth_date": birth_date,
        "user_gender": gender,
        "user_type": user_type
    }
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_user_id" not in created_user


def test_create_user_by_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    username = random_email()
    password =random_lower_string()
    birth_date=random_birth_date().isoformat()
    gender = UserGender.OTHER.value
    user_type = UserTypes.EXTERNAL.value
    data = {
        "full_name": "Test User",
        "email": username,
        "password": password,
        "birth_date": birth_date,
        "user_gender": gender,
        "user_type": user_type
    }
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 403


def test_retrieve_users(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    users.create_user(session=db, user_create=user_in(email=username, password=password))

    username2 = random_email()
    password2 = random_lower_string()
    users.create_user(session=db, user_create=user_in(email=username2, password=password2))

    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users["users"]) > 1
    assert "count" in all_users
    for item in all_users["users"]:
        assert "email" in item


def test_update_user_me(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    full_name = "Updated Name"
    email = random_email()
    data = {"full_name": full_name, "email": email}
    r = client.patch(
        f"{settings.API_V1_STR}/users/account",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_user = r.json()
    assert updated_user["email"] == email
    assert updated_user["full_name"] == full_name

    user_query = select(User).where(User.email == email)
    user_db = db.exec(user_query).first()
    assert user_db
    assert user_db.email == email
    assert user_db.full_name == full_name


def test_update_password_me(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    new_password = random_lower_string()
    data = {
        "current_password": settings.FIRST_SUPERUSER_PASSWORD,
        "new_password": new_password,
    }
    r = client.patch(
        f"{settings.API_V1_STR}/users/account/password",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_user = r.json()
    assert updated_user["message"] == "Password updated successfully"

    user_query = select(User).where(User.email == settings.FIRST_SUPERUSER)
    user_db = db.exec(user_query).first()
    assert user_db
    assert user_db.email == settings.FIRST_SUPERUSER
    assert verify_password(new_password, user_db.hashed_password)

    # Revert to the old password to keep consistency in test
    old_data = {
        "current_password": new_password,
        "new_password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.patch(
        f"{settings.API_V1_STR}/users/account/password",
        headers=superuser_token_headers,
        json=old_data,
    )
    db.refresh(user_db)

    assert r.status_code == 200
    assert verify_password(settings.FIRST_SUPERUSER_PASSWORD, user_db.hashed_password)


def test_update_password_me_incorrect_password(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    new_password = random_lower_string()
    data = {"current_password": new_password, "new_password": new_password}
    r = client.patch(
        f"{settings.API_V1_STR}/users/account/password",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 400
    updated_user = r.json()
    assert updated_user["detail"] == "Incorrect password"


def test_update_user_me_email_exists(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user = users.create_user(session=db, user_create=user_in(email=username, password=password))

    data = {"email": user.email}
    r = client.patch(
        f"{settings.API_V1_STR}/users/account",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "User with this email already exists"


def test_register_user(client: TestClient, db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    full_name = random_lower_string()
    birth_date=random_birth_date().isoformat()
    gender = UserGender.OTHER.value
    user_type = UserTypes.EXTERNAL.value
    data = {
        "full_name": full_name,
        "email": username,
        "password": password,
        "birth_date": birth_date,
        "user_gender": gender,
        "user_type": user_type
    }
    r = client.post(
        f"{settings.API_V1_STR}/users/signup",
        json=data,
    )
    assert r.status_code == 200
    created_user = r.json()
    assert created_user["email"] == username
    assert created_user["full_name"] == full_name

    user_query = select(User).where(User.email == username)
    user_db = db.exec(user_query).first()
    assert user_db
    assert user_db.email == username
    assert user_db.full_name == full_name
    assert verify_password(password, user_db.hashed_password)


def test_register_user_already_exists_error(client: TestClient) -> None:
    password = random_lower_string()
    full_name = random_lower_string()
    birth_date=random_birth_date().isoformat()
    gender = UserGender.OTHER.value
    user_type = UserTypes.EXTERNAL.value
    data = {
        "full_name": full_name,
        "email": settings.FIRST_SUPERUSER,
        "password": password,
        "birth_date": birth_date,
        "user_gender": gender,
        "user_type": user_type
    }
    r = client.post(
        f"{settings.API_V1_STR}/users/signup",
        json=data,
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "The user with this email already exists in the system."


def test_update_user(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user = users.create_user(session=db, user_create=user_in(email=username, password=password))

    data = {"full_name": "Updated_full_name"}
    r = client.patch(
        f"{settings.API_V1_STR}/users/{user.user_id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_user = r.json()

    assert updated_user["full_name"] == "Updated_full_name"

    user_query = select(User).where(User.email == username)
    user_db = db.exec(user_query).first()
    db.refresh(user_db)
    assert user_db
    assert user_db.full_name == "Updated_full_name"


def test_update_user_not_exists(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"full_name": "Updated_full_name"}
    r = client.patch(
        f"{settings.API_V1_STR}/users/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "The user with this id does not exist in the system"


def test_update_user_email_exists(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user = users.create_user(session=db, user_create=user_in(email=username, password=password))

    username2 = random_email()
    password2 = random_lower_string()
    user2 = users.create_user(session=db, user_create=user_in(email=username2, password=password2))

    data = {"email": user2.email}
    r = client.patch(
        f"{settings.API_V1_STR}/users/{user.user_id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "User with this email already exists"


def test_delete_user(client: TestClient, db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user = users.create_user(session=db, user_create=user_in(email=username, password=password))
    user_id = user.user_id

    login_data = {
        "username": username,
        "password": password,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    r = client.post(
        f"{settings.API_V1_STR}/users/account/delete",
        headers=headers,
    )
    deleted_user = r.json()
    assert r.status_code == 200
    assert deleted_user["user_status"] == "deleted"
    result = db.exec(select(User).where(User.user_id == user_id)).first()
    db.refresh(result)
    assert result.email != username


def test_delete_user_super_user(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user = users.create_user(session=db, user_create=user_in(email=username, password=password))
    user_id = user.user_id
    r = client.delete(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    deleted_user = r.json()
    assert deleted_user["message"] == "User deleted successfully"
    result = db.exec(select(User).where(User.user_id == user_id)).first()
    assert result is None


def test_delete_user_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.delete(
        f"{settings.API_V1_STR}/users/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "The user with this id does not exist in the system"


def test_delete_user_without_privileges(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user = users.create_user(session=db, user_create=user_in(email=username, password=password))

    r = client.delete(
        f"{settings.API_V1_STR}/users/{user.user_id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "The user doesn't have enough privileges"
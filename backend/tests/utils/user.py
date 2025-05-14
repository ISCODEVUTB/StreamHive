from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.core.config import settings
from backend.logic.controllers import profiles, users
from backend.logic.enum import UserGender, UserTypes
from backend.logic.models import User
from backend.logic.schemas.profiles import CreateProfile
from backend.logic.schemas.users import CreateUser, UpdateUser
from backend.tests.utils.utils import random_birth_date, random_email, random_lower_string


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


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


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = users.get_user_by_email(session=db, email=email)
    if not user:
        user_in_create = CreateUser(
            email=email, 
            password =password,
            birth_date=random_birth_date(),
            full_name = "Test User",
            user_gender = UserGender.OTHER,
            user_type = UserTypes.EXTERNAL
        )
        user = users.create_user(session=db, user_create=user_in_create)
    else:
        user_in_update = UpdateUser(password=password)
        if not user.user_id:
            raise Exception("User id not set")
        user = users.update_user(session=db, db_user=user, user_in=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)
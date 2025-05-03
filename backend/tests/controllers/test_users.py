from fastapi.encoders import jsonable_encoder
import pytest
from sqlmodel import Session

from backend.core.security import verify_password
from backend.logic.models import User
from backend.logic.enum import UserTypes
from backend.logic.controllers import users
from backend.logic.schemas.users import CreateUser, UpdateUser
from backend.tests.utils.utils import random_email, random_lower_string, random_birth_date


full_name='User Example'
gender="Other"
user_type=UserTypes.EXTERNAL


def test_create_active_external_user(db: Session) -> None:
    user_in = CreateUser(
        full_name=full_name,
        email=random_email(), 
        password =random_lower_string(),
        birth_date=random_birth_date(),
        gender=gender,
        user_type=user_type
    )
    
    user = users.create_user(session=db, user_create=user_in)

    assert user.email == user_in.email
    assert hasattr(user, "hashed_password")
    assert user.user_type == 'external'
    assert user.user_status == 'active'


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_check_if_user_is_inactive(db: Session) -> None:
    user_in = CreateUser(
        full_name=full_name,
        email=random_email(), 
        password =random_lower_string(),
        birth_date=random_birth_date(),
        gender=gender,
        user_type=user_type
    )
    user = users.create_user(session=db, user_create=user_in)
    user_in_inactive = UpdateUser(
        user_status='inactive'
    )
    if user.user_id is not None:
        users.update_user(session=db, db_user=user, user_in=user_in_inactive)
    user_2 = db.get(User, user.user_id)
    
    assert user_2
    assert user_2.user_status == 'inactive'


def test_check_if_user_is_admin(db: Session) -> None:
    user_in = CreateUser(
        full_name=full_name,
        email=random_email(), 
        password =random_lower_string(),
        birth_date=random_birth_date(),
        gender=gender,
        user_type=UserTypes.ADMIN
    )
    user = users.create_user(session=db, user_create=user_in)
    assert user.user_type == UserTypes.ADMIN


def test_check_if_user_is_internal(db: Session) -> None:
    user_in = CreateUser(
        full_name=full_name,
        email=random_email(), 
        password =random_lower_string(),
        birth_date=random_birth_date(),
        gender=gender,
        user_type=UserTypes.INTERNAL
    )
    user = users.create_user(session=db, user_create=user_in)
    assert user.user_type == UserTypes.INTERNAL


def test_get_user(db: Session) -> None:
    user_in = CreateUser(
        full_name=full_name,
        email=random_email(), 
        password =random_lower_string(),
        birth_date=random_birth_date(),
        gender=gender,
        user_type=user_type
    )
    user = users.create_user(session=db, user_create=user_in)
    user_2 = db.get(User, user.user_id)
    
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_update_user(db: Session) -> None:
    user_in = CreateUser(
        full_name=full_name,
        email=random_email(), 
        password =random_lower_string(),
        birth_date=random_birth_date(),
        gender=gender,
        user_type=user_type
    )
    user = users.create_user(session=db, user_create=user_in)
    
    new_fullname = 'Jane Doe'
    new_password = 'new_password123'
    user_in_update = UpdateUser(
        full_name=new_fullname,
        password=new_password
    )
    
    if user.user_id is not None:
        users.update_user(session=db, db_user=user, user_in=user_in_update)
    user_2 = db.get(User, user.user_id)
    
    assert user_2
    assert user.email == user_2.email
    assert user_2.full_name == new_fullname
    assert verify_password(new_password, user_2.hashed_password)


def test_user_authentification(db: Session) -> None:
    user_in = CreateUser(
        full_name=full_name,
        email=random_email(), 
        password =random_lower_string(),
        birth_date=random_birth_date(),
        gender=gender,
        user_type=user_type
    )
    user = users.create_user(session=db, user_create=user_in)

    user_auth = users.authenticate(session=db, email=user_in.email, password=user_in.password)

    assert user
    assert user_auth


def test_failed_user_authentification_password(db: Session) -> None:
    user_in = CreateUser(
        full_name=full_name,
        email=random_email(), 
        password =random_lower_string(),
        birth_date=random_birth_date(),
        gender=gender,
        user_type=user_type
    )
    user = users.create_user(session=db, user_create=user_in)

    wrong_password = random_lower_string() 
    user_auth = users.authenticate(session=db, email=user_in.email, password=wrong_password)

    assert user
    assert user_auth is None


def test_failed_user_authentification_email(db: Session) -> None:
    user_in = CreateUser(
        full_name=full_name,
        email=random_email(), 
        password =random_lower_string(),
        birth_date=random_birth_date(),
        gender=gender,
        user_type=user_type
    )
    user = users.create_user(session=db, user_create=user_in)

    wrong_email = random_email() 
    user_auth = users.authenticate(session=db, email=wrong_email, password=user_in.password)

    assert user
    assert user_auth is None
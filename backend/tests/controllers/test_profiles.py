from fastapi.encoders import jsonable_encoder
import pytest
from sqlmodel import Session

from backend.logic.models import Profile
from backend.logic.enum import ProfileRoles
from backend.logic.controllers import users, profiles
from backend.logic.schemas.users import CreateUser
from backend.logic.schemas.profiles import CreateProfile, UpdateProfile
from backend.tests.utils.utils import random_email, random_lower_string, random_birth_date


def user_in() -> CreateUser:  
    return CreateUser(
        email=random_email(), 
        password =random_lower_string(),
        birth_date=random_birth_date(),
        full_name='User Example',
        gender="Other",
        user_type="external"
    )


def test_create_profile(db: Session) -> None:
    user = users.create_user(session=db, user_create=user_in())
    
    profile_in = CreateProfile(
        username=random_lower_string(),
        profile_role=ProfileRoles.SUBSCRIBER
    )
    profile = profiles.create_profile(session=db, profile_create=profile_in, user_id=user.user_id)

    assert user.user_id == profile.user_id
    assert profile.username == profile_in.username
    assert profile.profile_role == ProfileRoles.SUBSCRIBER


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_check_if_profile_is_critic(db: Session) -> None:
    user = users.create_user(session=db, user_create=user_in())
    profile_in = CreateProfile(
        username=random_lower_string(),
        profile_role=ProfileRoles.SUBSCRIBER
    )
    profile = profiles.create_profile(session=db, profile_create=profile_in, user_id=user.user_id)

    profile_in_critic = UpdateProfile(
        profile_role=ProfileRoles.CRITIC
    )
    if profile.profile_id is not None:
        profiles.update_profile(session=db, db_profile=profile, profile_in=profile_in_critic)
    profile_2 = db.get(Profile, profile.profile_id)
    
    assert profile_2
    assert profile_2.profile_role == ProfileRoles.CRITIC


def test_check_if_profile_is_editor(db: Session) -> None:
    user = users.create_user(session=db, user_create=user_in())
    profile_in = CreateProfile(
        username=random_lower_string(),
        profile_role=ProfileRoles.EDITOR
    )
    profile = profiles.create_profile(session=db, profile_create=profile_in, user_id=user.user_id)

    assert user.user_id == profile.user_id
    assert profile.username == profile_in.username
    assert profile.profile_role == ProfileRoles.EDITOR


def test_get_profile(db: Session) -> None:
    user = users.create_user(session=db, user_create=user_in())
    profile_in = CreateProfile(
        username=random_lower_string(),
        profile_role=ProfileRoles.EDITOR
    )
    profile = profiles.create_profile(session=db, profile_create=profile_in, user_id=user.user_id)
    profile_2 = db.get(Profile, profile.profile_id)
    
    assert profile_2
    assert profile.username == profile_2.username
    assert jsonable_encoder(profile) == jsonable_encoder(profile_2)


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_update_profile(db: Session) -> None:
    user = users.create_user(session=db, user_create=user_in())
    profile_in = CreateProfile(
        username=random_lower_string(),
        profile_role=ProfileRoles.EDITOR
    )
    profile = profiles.create_profile(session=db, profile_create=profile_in, user_id=user.user_id)
    
    new_username = random_lower_string()
    profile_in_update = UpdateProfile(
        username=new_username
    )
    
    if profile.profile_id is not None:
        profiles.update_profile(session=db, db_profile=profile, profile_in=profile_in_update)
    profile_2 = db.get(Profile, profile.profile_id)
    
    assert profile_2
    assert profile_2.username == new_username
    
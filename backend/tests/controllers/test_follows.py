import pytest
from sqlmodel import Session

from backend.logic.models import Follow
from backend.logic.enum import ProfileRoles, UserTypes
from backend.logic.controllers import users, profiles, follows
from backend.logic.schemas.follows import CreateFollow
from backend.logic.schemas.users import CreateUser
from backend.logic.schemas.profiles import CreateProfile
from backend.tests.utils.utils import random_email, random_lower_string, random_birth_date

full_name='User Example'
gender="Other"
user_type=UserTypes.EXTERNAL


def create_test_profile(db: Session):  
    user_in = CreateUser(
        full_name=full_name,
        email=random_email(), 
        password=random_lower_string(),
        birth_date=random_birth_date(),
        gender=gender,
        user_type=user_type
    )
    
    user = users.create_user(session=db, user_create=user_in)

    profile_create = CreateProfile(
        username=random_lower_string(),
        profile_role=ProfileRoles.SUBSCRIBER
    )
    profile = profiles.create_profile(session=db, profile_create=profile_create, user_id=user.user_id)

    return profile


def test_create_follow(db: Session) -> None:
    profile1 = create_test_profile(db)
    profile2 = create_test_profile(db)
    
    follow_in = CreateFollow(
        follower_id=profile1.profile_id, following_id=profile2.profile_id
    )

    follow = follows.create_follow(session=db, follow_create=follow_in)

    assert follow.follower_id==profile1.profile_id
    assert follow.following_id==profile2.profile_id


def test_get_profile_followers(db: Session) -> None:
    profile1 = create_test_profile(db)
    profile2 = create_test_profile(db)

    db.add(Follow(follower_id=profile1.profile_id, following_id=profile2.profile_id))
    db.commit()

    followers = follows.get_profile_followers(session=db, profile_id=profile2.profile_id)

    assert followers.count == 1
    assert followers.followers[0].profile_id == profile1.profile_id


def test_get_profile_following(db: Session) -> None:
    profile1 = create_test_profile(db)
    profile2 = create_test_profile(db)
    
    db.add(Follow(follower_id=profile1.profile_id, following_id=profile2.profile_id))
    db.commit()

    following = follows.get_profile_following(session=db, profile_id=profile1.profile_id)

    assert following.count == 1
    assert following.following[0].profile_id == profile2.profile_id

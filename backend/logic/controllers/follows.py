import uuid
from typing import Any

from sqlmodel import Session, select

from backend.logic.models import Follow, Profile
from backend.logic.schemas.profiles import ProfilePublic
from backend.logic.schemas.follows import (
    CreateFollow,
    FollowersPublic,
    FollowingPublic
)


def create_follow(
    *, session: Session, 
    follow_create: CreateFollow
) -> Follow:
    """
    Create a follow relationship between two profiles.

    Args:
        session (Session): Active SQLModel database session.
        follow_create (CreateFollow): Data containing follower and following IDs.

    Returns:
        Follow: The created follow relationship.
    """
    db_obj = Follow(
        follower_id=follow_create.follower_id,
        following_id=follow_create.following_id
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_profile_followers(*, session: Session, profile_id: uuid) -> FollowersPublic | None:
    """
    Retrieve all followers of a specific profile.

    Args:
        session (Session): SQLModel DB session.
        profile_id (uuid.UUID): ID of the profile whose followers to retrieve.

    Returns:
        FollowersPublic: A list of follower profiles and the count.
    """
    profile = session.get(Profile, profile_id)

    if not profile:
        return None

    query = (
        select(Profile)
        .join(Follow, Follow.follower_id == Profile.profile_id)
        .where(Follow.following_id == profile_id)
    )

    followers = session.exec(query).all()
    followers_list = [ProfilePublic.model_validate(f) for f in followers]

    return FollowersPublic(
        **ProfilePublic.model_validate(profile).model_dump(),
        followers=followers_list,
        count=len(followers_list)
    )


def get_profile_following(*, session: Session, profile_id: uuid) -> FollowingPublic | None:
    """
    Retrieve all profiles that a given profile is following.

    Args:
        session (Session): SQLModel DB session.
        profile_id (uuid.UUID): ID of the profile whose followers to retrieve.

    Returns:
        FollowingPublic: A list of following profiles and the count.
    """
    profile = session.get(Profile, profile_id)

    if not profile:
        return None

    query = (
        select(Profile)
        .join(Follow, Follow.following_id == Profile.profile_id)
        .where(Follow.follower_id == profile_id)
    )

    followings = session.exec(query).all()
    following_list = [ProfilePublic.model_validate(f) for f in followings]

    return FollowingPublic(
        **ProfilePublic.model_validate(profile).model_dump(),
        following=following_list,
        count=len(following_list)
    )

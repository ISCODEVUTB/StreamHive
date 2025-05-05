import uuid
from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from backend.api.schemas import Message
from backend.logic.models import Profile, Follow
from backend.logic.schemas.follows import (
    FollowersPublic,
    FollowingPublic
)
from backend.logic.controllers import follows
from backend.api.deps import CurrentUser, SessionDep, get_current_user


router = APIRouter(prefix="/follows", tags=["follows"])


@router.post(
    "/",  
    dependencies=[Depends(get_current_user)],
    response_model=Follow
)
def create_follow(
    *, 
    session: SessionDep,
    current_user: CurrentUser,
    following_id: uuid.UUID
) -> Follow:
    """
    Create a new follow relationship between two profiles.
    Validates that both profiles exist before creating the relationship.
    """
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    profile_in: Profile = session.exec(statement).first()
    follower_id = profile_in.profile_id

    following_profile = session.get(Profile, following_id)

    if not following_profile:
        raise HTTPException(
            status_code=404,
            detail="The followed profile does not exist in the system.",
        )
    
    if follower_id == following_id:
        raise HTTPException(
            status_code=400,
            detail="A user cannot follow themselves.",
        )

    db_follow = follows.create_follow(session=session, following_id=following_id, follower_id=follower_id)
    return db_follow


@router.get(
    "/my-followers",
    dependencies=[Depends(get_current_user)],
    response_model=FollowersPublic,
)
def read_profiles_followers(session: SessionDep, current_user: CurrentUser) -> FollowersPublic:
    """
    Get all followers for a given profile.
    """
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    profile_in: Profile = session.exec(statement).first()
    follower_id = profile_in.profile_id

    followers = follows.get_profile_followers(
        session=session, profile_id=follower_id
    )

    if not followers:
        raise HTTPException(status_code=404, detail="Profile not found")

    return followers


@router.get(
    "/my-following",
    dependencies=[Depends(get_current_user)],
    response_model=FollowingPublic,
)
def read_profiles_following(session: SessionDep, current_user: CurrentUser) -> FollowingPublic:
    """
    Get all profiles that a given profile is following.
    """
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    profile_in: Profile = session.exec(statement).first()
    follower_id = profile_in.profile_id

    followings = follows.get_profile_following(
        session=session, profile_id=follower_id
    )

    if not followings:
        raise HTTPException(status_code=404, detail="Profile not found")

    return followings


@router.get(
    "/profile/{follower_id}/followers",
    dependencies=[Depends(get_current_user)],
    response_model=FollowersPublic,
)
def read_profiles_followers(session: SessionDep, follower_id: uuid.UUID) -> FollowersPublic:
    """
    Get all followers for a given profile.
    """
    followers = follows.get_profile_followers(
        session=session, profile_id=follower_id
    )

    if not followers:
        raise HTTPException(status_code=404, detail="Profile not found")

    return followers


@router.get(
    "/profile/{follower_id}/following",
    dependencies=[Depends(get_current_user)],
    response_model=FollowingPublic,
)
def read_profiles_following(session: SessionDep, follower_id: uuid.UUID) -> FollowingPublic:
    """
    Get all profiles that a given profile is following.
    """
    followings = follows.get_profile_following(
        session=session, profile_id=follower_id
    )

    if not followings:
        raise HTTPException(status_code=404, detail="Profile not found")

    return followings


@router.delete(
    "/{followed_id}",
    dependencies=[Depends(get_current_user)],
    response_model=Message
)
def delete_follow(
    session: SessionDep,
    current_user: CurrentUser,
    followed_id: uuid.UUID
) -> dict:
    """
    Delete an existing follow relationship between two profiles.
    """
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    profile_in: Profile = session.exec(statement).first()
    follower_id = profile_in.profile_id

    db_follow = session.exec(
        select(Follow).where(
            Follow.follower_id == follower_id,
            Follow.following_id == followed_id
        )
    ).first()
    
    if not db_follow:
        raise HTTPException(
            status_code=404,
            detail="Follow not found.",
        )
    
    session.delete(db_follow)
    session.commit()
    return Message(message="Follow deleted successfully.")
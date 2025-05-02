import uuid
from typing import Any, Annotated

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from backend.logic.models import Profile, Follow
from backend.logic.schemas.follows import (
    CreateFollow,
    FollowersPublic,
    FollowingPublic
)
from backend.logic.controllers import follows
from backend.api.deps import SessionDep


router = APIRouter(prefix="/follows", tags=["follows"])


@router.post("/",  response_model=Follow)
def create_follow(*, session: SessionDep, follow_create: CreateFollow) -> Any:
    """
    Create a new follow relationship between two profiles.
    Validates that both profiles exist before creating the relationship.
    """
    follower_profile = session.get(Profile, follow_create.follower_id)
    following_profile = session.get(Profile, follow_create.following_id)

    if not follower_profile or not following_profile:
        raise HTTPException(
            status_code=404,
            detail="Either the follower or the followed profile does not exist in the system.",
        )
    
    if follow_create.follower_id == follow_create.following_id:
        raise HTTPException(
            status_code=400,
            detail="A user cannot follow themselves.",
        )

    db_follow = follows.create_follow(session=session, follow_create=follow_create)
    return db_follow


@router.get(
    "/profile/{follower_id}/followers",
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
    response_model=FollowersPublic,
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


@router.delete("/follows/{follower_id}/{followed_id}")
def delete_follow(
    session: SessionDep, 
    follower_id: uuid.UUID,
    followed_id: uuid.UUID
) -> dict:
    """
    Delete an existing follow relationship between two profiles.
    """
    db_follow = session.exec(
        select(Follow).where(
            Follow.follower_id == follower_id,
            Follow.followed_id == followed_id
        )
    ).first()
    
    if not db_follow:
        raise HTTPException(
            status_code=404,
            detail="Follow not found.",
        )
    
    session.delete(db_follow)
    session.commit()
    return {"message": "Follow deleted successfully."}

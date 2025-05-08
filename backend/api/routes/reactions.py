from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import func, select
import uuid

from backend.api.deps import CurrentUser, SessionDep, get_current_user
from backend.logic.controllers import reactions
from backend.logic.models import Reaction, Profile
from backend.logic.enum import TargetTypes
from backend.logic.schemas.reactions import (
    ReactionPublic,
    ReactionsPublic,
    ProfileReaction,
    ProfilesReactions
)
from backend.api.schemas import Message


router = APIRouter(prefix="/reactions", tags=["interactions"])


@router.post(
    "/{target_type}/{target_id}", 
    response_model=ReactionPublic, 
    dependencies=[Depends(get_current_user)])
def create_reaction(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    target_id: str,
    target_type: TargetTypes
) -> Reaction:
    """
    Create a reaction (like) to a target (movie, comment, article).
    """
    profile = session.exec(select(Profile).where(Profile.user_id == current_user.user_id)).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found for current user.")

    try:
        reaction = reactions.create_reaction(
            session=session,
            target_id=target_id,
            target_type=target_type,
            profile_id=profile.profile_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return reaction


@router.get(
    "/t/movies/profile/{profile_id}", 
    dependencies=[Depends(get_current_user)],
    response_model=ProfilesReactions
)
def get_movie_reactions_by_profile(profile_id: uuid.UUID, session: SessionDep):
    db_objs: list[Reaction] = reactions.get_reactions_by_profile(
        session=session, profile_id=profile_id, target_type=TargetTypes.MOVIE
    )
    liked = [
        ReactionPublic(target_id=r.target_id, target_type=r.target_type)
        for r in db_objs
    ]
    return ProfilesReactions(profile_id=profile_id, liked=liked, count=len(liked))


@router.get(
    "/t/comments/profile/{profile_id}", 
    dependencies=[Depends(get_current_user)],
    response_model=ProfilesReactions
)
def get_comments_reactions_by_profile(profile_id: uuid.UUID, session: SessionDep):
    db_objs: list[Reaction] = reactions.get_reactions_by_profile(
        session=session, profile_id=profile_id, target_type=TargetTypes.COMMENT
    )
    liked = [
        ReactionPublic(target_id=r.target_id, target_type=r.target_type)
        for r in db_objs
    ]
    return ProfilesReactions(profile_id=profile_id, liked=liked, count=len(liked))


@router.get(
    "/t/articles/profile/{profile_id}", 
    dependencies=[Depends(get_current_user)],
    response_model=ProfilesReactions
)
def get_articles_reactions_by_profile(profile_id: uuid.UUID, session: SessionDep):
    db_objs: list[Reaction] = reactions.get_reactions_by_profile(
        session=session, profile_id=profile_id, target_type=TargetTypes.ARTICLE
    )
    liked = [
        ReactionPublic(target_id=r.target_id, target_type=r.target_type)
        for r in db_objs
    ]
    return ProfilesReactions(profile_id=profile_id, liked=liked, count=len(liked))


@router.get(
    "/t/{target_type}/{target_id}", 
    dependencies=[Depends(get_current_user)],
    response_model=ReactionsPublic
)
def get_reactions_by_target(
    *,
    session: SessionDep,
    target_id: str,
    target_type: TargetTypes
) -> Any:
    """
    Get all reactions for a given target.
    """
    reaction = reactions.get_reactions_by_target(
        session=session,
        target_type=target_type,
        target_id=target_id
    )

    return ReactionsPublic(
        target_id=target_id,
        target_type=target_type,
        liked_by=reaction,
        count=len(reaction)
    )


@router.delete(
    "/t/{target_type}/{target_id}",
    dependencies=[Depends(get_current_user)],
    response_model=Message
)
def delete_reaction(
    *, 
    session: SessionDep, 
    target_type: TargetTypes, 
    target_id: str,
    current_user: CurrentUser
) -> Message:
    profile = session.exec(select(Profile).where(Profile.user_id == current_user.user_id)).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found for current user.")
    
    statement = select(Reaction).where(
        (Reaction.profile_id == profile.profile_id) &
        (Reaction.target_type == target_type) & 
        (Reaction.target_id == target_id)
    )
    reaction = session.exec(statement).first()
    session.delete(reaction)
    session.commit()

    return Message(message='Reaction deleted successfully')
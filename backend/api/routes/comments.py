from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
import uuid

from backend.api.deps import CurrentUser, SessionDep, get_current_user
from backend.logic.controllers import comments
from backend.logic.models import Comment, Profile
from backend.logic.schemas.comments import (
    CreateComment, 
    CommentPublic, 
    CommentsPublic,
    ProfileComment,
    ProfileComments
)
from backend.logic.enum import TargetTypes
from backend.api.schemas import Message


router = APIRouter(prefix="/comments", tags=["interactions"])


@router.get(
    "/my-comments",
    response_model=ProfileComments,
    dependencies=[Depends(get_current_user)]
)
def get_my_comments(
    *,
    session: SessionDep,
    current_user: CurrentUser
) -> ProfileComments:
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    profile_in: Profile = session.exec(statement).first()
    profile_id = profile_in.profile_id

    comment_list = comments.get_comments_by_profile(session=session, profile_id=profile_id)
    return ProfileComments(
        profile_id=profile_id,
        comments=comment_list,
        count=len(comment_list)
    )


@router.post(
    "/t/{target_type}/{target_id}/p/{profile_id}", 
    response_model=CommentPublic,
    dependencies=[Depends(get_current_user)]
)
def create_comment(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    comment_in: CreateComment,
    target_id: str,
    target_type: TargetTypes
) -> Comment:
    profile = session.exec(select(Profile).where(Profile.user_id == current_user.user_id)).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")

    try:
        db_comment = comments.create_comment(
            session=session,
            comment_in=comment_in,
            profile_id=profile.profile_id,
            target_id=target_id,
            target_type=target_type
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return db_comment


@router.get(
    "/{comment_id}",
    response_model=CommentPublic,
    dependencies=[Depends(get_current_user)]
)
def get_comment(
    *,
    session: SessionDep,
    comment_id: uuid.UUID
) -> Comment:
    comment = session.get(Comment, comment_id)

    return comment


@router.delete(
    "/{comment_id}",
    response_model=Message,
    dependencies=[Depends(get_current_user)]
)
def delete_comment(
    *,
    session: SessionDep,
    comment_id: uuid.UUID
) -> Message:
    comment = session.get(Comment, comment_id)
    session.delete(comment)
    session.commit()

    return Message(message='Reaction deleted successfully')


@router.get(
    "/profile/{profile_id}",
    response_model=ProfileComments,
    dependencies=[Depends(get_current_user)]
)
def get_comments_by_profile(
    *,
    session: SessionDep,
    profile_id: uuid.UUID
) -> ProfileComments:
    comment_list = comments.get_comments_by_profile(session=session, profile_id=profile_id)
    return ProfileComments(
        profile_id=profile_id,
        comments=comment_list,
        count=len(comment_list)
    )


@router.get(
    "/t/{target_type}/{target_id}",
    response_model=CommentsPublic,
    dependencies=[Depends(get_current_user)]
)
def get_comments_by_target(
    *,
    session: SessionDep,
    target_type: TargetTypes,
    target_id: str
) -> CommentsPublic:
    comment_list = comments.get_comments_by_target(
        session=session,
        target_type=target_type,
        target_id=target_id
    )
    return CommentsPublic(
        target_id=target_id,
        target_type=target_type,
        comments=comment_list,
        count=len(comment_list)
    )
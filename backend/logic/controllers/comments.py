import uuid
from sqlmodel import Session, select
from typing import List

from backend.logic.models import Comment, Article
from backend.logic.schemas.comments import CreateComment
from backend.logic.enum import TargetTypes


def create_comment(
    *, 
    session: Session, 
    comment_in: CreateComment,
    profile_id: uuid.UUID,
    target_type: TargetTypes,
    target_id: str
) -> Comment:
    try:
        if target_type == TargetTypes.ARTICLE:
            db_obj = session.get(Article, uuid.UUID(target_id))
        elif target_type == TargetTypes.COMMENT:
            db_obj = session.get(Comment, uuid.UUID(target_id))
        else:
            db_obj = True
        
        if not db_obj:
            raise ValueError(f"{target_type.value.upper()} with id {target_id} not found")
    except ValueError as e:
        raise ValueError(str(e))
    
    db_obj = Comment(
        profile_id=profile_id,
        target_id=target_id,
        target_type=target_type,
        content=comment_in.content,
        has_spoilers=comment_in.has_spoilers
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_comments_by_target(
    *, session: Session, target_type: TargetTypes, target_id: uuid.UUID
) -> List[Comment]:
    statement = select(Comment).where(
        (Comment.target_type == target_type) & (Comment.target_id == target_id)
    )
    return session.exec(statement).all()


def get_comments_by_profile(
    *, session: Session, profile_id: uuid.UUID
) -> List[Comment]:
    statement = select(Comment).where(Comment.profile_id == profile_id)
    return session.exec(statement).all()
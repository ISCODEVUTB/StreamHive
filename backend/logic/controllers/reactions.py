import uuid
from sqlmodel import Session, select
from backend.logic.models import Reaction, Article, Comment
from backend.logic.enum import TargetTypes
from typing import Any


def create_reaction(
    *,
    session: Session,
    target_type: TargetTypes,
    target_id: str,
    profile_id: uuid.UUID
) -> Reaction:
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

    db_obj = Reaction(
        target_id=str(target_id),
        target_type=target_type,
        profile_id=profile_id
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_reactions_by_target(
    *, session: Session, target_type: TargetTypes, target_id: str
) -> list[Reaction]:
    statement = select(Reaction).where(
        (Reaction.target_type == target_type) & (Reaction.target_id == target_id)
    )
    results = session.exec(statement).all()
    return results


def get_reactions_by_profile(
    *, session: Session, profile_id: uuid.UUID, target_type: TargetTypes
) -> list[Reaction]:
    statement = select(Reaction).where(
        (Reaction.profile_id == profile_id) & (Reaction.target_type == target_type)
    )
    results = session.exec(statement).all()
    return results
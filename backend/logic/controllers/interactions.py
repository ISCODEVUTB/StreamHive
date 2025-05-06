import uuid
from sqlmodel import Session, select
from backend.logic.models import Interaction
from backend.logic.enum import TargetTypes, InteractTypes
from backend.logic.schemas.interactions import CreateInteraction
from typing import Any


def create_interaction(
    *, session: Session, interaction_create: CreateInteraction
) -> Interaction:
    db_obj = Interaction.model_validate(interaction_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_interactions_by_target(
    *, session: Session, target_type: TargetTypes
) -> list[Interaction]:
    statement = select(Interaction).where(
        Interaction.target_type == target_type
    )
    results = session.exec(statement).all()
    return results


def get_interactions_by_profile(
    *, session: Session, interaction_type: InteractTypes | None = None
) -> list[Interaction]:
    statement = select(Interaction).where(Interaction.interaction_type == interaction_type)
    results = session.exec(statement).all()
    return results
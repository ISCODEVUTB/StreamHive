import uuid
from sqlmodel import SQLModel

from backend.logic.enum import InteractTypes, TargetTypes


class CreateInteraction(SQLModel):
    target_id: uuid.UUID
    target_type: TargetTypes
    interaction_type: InteractTypes
    profile_id: uuid.UUID


class ProfileInteraction(SQLModel):
    profile_id: uuid.UUID
    Interaction_type: InteractTypes | None


class InteractionPublic(SQLModel):
    target_id: uuid.UUID
    target_type: TargetTypes
    Interaction_type: InteractTypes


class InteractionsPublic(SQLModel):
    target_id: uuid.UUID
    target_type: TargetTypes
    interactions: list[ProfileInteraction]
    count: int


class ProfilesInteractions(ProfileInteraction):
    interactions: list[InteractionPublic]
    count: int
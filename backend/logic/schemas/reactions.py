import uuid
from sqlmodel import SQLModel

from backend.logic.enum import TargetTypes


class ProfileReaction(SQLModel):
    profile_id: uuid.UUID


class ReactionPublic(SQLModel):
    target_id: str
    target_type: TargetTypes


class ReactionsPublic(SQLModel):
    target_id: str
    target_type: TargetTypes
    liked_by: list[ProfileReaction]
    count: int


class ProfilesReactions(ProfileReaction):
    liked: list[ReactionPublic]
    count: int
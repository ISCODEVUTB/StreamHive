import uuid
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from backend.logic.enum import InteractTypes, TargetTypes


class Interaction(SQLModel, table=True):
    target_id: uuid.UUID
    target_type: TargetTypes = Field(index=True)
    interaction_type: InteractTypes = Field(index=True)
    profile_id: uuid.UUID = Field(foreign_key='profile.profile_id')

    interaction_id: uuid.UUID = Field(default_factory=uuid.uuid4 ,primary_key=True)
    created_at: datetime = datetime.now(timezone.utc)

    profile: "Profile" = Relationship(back_populates='interaction')


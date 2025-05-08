import uuid
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from backend.logic.enum import TargetTypes


class Reaction(SQLModel, table=True):
    target_id: str = Field(primary_key=True)
    target_type: TargetTypes = Field(index=True, primary_key=True)
    profile_id: uuid.UUID = Field(foreign_key='profile.profile_id', primary_key=True)

    created_at: datetime = datetime.now(timezone.utc)

    profile: "Profile" = Relationship(back_populates='reaction')

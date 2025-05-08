import uuid
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from backend.logic.enum import TargetTypes


class Comment(SQLModel, table=True):
    target_id: str
    target_type: TargetTypes = Field(index=True)
    profile_id: uuid.UUID = Field(foreign_key='profile.profile_id')
    content: str = Field(max_length=500)
    has_spoilers: bool = Field(default=False)

    comment_id: uuid.UUID = Field(default_factory=uuid.uuid4 ,primary_key=True)
    created_at: datetime = datetime.now(timezone.utc)

    profile: "Profile" = Relationship(back_populates='comment')

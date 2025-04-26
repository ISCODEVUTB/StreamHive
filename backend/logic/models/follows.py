import uuid
from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel


class Follow(SQLModel, table=True):
    follower_id: uuid.UUID = Field(foreign_key="profile.profile_id", primary_key=True)
    following_id: uuid.UUID = Field(foreign_key="profile.profile_id", primary_key=True)
    created_at: datetime = datetime.now(timezone.utc)

    follower: "Profile" = Relationship(
        back_populates="following", sa_relationship_kwargs={"foreign_keys": "[Follow.follower_id]"}
    )
    following: "Profile" = Relationship(
        back_populates="followers", sa_relationship_kwargs={"foreign_keys": "[Follow.following_id]"}
    )

import uuid
from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel


class Rating(SQLModel, table=True):
    profile_id: uuid.UUID = Field(foreign_key="profile.profile_id" ,primary_key=True)
    movie_id: str = Field(max_length=20, primary_key=True)
    rate: float = Field(ge=1.5, le=5, decimal_places=1)
    created_at: datetime = datetime.now(timezone.utc)

    profile: "Profile" = Relationship(back_populates="rating")
    